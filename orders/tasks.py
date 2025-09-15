from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order


@shared_task
def handle_order_task(order_id, created=False):
    try:
        instance = Order.objects.get(id=order_id)

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
    except Exception as e:
        print(f'handle_order {e}')
