from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create_orders/', views.CreateOrderView.as_view(), name='create_orders'),
    path('webhook/yookassa/', views.YookassaWebhookView.as_view(), name='yookassa_webhook'),
]
