from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    business = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "status",
            "created_by",
            "business",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_by",
            "business",
            "status",
            "created_at",
            "updated_at",
        ]

