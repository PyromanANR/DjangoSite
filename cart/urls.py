from django.contrib import admin
from django.urls import path, include

from cart import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('cart_add', views.cart_add, name='cart_add')
]
