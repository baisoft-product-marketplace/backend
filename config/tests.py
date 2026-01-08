from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from marketplace.models import Business,  Product
from users.models import User

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.business = Business.objects.create(name='TestBiz')
        self.user = User.objects.create_user(username='testuser', password='pass', business=self.business, role='editor')
        self.product = Product.objects.create(name='TestProd', description='Desc', price=10, business=self.business, created_by=self.user)

    def test_create_product(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'NewProd', 'description': 'Desc', 'price': 20}
        response = self.client.post('/marketplace/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.filter(business=self.business).count(), 2)  # FK check

    def test_approve_product(self):
        approver = User.objects.create_user(username='approver', password='pass', business=self.business, role='approver')
        self.client.force_authenticate(user=approver)
        response = self.client.post(f'/marketplace/products/{self.product.id}/approve/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.status, 'approved')