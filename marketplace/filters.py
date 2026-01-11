import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    """
    Filter products by status and price range.
    """
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=Product.Status.choices
    )

    class Meta:
        model = Product
        fields = ["status", "min_price", "max_price"]
