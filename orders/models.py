from django.contrib.auth import get_user_model
from django.db import models

from goods.models import Product

User = get_user_model()


class OrderitemQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.sum() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Онлайн оплата'),
        ('cash_on_delivery', 'Оплата при получении'),
    ]

    DELIVERY_METHOD_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьерская доставка'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Почта')

    delivery_method = models.CharField(
        max_length=50,
        choices=DELIVERY_METHOD_CHOICES,
        verbose_name='Способ доставки'
    )
    delivery_address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Адрес доставки'
    )

    delivery_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name='Стоимость доставки'
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты'
    )
    is_paid = models.BooleanField(default=False, verbose_name='Заказ оплачен')
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID платежа')

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус заказа'
    )

    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')
    summa = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Сумма')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ №{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    name = models.CharField(max_length=50, verbose_name='Название')
    size = models.CharField(max_length=50, verbose_name='Размер')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата продажи')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'

    def __str__(self):
        return f'{self.name}'

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)
