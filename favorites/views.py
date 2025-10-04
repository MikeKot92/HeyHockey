from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from goods.models import Product

from .favorites import Favorites


def view_favorites(request):
    """
    Отображает страницу избранных товаров пользователя.
    """
    context = {'title': 'Favorites'}
    return render(request, 'favorites/favorites.html', context)


def toggle_favorite(request, product_id):
    """
    Добавляет или удаляет товар из избранного.
    """
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)

    from_favorites_page = request.GET.get('from') == 'favorites'
    in_favorites = favorites.is_in_favorites(product.id)

    if in_favorites:
        favorites.remove(product.id)
    else:
        favorites.add(product.id)

    if from_favorites_page and in_favorites:
        badge_html = render_to_string(
            'favorites/favorites_badge.html',
            request=request
        )
        return HttpResponse(f'<div id="favorites-badge" hx-swap-oob="true">{badge_html}</div>')

    button_html = render_to_string(
        'favorites/favorite_button.html',
        {'product': product},
        request=request
    )

    badge_html = render_to_string(
        'favorites/favorites_badge.html',
        request=request
    )

    combined_html = f'{button_html}<div id="favorites-badge" hx-swap-oob="true">{badge_html}</div>'

    return HttpResponse(combined_html)
