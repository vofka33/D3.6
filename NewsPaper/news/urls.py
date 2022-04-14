from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostDetailView, PostAddView, PostEditView, PostDeleteView, SearchList

urlpatterns = [
   path('', PostsList.as_view()),
   path('search/', SearchList.as_view(), name='search'),
   path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
   path('add/', PostAddView.as_view(), name='post_add'), 
   path('<int:pk>/add', PostEditView.as_view(), name='post_edit'),
   path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),

   ]