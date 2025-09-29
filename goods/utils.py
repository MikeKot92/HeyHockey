from django.db.models import Q

from goods.views import Product


def q_search(query):
    """
    Выполняет поиск товаров по названию и описанию.
    """
    keyword = [word for word in query.split() if len(word) > 2]
    q_objects = Q()

    for token in keyword:
        q_objects |= Q(description__icontains=token)
        q_objects |= Q(description__icontains=token.title())
        q_objects |= Q(name__icontains=token)
        q_objects |= Q(name__icontains=token.title())
    return Product.objects.filter(q_objects)
