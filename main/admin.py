from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from main.models import Info, News, Review


@admin.register(Info)
class InfoAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ['user', 'rating', 'text_display', 'status', ]
    list_editable = ['status', ]

    def text_display(self, obj):
        text = obj.text[:50]
        return text

    text_display.short_description = 'Содержание'


@admin.register(News)
class InfoAdmin(ModelAdmin):
    list_display = ['name', 'created_at']

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }
