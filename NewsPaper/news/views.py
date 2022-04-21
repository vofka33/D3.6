from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin



class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    ordering = '-dateCreation'
    template_name = 'post_list.html'
    context_object_name = 'posts'
    # queryset = Post.objects.filter(categoryType='NU')
    paginate_by = 5

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter()
        }

  
class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


class PostAddView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'news/post_add.html'
    form_class = PostForm


class PostEditView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post')
    template_name = 'news/post_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post'
    ordering = ['-dateCreation', 'author']
    paginate_by = 5


    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter()
        }
    

class EditUserProfile(LoginRequiredMixin, UpdateView):
    template_name = 'news/user_update.html'
    form_class = UserForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context



@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')