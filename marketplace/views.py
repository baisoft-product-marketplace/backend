from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
from .permissions import CanApproveProduct


class ProductViewSet(viewsets.ModelViewSet):
    """
    Internal product management.
    Users can create and edit products within their business.
    """

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only see products belonging to their business
        return Product.objects.filter(
            business=self.request.user.business
        )

    def perform_create(self, serializer):
        # Attach ownership automatically
        serializer.save(
            created_by=self.request.user,
            business=self.request.user.business
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[CanApproveProduct]
    )
    def approve(self, request, pk=None):
        """
        Approves a product.
        Only accessible to users with approval permission.
        """
        product = self.get_object()
        product.status = 'approved'
        product.save()
        return Response({'detail': 'Product approved successfully'})

class PublicProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public-facing product listing.
    Only approved products are exposed.
    """

    queryset = Product.objects.filter(status='approved')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

