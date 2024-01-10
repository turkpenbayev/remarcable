import django_filters
from django_filters import ModelMultipleChoiceFilter, widgets
from .models import Tag, Category, Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains', label='Product Name')

    tags = ModelMultipleChoiceFilter(
        field_name='tags',
        queryset=Tag.objects.all().distinct(),
        label='Tag'
    )

    category = ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all().distinct(),
        label='Category'
    )

    class Meta:
        model = Product
        fields = ['name', 'tags', 'category']
