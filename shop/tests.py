from django.test import TestCase
from django.test import Client
from .models import Product, Order
import json

class ProductTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            price=99.99,
            description="Test description"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(float(self.product.price), 99.99)

    def test_api_get_products(self):
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Test Product")

    def test_api_create_order(self):
        order_data = {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "items": [
                {"product_id": self.product.id, "quantity": 2}
            ]
        }
        response = self.client.post(
            '/api/orders',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['customer_name'], "John Doe")
        self.assertEqual(float(data['total']), 199.98)

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['status'], 'ok')