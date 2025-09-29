from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Info(models.Model):
    """
    Модель информационной страницы.
    """
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Содержание')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'info'
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'

    def __str__(self):
        return self.name


class News(models.Model):
    """
    Модель новости.
    """
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to='news/', verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Содержание', )
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        db_table = 'news'
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Модель отзыва.
    """
    STATUS_CHOICES = (('Модерация', 'Модерация'), ('Опубликован', 'Опубликован'),)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Отзыв')
    rating = models.IntegerField(verbose_name='Рейтинг')
    status = models.CharField(max_length=100, default='Модерация', choices=STATUS_CHOICES, verbose_name='Статус')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'review'
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.user} | {self.rating}'
