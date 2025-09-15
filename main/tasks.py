from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import News

User = get_user_model()


@shared_task
def send_newsletter_task(news_id):
    try:
        instance = News.objects.get(id=news_id)

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
