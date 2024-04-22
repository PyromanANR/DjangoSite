import decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product
import os


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Electronics')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Product',
            cost=decimal.Decimal('999.99'),
            category=self.category,
            description='This is a test product',
            image=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image/test/277546396.jpg')
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Product')

    def test_product_cost(self):
        self.assertEqual(self.product.cost, decimal.Decimal('999.99'))

    def test_product_category(self):
        self.assertEqual(self.product.category, self.category)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Product',
            cost=decimal.Decimal('999.99'),
            category=self.category,
            description='This is a test product',
            image=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image/test/277546396.jpg')
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_product_view(self):
        response = self.client.get(reverse('product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/product.html')
        self.assertContains(response, 'Product')

    def test_buy_product_view(self):
        response = self.client.get(reverse('buy_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/buy_product.html')
        self.assertContains(response, 'Product')
