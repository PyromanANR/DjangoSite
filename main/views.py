from django.shortcuts import render, get_object_or_404
from .models import Product, Category


# Create your views here.
def home(request):
    return render(request, 'main/home.html')


def product(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/product.html', {'products': products, 'categories': categories})


def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'main/buy_product.html', {'product': product})
