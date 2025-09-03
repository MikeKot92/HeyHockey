
from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('info/<slug:info_slug>/', views.InfoDetailView.as_view(), name='info'),
    path('news/', views.NewsTemplateView.as_view(), name='news'),
    path('review/', views.ReviewTemplateView.as_view(), name='review'),
]
