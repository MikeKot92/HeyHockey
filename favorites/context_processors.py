from .favorites import Favorites


def favorites(request):
    """
    Контекст-процессор для добавления избранных товаров в контекст всех шаблонов.
    """
    return {
        'favorites': Favorites(request),
    }
