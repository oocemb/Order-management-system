from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from base.utils import paginator_create, default_or_search_posts
from blog.mixins import ObjectDetailMixin, ObjectCreateMixin, ObjectDeleteMixin, ObjectUpdateMixin
from blog.models import Post, Tag
from blog.forms import TagForm, PostForm


def posts_list(request: HttpRequest) -> HttpResponse:
    """Вывод списка постов"""
    posts, post_per_page = default_or_search_posts(request, Post)
    is_paginated, prev_url, next_url, current_page = paginator_create(posts, post_per_page, request)
    
    return render(
        request, 'blog/posts_list.html', context={
            'posts': current_page, 'is_paginated': is_paginated, 'next_url': next_url, 'prev_url': prev_url
        }
    )


def tags_list(request: HttpRequest) -> HttpResponse:
    """Вывод списка тэгов"""
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
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
    model_form = PostForm
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
