from .cart import Cart

def carts(request):
    """
    Добавляет объект корзины в контекст всех шаблонов.
    """
    return {'carts': Cart(request)}