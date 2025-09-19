from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import logging
from .models import Order


logger = logging.getLogger(__name__)

@shared_task
def handle_order_task(order_id, created=False):
    try:
        instance = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.warning(f"Заказ с id={order_id} не найден. Возможно, задача была запущена до фиксации транзакции.")
        return f"Order {order_id} not found"

    try:
        status = instance.get_status_display()
        delivery_method = instance.get_delivery_method_display()
        payment_method = instance.get_payment_method_display()

        message = (
            f"Заказ №{instance.id}\n"
            f"Статус: {status}\n"
            f"Способ доставки: {delivery_method}\n"
            f"Адрес доставки: {instance.delivery_address}\n"
            f"Способ оплаты: {payment_method}\n"
            f"Оплата: {'Оплачен' if instance.is_paid else 'Не оплачен'}\n"
            f"Стоимость доставки: {instance.delivery_cost} руб.\n"
            f"Общая сумма: {instance.summa} руб.\n"
        )

        if created:
            subject = "Ваш заказ успешно создан!"
            email_message = (
                f"Здравствуйте, {instance.name}!\n\n"
                f"Ваш заказ успешно создан.\n\n"
                f"{message}"
            )
        else:
            subject = f"Обновление статуса заказа №{instance.id}"
            email_message = (
                f"Здравствуйте, {instance.name}!\n\n"
                f"Статус вашего заказа был обновлен.\n\n"
                f"{message}"
            )

        send_mail(
            subject=subject,
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )
        return "Email sent successfully"
    except Exception as e:
        logger.error(f"Ошибка в handle_order_task для заказа {order_id}: {e}")
        return f"Error: {e}"