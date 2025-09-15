from django.urls import path

from carts import views

app_name = 'carts'

urlpatterns = [
    path('cart-add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart-change/<int:product_id>/<int:size_id>/<int:quantity>/<str:num>/', views.cart_change, name='cart_change'),
    path('cart-remove/<int:product_id>/<int:size_id>/', views.cart_remove, name='cart_remove'),
    path('cart-clear/', views.cart_clear, name='cart_clear'),
    path('my-cart/', views.my_cart, name='my_cart'),

]
