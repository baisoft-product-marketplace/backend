from django.db import models
from django.conf import settings


class Business(models.Model):
    """Represents a company that owns products and users."""
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Products belong to a business and go through an
    approval workflow before becoming public.
    """

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )

    created_at = models.DateTimeField(auto_now_add=True)

