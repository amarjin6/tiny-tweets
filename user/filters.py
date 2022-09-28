from django_filters import rest_framework as filters

from user.models import User


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username')

    class Meta:
        model = User
        fields = ['username']
