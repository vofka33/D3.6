from django.forms import ModelForm, BooleanField
from django import forms
from .models import *



class PostForm(ModelForm):
    check_box = BooleanField(label='Поставьте галочку для подтверждения')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Выберите автора"



    class Meta:
        model = Post
        fields = ['title' , 'postCategory', 'author', 'text', 'categoryType',
                  'check_box']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 120, 'rows': 10}),
        }




