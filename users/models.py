from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Фото')
    subscribe_to_newsletter = models.BooleanField(default=True, verbose_name='Согласие на рассылку')

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and hasattr(self.image, 'path'):
            try:
                img = Image.open(self.image.path)

                if img.height > 100 or img.width > 100:
                    new_img = (100, 100)
                    img.thumbnail(new_img)
                    img.save(self.image.path)
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"Ошибка при обработке изображения: {e}")
