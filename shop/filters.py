import django_filters

from shop.models import Course


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            'title': ['contains'],
            'price': ['gt', 'lt'],
            'category': ['exact']
        }
