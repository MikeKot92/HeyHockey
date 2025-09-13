from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import News


User = get_user_model()


@receiver(post_save, sender=News)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        try:
            subscribers = User.objects.filter(subscribe_to_newsletter=True)

            if subscribers.exists():
                subject = f"Новости HeyHockey! - {instance.name}"

                html_content = render_to_string('newsletter.html', {
                    'news': instance,
                    'site_name': 'HeyHockey!',
                    'site_url': settings.DOMAIN_NAME
                })

                text_content = f"""
                            Новая новость на сайте HeyHockey!
                            
                            {instance.name}
                            
                            {instance.description}
                            
                            Читать полностью: {settings.DOMAIN_NAME}
                            
                            ---
                            С уважением,
                            Команда HeyHockey!
                """
                sent_count = 0
                for subscriber in subscribers:
                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[subscriber.email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    sent_count += 1

        except Exception as e:
            print(f"Ошибка при отправке рассылки новости: {e}")