import os
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from main.models import Category, Product
from .cart import Cart
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
import decimal
import json


def dummy_get_response(request):
    return None


class CartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Electronics')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.product = Product.objects.create(
            name='iPhone 13',
            cost=decimal.Decimal('999.99'),
            category=self.category,
            description='The latest iPhone model.',
            image=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image/test/277546396.jpg')
        )
        self.request = self.factory.get('/')
        self.request.user = self.user
        middleware = SessionMiddleware(dummy_get_response)
        middleware.process_request(self.request)
        self.request.session.save()
        self.cart = Cart(self.request)

    def test_add_product(self):
        self.cart.add_product(self.product, 1)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart.cart[str(self.product.id)]['quantity'], 1)

    def test_delete_product(self):
        self.cart.add_product(self.product, 1)
        self.cart.delete(self.product.id)
        self.assertEqual(len(self.cart), 0)

    def test_update_product(self):
        self.cart.add_product(self.product, 1)
        self.cart.update(self.product.id, 2)
        self.assertEqual(self.cart.cart[str(self.product.id)]['quantity'], 2)


class CartViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='iPhone 13',
            cost=decimal.Decimal('999.99'),
            category=self.category,
            description='The latest iPhone model.',
            image='path/to/image.jpg'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_cart_view(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')

    def test_cart_add_view(self):
        response = self.client.post(reverse('cart_add'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 1)

    def test_cart_update_view(self):
        self.client.post(reverse('cart_add'), {'product_id': self.product.id})
        response = self.client.post(reverse('cart_update'), {
            'product_id': self.product.id,
            'quantity': 2,
            'action': 'post'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 2)

    def test_cart_delete_view(self):
        self.client.post(reverse('cart_add'), {'product_id': self.product.id})
        response = self.client.post(reverse('cart_delete'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['product'], str(self.product.id))

    def test_cart_pdf_view(self):
        self.client.post(reverse('cart_add'), {'product_id': self.product.id})
        response = self.client.post(reverse('cart_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="cart.pdf"')
