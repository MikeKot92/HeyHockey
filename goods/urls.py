from django.urls import path

from goods import views

app_name='goods'

urlpatterns = [
    path('search/', views.ProductListView.as_view(), name='search'),
    path('<slug:team_slug>', views.ProductListView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product'),
]