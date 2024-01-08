from django_filters import rest_framework as filters

from apps.cars.choices.body_type_choices import BodyTypeChoices
from apps.cars.models import CarModel


class CarFilter(filters.FilterSet):
    # yearLt = filters.NumberFilter('year', 'lt')
    # year_gt = filters.NumberFilter('year', 'gt')
    # year = filters.RangeFilter('year')
    # brand_contains = filters.CharFilter('brand', 'icontains')
    # body = filters.ChoiceFilter('body', choices=BodyTypeChoices.choices)
    order = filters.OrderingFilter(
        fields=(
            'id',
            'brand',
            'year',
            'price',
            'body',
            'crated_at',
            'updated_at'
        )
    )

    class Meta:
        model = CarModel
        fields = {
            'year': ('lt', 'lte', 'gt', 'gte'),
            'price': ('lt', 'lte', 'gt', 'gte'),
            'body': ('istartswith', 'iendswith', 'icontains'),
            'brand': ('istartswith', 'iendswith', 'icontains')
        }
