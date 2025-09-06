from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('my-favorite/', views.view_favorites, name='view_favorites'),
    path('toggle-favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
]