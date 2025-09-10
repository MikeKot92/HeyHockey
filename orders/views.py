from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.conf import settings

from carts.cart import Cart
from common.mixins import TitleMixin
from orders.forms import FormOrder
from orders.models import Order, OrderItem
import uuid

from yookassa import Configuration, Payment

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


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

                order = Order.objects.create(
                    user=user,
                    name=form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name'),
                    delivery_address=form.cleaned_data.get('city') + ' ' + form.cleaned_data.get(
                        'street') + ' ' + form.cleaned_data.get('house') + ' ' + form.cleaned_data.get('apartment'),
                    delivery_method=form.cleaned_data.get('delivery_method'),
                    delivery_cost=delivery_cost,
                    phone=form.cleaned_data.get('phone'),
                    email=form.cleaned_data.get('email'),
                    payment_method=payment_method,
                    is_paid=False,
                    status='created',
                    comment=form.cleaned_data.get('comment'),
                    summa=total_sum
                )

                for cart_item in carts:
                    product = cart_item['product']
                    name = product.name
                    size = cart_item['size']
                    price = cart_item['total_price']
                    quantity = cart_item['quantity']

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        name=name,
                        size=size,
                        price=price,
                        quantity=quantity,
                    )

                carts.clear()

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
                            "return_url": f"{settings.DOMAIN_NAME}/{return_url}"
                        },
                        "capture": True,
                        "description": f"Заказ №{order.id} на сайте HeyHockey!",
                        "metadata": {
                            "order_id": order.id
                        },
                    }, payment_idempotence_key)
                    confirmation_url = payment.confirmation.confirmation_url
                    order.payment_id = payment.id
                    order.save()
                    return redirect(confirmation_url)
                else:
                    messages.success(self.request, f"Ваш заказ №{order.id} успешно создан!")
                    return super().form_valid(form)

        except Exception as e:
            print(f'create_orders {e}')
            return redirect('carts:my_cart')



