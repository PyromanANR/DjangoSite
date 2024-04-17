from django.contrib import admin
from django.urls import path, include

from cart import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('cart_add', views.cart_add, name='cart_add'),
    path('cart_delete', views.cart_delete, name='cart_delete'),
    path('cart_update', views.cart_update, name='cart_update')
]
