from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class MarketplaceProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='marketplace_profiles'
    )
    business = models.ForeignKey(
        'marketplace.Business',  # string reference
        on_delete=models.CASCADE,
        related_name='marketplace_profiles'
    )

class Business(models.Model):
    """
    Represents a business entity.
    Businesses can have multiple users and products.
    """
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Represents a product in the marketplace.
    Products belong to a business and have an approval workflow.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    business = models.ForeignKey(
        'marketplace.Business',
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.business.name})"

    class Meta:
        permissions = [
            ('can_approve_product', 'Can approve products'),
        ]
