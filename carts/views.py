from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from carts.cart import Cart
from goods.models import Product, Size


def cart_add(request, product_id):
    size_value = request.POST.get('size')
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    quantity = 1
    size = Size.objects.get(name=size_value)
    cart.add(product=product, size=size, quantity=quantity)
    messages.success(request, "Товар добавлен в корзину!")
    return redirect(request.META['HTTP_REFERER'])


def cart_change(request, product_id, num, size_id, quantity):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(Size, id=size_id)
    quantity += int(num)
    if quantity > 0:
        cart.update(product=product, size=size, quantity=quantity)
    return redirect(request.META['HTTP_REFERER'])


def cart_remove(request, product_id, size_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(Size, id=size_id)
    cart.remove(product=product, size=size)
    return redirect(request.META['HTTP_REFERER'])


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Корзина очищена")
    return redirect('cart:my_cart')


def my_cart(request):
    context = {'title': 'Cart'}
    return render(request, 'cart/cart.html', context)
