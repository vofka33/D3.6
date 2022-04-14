from django.forms import ModelForm, BooleanField
from .models import Post, Author, Category



class PostForm(ModelForm):
    check_box = BooleanField(label='Поставьте галочку для подтверждения')  # добавляем галочку, или же true-false поле

    class Meta:
        model = Post
        fields = ['title', 'postCategory', 'author', 'text', 'categoryType',
                  'check_box']  # не забываем включить галочку в поля иначе она не будет показываться на странице! 'author',