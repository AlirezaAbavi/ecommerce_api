import django_filters

from .models import Product, Brand


class ProductFilter(django_filters.FilterSet):
    color = django_filters.CharFilter(field_name='quantities__color__code', lookup_expr='iexact', label='color')
    size = django_filters.CharFilter(field_name='quantities__size__code', lookup_expr='iexact', label='size')
    price = django_filters.RangeFilter(field_name='sell_price', label='price')
    brand = django_filters.filters.ModelMultipleChoiceFilter(
        field_name='brand',
        to_field_name='id',
        queryset=Brand.objects.all(),
    )
    STATUS_CHOICES = (
        (1, 'In Stock'),  # In Stock
    )
    status = django_filters.ChoiceFilter(field_name='quantities__status', choices=STATUS_CHOICES, label='status')

    class Meta:
        model = Product
        fields = {
            # 'status',
            # 'quantities__color__code': ['iexact'],
            # 'release_date': ['exact', 'year__gt'],
        }
