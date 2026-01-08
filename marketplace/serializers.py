from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for product CRUD operations.
    """

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_by', 'business', 'status']
