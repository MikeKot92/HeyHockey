from django.core.cache import cache

class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

class CacheMixin:

    def set_get_cache(self, query, cache_name, cache_time):
        data = cache.get(cache_name)
        if not data:
            data = query
            cache.set(cache_name, data, cache_time)
        return data



