from django.forms import ModelForm, BooleanField
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group



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

class UserForm(ModelForm):
    check_box = BooleanField(label='Поставьте галочку для подтверждения')

    class Meta:
        model = User
        fields = '__all__'

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


