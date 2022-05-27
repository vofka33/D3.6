from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostDetailView, PostAddView, PostEditView, PostDeleteView, SearchList, EditUserProfile, CategoryList
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me, add_subscribe

urlpatterns = [
   path('', PostsList.as_view()),
   path('search/', SearchList.as_view(), name='search'),
   path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
   path('add/', PostAddView.as_view(), name='post_add'), 
   path('<int:pk>/add', PostEditView.as_view(), name='post_edit'),
   path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
   path('<int:pk>/add', PostEditView.as_view(), name='post_edit'),
   path('user_update/', EditUserProfile.as_view(), name='user_update'),
   # path('login/', LoginView.as_view(template_name='news/login.html'), name='login'),
   # path('logout/', LogoutView.as_view(template_name='news/logout.html'), name='logout'),
   path('accounts/', include('allauth.urls')),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('category/', CategoryList.as_view(), name='category'),
   path('<int:pk>/add_subscribe', add_subscribe, name='subscribe'),
   # path('', IndexView.as_view()),
   ]