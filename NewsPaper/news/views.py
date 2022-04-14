from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm



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


class PostAddView(CreateView):
    template_name = 'news/post_add.html'
    form_class = PostForm


class PostEditView(UpdateView):
    template_name = 'news/post_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
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
    

