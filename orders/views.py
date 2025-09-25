import json
import logging
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from yookassa import Configuration, Payment

from carts.cart import Cart
from common.mixins import TitleMixin
from orders.forms import FormOrder
from orders.models import Order
from orders.utils import create_order, telegram

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

logger = logging.getLogger(__name__)


class CreateOrderView(LoginRequiredMixin, TitleMixin, FormView):
    title = 'Order'
    form_class = FormOrder
    template_name = 'orders/create_orders.html'
    success_url = reverse_lazy('users:profile')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                carts = Cart(self.request)
                delivery_cost = 0 if form.cleaned_data.get('delivery_method') == 'pickup' else 500
                total_sum = carts.get_total_price() + delivery_cost
                payment_method = form.cleaned_data.get('payment_method')

                if payment_method == 'online':
                    payment_idempotence_key = str(uuid.uuid4())
                    return_url = reverse_lazy('users:profile')
                    payment = Payment.create({
                        "amount": {
                            "value": f"{total_sum:.2f}",
                            "currency": "RUB"
                        },
                        "confirmation": {
                            "type": "redirect",
                            "return_url": f"{settings.DOMAIN_NAME}{return_url}"
                        },
                        "capture": True,
                        "description": "Заказ на сайте HeyHockey!",
                    }, payment_idempotence_key)
                    confirmation_url = payment.confirmation.confirmation_url

                    create_order(user=user, form=form, carts=carts, payment_method=payment_method,
                                 delivery_cost=delivery_cost, total_sum=total_sum, payment_id=payment.id)
                    return redirect(confirmation_url)
                else:
                    order = create_order(user=user, form=form, carts=carts, payment_method=payment_method,
                                         delivery_cost=delivery_cost, total_sum=total_sum, payment_id='')
                    telegram(order)
                    messages.success(self.request, "Ваш заказ успешно создан!")
                    return super().form_valid(form)

        except Exception as e:
            logger.error(f'create_orders_view {e}')
            return redirect('carts:my_cart')


@method_decorator(csrf_exempt, name='dispatch')
class YookassaWebhookView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            print(f"Получен вебхук от YOOKASSA: {json_data}")

            if json_data.get("event") != "payment.succeeded":
                return HttpResponse(status=200)

            payment_object = json_data.get("object", {})
            payment_id = payment_object.get("id")

            if not payment_id:
                logger.error("payment_id не найден в metadata платежа")
                return HttpResponse(status=400)

            try:
                order = Order.objects.get(payment_id=payment_id)
            except Order.DoesNotExist:
                logger.error(f"Заказ с payment_id={payment_id} не найден")
                return HttpResponse(status=404)

            if payment_object.get("status") == "succeeded":
                order.is_paid = True
                order.save()
                telegram(order)

            return HttpResponse(status=200)

        except Exception as e:
            logger.error(f"Ошибка обработки вебхука: {e}")
            return HttpResponse(status=500)
