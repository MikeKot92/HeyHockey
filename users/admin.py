from django.contrib import admin
from django.contrib.auth import get_user_model
from unfold.admin import ModelAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', ]
    search_fields = ['username', 'first_name', 'last_name', 'email', ]
