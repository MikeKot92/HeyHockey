from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .tasks import handle_order_task


@receiver(post_save, sender=Order)
def handle_order(sender, instance, created, **kwargs):
    """
    Отправляет задачу на обработку заказа после его сохранения.
    """
    transaction.on_commit(lambda: handle_order_task.delay(instance.id, created=created))
