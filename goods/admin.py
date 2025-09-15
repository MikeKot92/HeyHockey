from django.contrib import admin

from goods.models import (Categories, League, Product, ProductImage,
                          ProductSize, Size, Team)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['league', ]
    search_fields = ['name', ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 6


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'status', 'price', 'discount']
    list_editable = ['status', 'price', 'discount']
    search_fields = ['name', 'description']
    list_filter = ['discount', 'status', 'category', 'team', ]
    autocomplete_fields = ['team']
    inlines = [ProductImageInline, ProductSizeInline, ]


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
