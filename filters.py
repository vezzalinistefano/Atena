import django_filters
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter

from shop.models import Course
from users.models import UserProfile


class CourseFilter(django_filters.FilterSet):

    class Meta:
        model = Course
        fields = {
            'title': ['contains'],
            'price': ['gt', 'lt'],
            'category': ['exact']
        }

