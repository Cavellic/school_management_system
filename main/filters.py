import django_filters
from .models import *
from django_filters import CharFilter

class StudentFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name = 'first_name', lookup_expr = 'icontains')
    class Meta:
        model = Student
        fields = ['first_name']

class StudentInFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name = 'first_name', lookup_expr = 'icontains')
    class Meta:
        model = Student
        fields = ['first_name'] 