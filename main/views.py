from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView

from common.mixins import TitleMixin
from goods.models import Product
from main.models import Info, News, Review


class IndexTemplateView(TitleMixin, TemplateView):
    title = 'Home'
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.all().order_by('-id')
        context['popular_products'] = queryset[:4]
        return context


class NewsTemplateView(TitleMixin, TemplateView):
    title = 'News'
    template_name = 'main/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all().order_by('-id')
        return context


class InfoDetailView(TitleMixin, DetailView):
    title = 'Info'
    model = Info
    template_name = 'main/info.html'
    context_object_name = 'info'
    slug_url_kwarg = 'info_slug'


class ReviewTemplateView(TitleMixin, TemplateView):
    title = 'Review'
    model = Review
    template_name = 'main/review.html'
    success_message = "Ваш отзыв будет опубликован после модерации!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_pub_all'] = Review.objects.filter(status='Опубликован').order_by('-id').select_related('user')
        return context

    def post(self, request, *args, **kwargs):
        print(kwargs)
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        user_id = request.user.id
        Review.objects.create(user_id=user_id, text=text, rating=rating)
        messages.success(request, "Ваш отзыв будет опубликован после модерации!")
        return redirect('main:review')
