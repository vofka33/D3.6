from django_filters import FilterSet  # DateFilter импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Category, Author


class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Post

        fields = {
            'title': ['icontains'],
            'dateCreation': ['gte'],
            'author': ['exact'],
            'rating': ['gte']
        }

# class PostFilter(FilterSet):
#     time_in = DateFilter(
#         lookup_expr='gt',
#         widget=django.forms.DateInput(
#             attrs={
#                 'type': 'date'
#             }
#         )
#     )
#     class Meta:
#         model = Post
#         fields = {
#             'heading': ['icontains'],
#             'author__name': ['exact'],
#             'category': ['exact'],
#         }