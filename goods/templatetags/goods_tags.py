from django import template
from django.utils.http import urlencode

from goods.models import League

register = template.Library()


@register.simple_tag()
def tag_teams():
    """
    Возвращает все лиги с предзагруженными командами.
    """
    league = League.objects.all().prefetch_related('team_set')
    data = {'league': league}
    return data


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    """
    Обновляет параметры GET-запроса и возвращает строку параметров.
    """
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
