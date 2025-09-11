from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.conf import settings
from .models import Order


@receiver(post_save, sender=Order,)
def handle_order_completed(sender, instance, created, **kwargs):
    try:
        message = (
            f"Заказ №{instance.id}\n"
            f"Статус: {instance.status}\n"
            f"Общая сумма: {instance.summa} руб.\n"
            f"Оплата: {'Оплачен' if instance.is_paid else 'Не оплачен'}\n"
            f"Адрес доставки: {instance.delivery_address}\n"
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
        print(f'handle_order_completed {e}')