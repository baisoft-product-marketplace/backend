from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, PublicProductViewSet

app_name = "marketplace"

# DRF router for Product endpoints
router = DefaultRouter()
router.register("products", ProductViewSet, basename="product"),
router.register('public-products', PublicProductViewSet, basename='public-product')

urlpatterns = [
    path("", include(router.urls)),
]





