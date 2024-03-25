from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):
    return render(request, 'main/home.html')


def product(request):
    products = Product.objects.all()
    return render(request, 'main/product.html', {'products': products})