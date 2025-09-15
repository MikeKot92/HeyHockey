import telebot
from django.conf import settings


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

        bot.send_message(settings.CHAT, 'Поступил новый заказ!' + '\n' + order_description)
    except Exception as e:
        print(f'telegram {e}')
