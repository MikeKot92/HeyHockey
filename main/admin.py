from django.contrib import admin

from main.models import Info, News


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}




admin.site.register(News)
