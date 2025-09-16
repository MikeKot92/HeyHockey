from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from goods.models import (Categories, League, Product, ProductImage,
                          ProductSize, Size, Team)


@admin.register(Size)
class SizeAdmin(ModelAdmin):
    list_display = ['name', ]


@admin.register(Categories)
class CategoriesAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Team)
class TeamAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['league', ]
    search_fields = ['name', ]


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 3


class ProductSizeInline(TabularInline):
    model = ProductSize
    extra = 6


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'status', 'price', 'discount']
    list_editable = ['status', 'price', 'discount']
    search_fields = ['name', 'description']
    list_filter = ['discount', 'status', 'category', 'team', ]
    autocomplete_fields = ['team']
    inlines = [ProductImageInline, ProductSizeInline, ]

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }


@admin.register(League)
class LeagueAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
