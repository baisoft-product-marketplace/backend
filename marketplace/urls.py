from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, PublicProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('public/products', PublicProductViewSet, basename='public-products')

urlpatterns = router.urls
