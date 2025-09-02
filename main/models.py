from django.db import models


class Info(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Содержание', blank=True, null=True, )
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'info'
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'

    def __str__(self):
        return self.name


class News(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to='news/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Содержание', blank=True, null=True, )

    class Meta:
        db_table = 'news'
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
        ordering = ['-id']

    def __str__(self):
        return self.name
