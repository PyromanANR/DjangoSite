from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from main.models import Product


# Create your views here.
def cart(request):
    return None


def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add_product(product)

        return JsonResponse({'qty': sum(item['quantity'] for item in cart.cart.values())})

    return JsonResponse({'error': 'Invalid request'}, status=400)