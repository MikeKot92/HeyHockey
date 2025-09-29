from goods.models import Product, Size


class Cart:
    """
    Класс для управления корзиной товаров в сессии пользователя.
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart', {})
        self.cart = cart
        self._products_cache = None
        self._sizes_cache = None

    def add(self, product, size, quantity=1):
        product_id = str(product.id)
        size_id = str(size.id)

        if product_id not in self.cart:
            self.cart[product_id] = {}

        if size_id not in self.cart[product_id]:
            self.cart[product_id][size_id] = {'quantity': 0}

        self.cart[product_id][size_id]['quantity'] += quantity
        self.save()

    def update(self, product, size, quantity):
        product_id = str(product.id)
        size_id = str(size.id)

        if product_id in self.cart and size_id in self.cart[product_id]:
            self.cart[product_id][size_id]['quantity'] = quantity
            self.save()

    def remove(self, product, size):
        product_id = str(product.id)
        size_id = str(size.id)

        if product_id in self.cart and size_id in self.cart[product_id]:
            del self.cart[product_id][size_id]

            if not self.cart[product_id]:
                del self.cart[product_id]

            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
        self._products_cache = None
        self._sizes_cache = None

    def _get_products_and_sizes(self):
        if self._products_cache is not None and self._sizes_cache is not None:
            return self._products_cache, self._sizes_cache

        product_ids = list(self.cart.keys())
        size_ids = []
        for product_data in self.cart.values():
            size_ids.extend(list(product_data.keys()))

        products = Product.objects.filter(id__in=product_ids)
        sizes = Size.objects.filter(id__in=size_ids)

        self._products_cache = {str(product.id): product for product in products}
        self._sizes_cache = {str(size.id): size for size in sizes}

        return self._products_cache, self._sizes_cache

    def __iter__(self):
        product_dict, size_dict = self._get_products_and_sizes()

        for product_id, sizes_data in self.cart.items():
            product = product_dict.get(product_id)
            if not product:
                continue

            for size_id, item_data in sizes_data.items():
                size = size_dict.get(size_id)
                if not size:
                    continue

                total_price = product.sell_price() * item_data['quantity']
                price_without_discount = product.price * item_data['quantity']

                yield {
                    'product': product,
                    'size': size,
                    'quantity': item_data['quantity'],
                    'total_price': total_price,
                    'price_without_discount': price_without_discount,
                }

    def get_total_quantity(self):
        return sum(
            item_data['quantity']
            for sizes_data in self.cart.values()
            for item_data in sizes_data.values()
        )

    def get_total_price(self):
        product_dict, _ = self._get_products_and_sizes()

        return sum(
            product_dict[product_id].sell_price() * item_data['quantity']
            for product_id, sizes_data in self.cart.items()
            for size_id, item_data in sizes_data.items()
            if product_id in product_dict
        )
