import django_filters

from .models import *

class ChampionsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    role = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Champions
        fields= '__all__'
        exclude= ['picture']
