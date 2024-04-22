from django.contrib import admin
from django.urls import path, include

from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product', views.product, name='product'),
    path('product/<int:product_id>/buy', views.buy_product, name='buy_product'),
]
