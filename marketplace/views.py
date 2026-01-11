from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer
from users.models import User
from users.permissions import CanApproveProduct, CanEditProduct
from .filters import ProductFilter
from rest_framework import viewsets, permissions

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        """
        Business users can see their own products.
        Viewers can only see approved products.
        """
        user = self.request.user

        if user.role in {'admin', 'editor', 'approver'}:
            return Product.objects.filter(business=user.business).order_by('id')

        return Product.objects.filter(status='approved').order_by('id')

    def get_permissions(self):
        """
        Apply role-based permissions per action.
        """
        if self.action in {"create", "update", "partial_update"}:
            return [IsAuthenticated(), CanEditProduct()]

        if self.action == "approve":
            return [IsAuthenticated(), CanApproveProduct()]

        return super().get_permissions()

    def perform_create(self, serializer):
        # Automatically assign creator and business
        serializer.save(
            created_by=self.request.user,
            business=self.request.user.business
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """
        Approve a product (admin or approver only).
        """
        product = self.get_object()
        product.status = 'approved'
        product.save(update_fields=["status"])
        return Response(
            {"detail": "Product approved successfully."},
            status=status.HTTP_200_OK,
        )


class PublicProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public-facing products: only approved.
    """
    queryset = Product.objects.filter(status='approved')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  # anyone can view
