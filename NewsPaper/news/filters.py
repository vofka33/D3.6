from django_filters import FilterSet, DateFilter # DateFilter импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Category, Author
from django import forms


class PostFilter(FilterSet):
    date = DateFilter(
        field_name="dateCreation",
        lookup_expr="gte",
        label="Дата от",
        widget=forms.DateInput(attrs={'type': 'date'})            
            )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            # 'dateCreation': ['gte'],
            'author': ['exact'],
            'rating': ['gte']
        }

            




