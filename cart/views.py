from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from cart.cart import Cart
from main.models import Product


# Create your views here.
def cart(request):
    cart = Cart(request)
    products = []
    total_cost = 0
    for id, item in cart.cart.items():
        product = Product.objects.get(id=id)
        products.append({
            'product': product,
            'quantity': item['quantity'],
            'total_price': product.cost * item['quantity'],
        })
        total_cost += product.cost * item['quantity']
    return render(request, 'cart/cart.html', {'cart': products, 'total_cost': total_cost})


def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add_product(product)

        return JsonResponse({'qty': sum(item['quantity'] for item in cart.cart.values())})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('quantity'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        cart.delete(product=product_id)

        messages.success(request, ("Item Deleted From Shopping Cart"))

        response = JsonResponse({'product': product_id})
        return response

    return JsonResponse({'error': 'Invalid request'}, status=400)
