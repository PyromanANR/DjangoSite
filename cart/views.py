from django.shortcuts import render
import io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from cart.cart import Cart
from main.models import Product
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.utils import timezone



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


def cart_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    p = canvas.Canvas(buffer)
    p.setFont('DejaVuSans', 12)

    # Get the cart from the session
    cart = Cart(request)

    # Draw things on the PDF. Here's where the PDF generation happens.
    p.drawString(100, 100, "Your Cart")
    p.drawString(100, 80, "Date: " + timezone.now().strftime("%Y-%m-%d %H:%M:%S"))

    y = 60
    ids = []
    total_cost = 0
    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=item['id'])  # Fetch the product details
        ids.append(item['id'])
        p.drawString(100, y, f"{product.name}: {item['quantity']} x {product.cost} = {product.cost * item['quantity']}")
        total_cost += product.cost * item['quantity']
        y -= 20

    p.drawString(100, y, f"Total price: {total_cost}")
    for i in ids:
        cart.delete(product=i)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='cart.pdf')