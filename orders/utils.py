import telebot
from django.conf import settings
from orders.models import Order, OrderItem
import logging

logger = logging.getLogger(__name__)


def telegram(order):
    try:
        bot = telebot.TeleBot(settings.TELE_TOKEN)
        status = order.get_status_display()
        total_sum = order.summa
        address = order.delivery_address
        delivery = order.get_delivery_method_display()
        delivery_cost = order.delivery_cost
        phone = order.phone
        email = order.email
        customer_name = order.name
        comment = order.comment
        pay = order.get_payment_method_display()
        is_paid = '(Оплачен)' if order.is_paid else '(Не оплачен)'
        order_description = ''
        for item in order.items.all():
            order_description += item.product.name + ' ' + item.size + ' ' + str(item.quantity) + 'шт. ' + str(
                item.price) + '\n'
        order_description += 'Статус: ' + status + '\n'
        order_description += 'Оплата: ' + pay + is_paid + '\n'
        order_description += 'Доставка: ' + delivery + '\n'
        order_description += 'Стоимость доставки: ' + str(delivery_cost) + ' р' + '\n'
        order_description += 'Итого: ' + str(total_sum) + ' р' + '\n'
        order_description += 'Заказчик: ' + customer_name + '\n'
        order_description += 'Телефон: ' + phone + '\n' + 'Почта: ' + email + '\n'
        order_description += 'Адрес: ' + address + '\n'
        order_description += 'Комментарий: ' + comment + '\n'

        bot.send_message(settings.CHAT, f'Поступил новый заказ! #{order.id}' + '\n' + order_description)
    except Exception as e:
        logger.error(f'telegram {e}')


def create_order(**kwargs):
    try:
        delivery_cost =  kwargs['delivery_cost']
        total_sum = kwargs['total_sum']

        if kwargs['form'].cleaned_data.get('delivery_method') == 'pickup':
            address = ''
        else:
            address = (kwargs['form'].cleaned_data.get('city') + ' ' + kwargs['form'].cleaned_data.get(
                    'street') + ' д. ' + kwargs['form'].cleaned_data.get('house') + ' кв. ' +
                       kwargs['form'].cleaned_data.get('apartment'))

        order = Order.objects.create(
            user=kwargs['user'],
            name=kwargs['form'].cleaned_data.get('first_name') + ' ' + kwargs['form'].cleaned_data.get('last_name'),
            delivery_address=address,
            delivery_method=kwargs['form'].cleaned_data.get('delivery_method'),
            delivery_cost=delivery_cost,
            phone=kwargs['form'].cleaned_data.get('phone'),
            email=kwargs['form'].cleaned_data.get('email'),
            payment_method=kwargs['payment_method'],
            payment_id=kwargs['payment_id'],
            is_paid=False,
            status='created',
            comment=kwargs['form'].cleaned_data.get('comment'),
            summa=total_sum
        )

        for cart_item in kwargs['carts']:
            product = cart_item['product']
            name = product.name
            size = cart_item['size']
            price = cart_item['total_price']
            quantity = cart_item['quantity']

            OrderItem.objects.create(
                order=order,
                product=product,
                name=name,
                size=size,
                price=price,
                quantity=quantity,
            )
        kwargs['carts'].clear()
        return order

    except Exception as e:
        logger.error(f'create_order {e}')
