from goods.models import Product, Size


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart', {})
        self.cart = cart

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

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            for size_id, item_data in self.cart[str(product.id)].items():
                size = Size.objects.get(id=size_id)
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
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        product_dict = {str(product.id): product for product in products}
        return sum(
            product_dict[product_id].sell_price() * item_data['quantity']
            for product_id, sizes_data in self.cart.items()
            for size_id, item_data in sizes_data.items()
            if product_id in product_dict
        )

    # def get_delivery_cost(self):
    #     return 500 if self.get_total_price() < 5000 else 0
    #
    # def get_total_price_with_delivery(self):
    #     return self.get_total_price() + self.get_delivery_cost()