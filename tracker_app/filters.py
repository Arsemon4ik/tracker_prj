import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'score': ['lt', 'gt'],
            'deadline': ['exact', 'day__gt'],
            'name': ['exact', 'icontains'],
        }