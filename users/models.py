from django.db import models
from django.contrib.auth.models import AbstractUser
from marketplace.models import Business


class User(AbstractUser):
    """
    Custom user model.
    Each user belongs to a business and has a role
    that determines permissions within the system.
    """

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('approver', 'Approver'),
        ('viewer', 'Viewer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )

