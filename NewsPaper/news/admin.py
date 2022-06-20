from django.contrib import admin
from .models import Category, Post


class NewsAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('pk', 'title', 'dateCreation', 'categoryType', 'rating') # генерируем список имён всех полей для более красивого отображения
    list_filter = ('title', 'dateCreation', 'categoryType', 'rating')
    search_fields = ('title', 'dateCreation', 'categoryType', 'rating')

# Register your models here.
admin.site.register(Category)
admin.site.register(Post, NewsAdmin)
