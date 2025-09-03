from django.contrib import admin

from main.models import Info, News, Review


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'text_display', 'status', ]
    list_editable = ['status',]

    def text_display(self, obj):
        text = obj.text[:50]
        return text

    text_display.short_description = 'Содержание'


admin.site.register(News)
