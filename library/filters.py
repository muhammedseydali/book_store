from django_filters import rest_framework as filters
from .models import Book


# We create filters for each field we want to be able to filter on
class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(lookup_expr='icontains')
    category = filters.CharFilter(lookup_expr='icontains')
    year_of_publication = filters.NumberFilter()
    created_at = filters.NumberFilter(field_name='year', lookup_expr='gt')
    updated_at = filters.NumberFilter(field_name='year', lookup_expr='lt')
    creator = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'year_of_publication', 'created_at', 'updated_at', 'creator']

