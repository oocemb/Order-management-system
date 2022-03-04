from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from base.services import *
from .utils import *
from .models import *
from .forms import *



def posts_list(request):
    """ Вывод списка постов
    """
    posts, POST_PER_PAGE = default_or_search_posts(request, Post)
    is_paginated, prev_url, next_url, current_page = paginator_create(posts, POST_PER_PAGE, request)
    
    return render(request, 'blog/posts_list.html', context={'posts': current_page
    , 'is_paginated': is_paginated, 'next_url':next_url, 'prev_url':prev_url})


def tags_list(request):
    """ Вывод списка тэгов
    """
    tags = Tag.objects.all()

    return render(request, 'blog/tags_list.html', context={'tags':tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    redirect_url = 'tags_list'
    raise_exception = True


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.html'
    redirect_url = 'posts_list'
    raise_exception = True
