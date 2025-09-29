from goods.models import Product


class Favorites:
    """
    Класс для управления избранными товарами пользователя через сессию.
    """
    def __init__(self, request):
        self.session = request.session
        favorites = self.session.get('favorites', [])
        self.favorites = favorites

    def add(self, product_id):
        if product_id not in self.favorites:
            self.favorites.append(product_id)
            self.save()

    def remove(self, product_id):
        if product_id in self.favorites:
            self.favorites.remove(product_id)
            self.save()

    def save(self):
        self.session['favorites'] = self.favorites
        self.session.modified = True

    def is_in_favorites(self, product_id):
        return product_id in self.favorites

    def get_total_quantity(self):
        return len(self.favorites)

    def __iter__(self):
        product_ids = self.favorites
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            yield product

