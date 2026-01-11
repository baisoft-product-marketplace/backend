from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User, Business
from marketplace.models import Product


class ProductTests(APITestCase):
    def setUp(self):
        self.business = Business.objects.create(name="Biz")
        self.user_editor = User.objects.create_user(
            username="editor",
            password="pass123",
            role=User.Role.EDITOR,
            business=self.business,
        )
        self.user_approver = User.objects.create_user(
            username="approver",
            password="pass123",
            role=User.Role.APPROVER,
            business=self.business,
        )
        self.client.force_authenticate(user=self.user_editor)

    def test_create_product(self):
        """
        Editors can create products.
        """
        url = reverse("marketplace:product-list")
        data = {"name": "Test Product", "description": "Desc", "price": 10.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Test Product")

    def test_product_list_limited_to_business(self):
        """
        Users can only see products from their business.
        """
        other_business = Business.objects.create(name="OtherBiz")
        Product.objects.create(
            name="Other Product",
            description="Desc",
            price=5.0,
            created_by=self.user_editor,
            business=other_business
        )
        url = reverse("marketplace:product-list")
        response = self.client.get(url)
        for item in response.data:
            self.assertEqual(item["business"], str(self.business))
  
    def test_permission_denied_for_approval_by_editor(self):
        """
        Editors cannot approve products.
        """
        product = Product.objects.create(
            name="P1",
            description="D",
            price=5,
            created_by=self.user_editor,
            business=self.business,
        )
        url = reverse("marketplace:product-approve", args=[product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_approve_product_as_approver(self):
        """
        Approvers can approve products.
        """
        product = Product.objects.create(
            name="P2",
            description="Desc",
            price=5,
            created_by=self.user_editor,
            business=self.business,
        )
        self.client.force_authenticate(user=self.user_approver)
        url = reverse("marketplace:product-approve", args=[product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        product.refresh_from_db()
        self.assertEqual(product.status, Product.Status.APPROVED)

