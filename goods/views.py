from django.views.generic import DetailView, ListView

from common.mixins import TitleMixin
from goods.forms import FilterForm
from goods.models import Product
from goods.utils import q_search


class ProductListView(TitleMixin, ListView):
    title = 'Catalog'
    model = Product
    template_name = 'goods/catalog.html'
    context_object_name = 'products'
    paginate_by = 8
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset().distinct()

        team_slug = self.kwargs.get('team_slug')
        price = self.request.GET.get('price', None)
        discount = self.request.GET.get('discount', None)
        categories = self.request.GET.getlist('category')
        sizes = self.request.GET.getlist('size')
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

        if categories:
            products = products.filter(category_id__in=categories)

        if sizes:
            products = products.filter(productsize__size_id__in=sizes, productsize__availability=True).distinct()

        return products.distinct()

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

    def get_queryset(self):
        return Product.objects.select_related(
            'team',
            'team__league',
            'category'
        ).prefetch_related(
            'images',
            'productsize_set__size'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        sizes = product.get_size()
        status = product.status
        recommendation = list(Product.objects.select_related('team').filter(
            team=product.team
        ).exclude(
            slug=product.slug
        )[:4])
        context.update({
            'recommendation': recommendation if len(recommendation) >= 4 else None,
            'sizes': sizes,
            'status': status,
        })

        return context
