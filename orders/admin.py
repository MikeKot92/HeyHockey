from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget
from orders.models import Order, OrderItem


class OrderItemTabulareAdmin(TabularInline):
    model = OrderItem
    fields = 'product', 'price', 'quantity', 'size',
    search_fields = [
        'product',
        'name'
    ]
    autocomplete_fields = ['product']
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['order_display', 'name', 'price', 'quantity']
    search_fields = ['name', 'order']
    list_filter = ['created_at']
    autocomplete_fields = ['product']

    def order_display(self, obj):
        return str(obj.order.id)

    order_display.short_description = 'Заказ'


class OrderTabulareAdmin(TabularInline):
    model = Order
    fields = ('address', 'delivery', 'pay', 'status', 'summa', 'created_timestamp',)
    search_fields = [
        'product',
        'name',
        'created_timestamp',
    ]
    readonly_fields = ('created_timestamp',)
    extra = 0


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['order_id', 'user', 'name', 'is_paid', 'delivery_method', 'status', 'summa', 'created_at', ]
    list_filter = ['created_at', 'is_paid', 'status', 'delivery_method']
    search_fields = ['name', 'id', ]
    list_editable = ['status']

    def order_id(self, obj):
        return str(f'№ {obj.id}')

    order_id.short_description = 'Заказ'

    inlines = (OrderItemTabulareAdmin,)
