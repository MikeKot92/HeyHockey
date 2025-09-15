from django.shortcuts import get_object_or_404, redirect, render

from goods.models import Product

from .favorites import Favorites


def view_favorites(request):
    context = {'title': 'Favorites'}
    return render(request, 'favorites/favorites.html', context)


def toggle_favorite(request, product_id):
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)

    if favorites.is_in_favorites(product.id):
        favorites.remove(product.id)
    else:
        favorites.add(product.id)

    return redirect(request.META['HTTP_REFERER'])
