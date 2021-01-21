import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['price_from', 'price_to']
