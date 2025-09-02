from django import template
from django.utils.http import urlencode
from main.models import Info

register = template.Library()




@register.simple_tag()
def tag_info():
    info = Info.objects.all()
    data = {'info': info}
    return data

