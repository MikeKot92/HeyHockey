
from django.views.generic import DetailView, ListView
from common.mixins import TitleMixin
from goods.forms import FilterForm
from goods.models import Product
import random
from goods.utils import q_search



class ProductListView(TitleMixin, ListView):
    title = 'Catalog'
    model = Product
    template_name = 'goods/catalog.html'
    context_object_name = 'products'
    paginate_by = 2
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset()

        team_slug = self.kwargs.get('team_slug')
        price = self.request.GET.get('price', None)
        discount = self.request.GET.get('discount', None)
        category = self.request.GET.get('category', None)
        size = self.request.GET.get('size', None)
        query = self.request.GET.get('q', None)

        if team_slug == 'all':
            products = queryset
        elif query:
            products = q_search(query)
        else:
            products = queryset.filter(team__slug=team_slug)

        if price and price != 'default':
            products = products.order_by(price)

        if discount:
            products = products.filter(discount__gt=0)

        if category:
            products = products.filter(category_id=category)

        if size:
            products = products.filter(productsize__size_id=size, productsize__availability=True).distinct()

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug_url'] = self.kwargs.get('team_slug')
        context['form'] = FilterForm(self.request.GET)
        return context


class ProductDetailView(TitleMixin, DetailView):
    title = 'Product'
    model = Product
    template_name = 'goods/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        sizes = product.get_size()
        status = product.status

        recommendation = list(Product.objects.filter(team=product.team).exclude(slug=product.slug))
        if len(recommendation) >= 5:
            recommendation = random.sample(recommendation, 5)
        else:
            recommendation = None

        context.update({
            'recommendation': recommendation,
            'sizes': sizes,
            'status': status,
        })

        return context


