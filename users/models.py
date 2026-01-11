from django.contrib.auth.models import AbstractUser
from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        EDITOR = "editor", "Editor"
        APPROVER = "approver", "Approver"
        VIEWER = "viewer", "Viewer"

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )

    def __str__(self):
        return f"{self.username} [{self.role}]"

