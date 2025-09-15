from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import News
from .tasks import send_newsletter_task


@receiver(post_save, sender=News)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        send_newsletter_task.delay(instance.id)
