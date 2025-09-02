from django.views.generic import TemplateView, DetailView
from common.mixins import TitleMixin
from main.models import Info, News


class IndexTemplateView(TitleMixin, TemplateView):
    title = 'Home'
    template_name = 'main/index.html'


class NewsTemplateView(TitleMixin, TemplateView):
    title = 'News'
    template_name = 'main/news.html'
    extra_context = {
        'news': News.objects.all()
    }


class InfoDetailView(TitleMixin, DetailView):
    title = 'Info'
    model = Info
    template_name = 'main/info.html'
    context_object_name = 'info'
    slug_url_kwarg = 'info_slug'