from django_filters import rest_framework as filters

from page.models import Page


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    ...


class PageFilter(filters.FilterSet):
    uuid = filters.UUIDFilter(field_name='uuid', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title')
    tags = CharFilterInFilter(field_name='tags__name', lookup_expr='in')

    class Meta:
        model = Page
        fields = ['uuid', 'title', 'tags']
