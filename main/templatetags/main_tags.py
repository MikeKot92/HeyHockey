from django import template

from main.models import Info

register = template.Library()


@register.simple_tag()
def tag_info():
    """
    Возвращает все информационные страницы.
    """
    info = Info.objects.all()
    data = {'info': info}
    return data
