from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from carts.cart import Cart
from goods.models import Product, Size


def cart_add(request, product_id):
    """
    Добавляет товар в корзину пользователя.
    """
    size_value = request.POST.get('size')
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    quantity = 1
    size = Size.objects.get(name=size_value)
    cart.add(product=product, size=size, quantity=quantity)

    cart_html = render_to_string('cart/cart_count_badge.html', request=request)
    return HttpResponse(cart_html)




def cart_change(request, product_id, num, size_id, quantity):
    """
    Изменяет количество товара в корзине.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(Size, id=size_id)
    quantity += int(num)
    if quantity > 0:
        cart.update(product=product, size=size, quantity=quantity)
    return redirect(request.META['HTTP_REFERER'])


def cart_remove(request, product_id, size_id):
    """
    Удаляет товар из корзины.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(Size, id=size_id)
    cart.remove(product=product, size=size)
    return redirect(request.META['HTTP_REFERER'])


def cart_clear(request):
    """
    Удаляет все товары из корзины.
    """
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Корзина очищена")
    return redirect('cart:my_cart')


def my_cart(request):
    """
    Отображает страницу корзины пользователя.
    """
    context = {'title': 'Cart'}
    return render(request, 'cart/cart.html', context)
