from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    table_size = models.ImageField(upload_to='size_table/', blank=True, verbose_name='Таблица размеров')

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')

    class Meta:
        db_table = 'league'
        verbose_name = 'Лига'
        verbose_name_plural = 'Лиги'

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    league = models.ForeignKey(to=League, on_delete=models.CASCADE, verbose_name='Лига')

    class Meta:
        db_table = 'team'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')

    class Meta:
        db_table = 'size'
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS = ((1, 'в наличии'), (0, 'нет в наличии'),)
    image = models.ImageField(upload_to='goods_images/', blank=True)
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка в %')
    status = models.SmallIntegerField(default=0, choices=STATUS, verbose_name='Статус')
    video_src = models.URLField(blank=True, null=True, verbose_name='SRC-video')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE, verbose_name='Команда')
    size = models.ManyToManyField(to=Size, blank=True, through='ProductSize', verbose_name='Размер')

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'

    def get_size(self):
        return [ps.size.name for ps in self.productsize_set.all() if ps.availability]

    def get_absolute_url(self):
        return reverse('goods:product', kwargs={'product_slug': self.slug})

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер')
    availability = models.BooleanField(default=False, verbose_name='Наличие')

    class Meta:
        unique_together = ('product', 'size')
        verbose_name = 'Размер продукта'
        verbose_name_plural = 'Размеры продуктов'

    def __str__(self):
        return f'{self.product.name} - {self.size.name} ({self.availability})'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт'
    )
    image = models.ImageField(upload_to='goods_images/', verbose_name='Изображение')

    class Meta:
        db_table = 'product_image'
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'

    def __str__(self):
        return f'{self.product.name}'
