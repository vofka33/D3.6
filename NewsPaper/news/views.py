from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category, PostCategory
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
from django.dispatch import receiver
from django.core.mail import mail_managers
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from .tasks import send_post_create_celery
import logging

logger = logging.getLogger(__name__)
logger.warning('!WARNING!')
logger.info('!INFO!')
logger.error('!ERROR!')
logger.critical('!CRITICAL!')

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

    def notify_post_create_celery(self, request):
        for cat_id in instance.postCategory.all():

            users = Category.objects.filter(name=cat_id).values("subscribers")
            # print('user', users)
            link = ''.join(['http://', get_current_site(None).domain, ':8000/'])
            send_post_create_celery(users, link)
            



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


class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category_list.html'
    context_object_name = 'category_list'
    


@login_required
def add_subscribe(request, pk):
    a = request.user
    a.save()
    b = Category.objects.get(id=pk)
    b.subscribers.add(a)
    return redirect('/news/')



@receiver(m2m_changed, sender=PostCategory)
def notify_post_create(sender, instance, *args, **kwargs):
    for cat_id in instance.postCategory.all():
        
        users = Category.objects.filter(name=cat_id).values("subscribers")
        # print('user', users)
        link = ''.join(['http://', get_current_site(None).domain, ':8000/'])
        for user_id in users:
            send_mail(
                subject=f'Новая публикация - "{instance.title}"',
                message=f"Здравствуй, {User.objects.get(pk=user_id['subscribers']).username}. "
                        f'Новая публикация в вашем любимом разделе! \n"{instance.text[:50]}..."\n'
                        f'Пройдите по ссылке {link} что бы прочитать на нашем сайте.',
                from_email='imya6301@yandex.ru',
                recipient_list=[User.objects.get(pk=user_id['subscribers']).email]
            )


