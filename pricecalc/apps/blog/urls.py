from django.urls import path

from .views import *


#app_name = "blog"
urlpatterns = [
    path('posts/', posts_list, name = 'posts_list'),
    path('post/create/', PostCreate.as_view(), name='postcreate'),
    path('post/<str:slug>/', PostDetail.as_view(), name='postdetail'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name='postupdate'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='postdelete'),

    path('tags/', tags_list, name='tags_list'),
    path('tag/create/', TagCreate.as_view(), name = 'tagcreate'),
    path('tag/<str:slug>/', TagDetail.as_view(), name = 'tagdetail'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name = 'tagupdate'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name = 'tagdelete'),
]