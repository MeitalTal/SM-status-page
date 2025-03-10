import django_filters
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from statuspage.filtersets import BaseFilterSet
from utilities.filters import ContentTypeFilter
from .models import *


__all__ = (
    'ContentTypeFilterSet',
    'ObjectChangeFilterSet',
)


class ObjectChangeFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    time = django_filters.DateTimeFromToRangeFilter()
    changed_object_type = ContentTypeFilter()
    user_id = django_filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all(),
        label='User (Id)',
    )
    user = django_filters.ModelMultipleChoiceFilter(
        field_name='user__username',
        queryset=User.objects.all(),
        to_field_name='username',
        label='User name',
    )

    class Meta:
        model = ObjectChange
        fields = [
            'id', 'user', 'user_name', 'request_id', 'action', 'changed_object_type_id', 'changed_object_id',
            'object_repr',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(user_name__icontains=value) |
            Q(object_repr__icontains=value)
        )


#
# ContentTypes
#

class ContentTypeFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(app_label__icontains=value) |
            Q(model__icontains=value)
        )
