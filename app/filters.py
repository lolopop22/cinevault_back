import django_filters
from .models import Movie


class MovieFilter(django_filters.FilterSet):
    categories = django_filters.CharFilter(
        field_name="categories__name", lookup_expr="icontains"
    )

    class Meta:
        model = Movie
        fields = ["categories"]
