from re import search, template
from urllib import request
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View
from .utils import *
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


def posts_list(request):
    POST_PER_PAGE = 3
    search_query = request.GET.get('search', '')
    if search_query:  # если в фильтре через запятую параметры то это аператор AND и там и там
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        POST_PER_PAGE = len(posts)
    else:
        posts = Post.objects.all()
    
    paginator = Paginator(posts,POST_PER_PAGE) # http://127.0.0.1:8000/posts/?page=2
    page_number = request.GET.get('page', 1) # дефолтное значение если не нашёл в запросе этот параметр
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    return render(request, 'calc/posts_list.html', context={'posts':page, 'is_paginated': is_paginated, 'next_url':next_url, 'prev_url':prev_url})  # object_list текущие страницы


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'calc/tags_list.html', context={'tags':tags})


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'calc/post_detail.html'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'calc/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'calc/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'calc/tag_update.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'calc/tag_delete.html'
    redirect_url = 'tags_list'
    raise_exception = True


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'calc/post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'calc/post_update.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'calc/post_delete.html'
    redirect_url = 'posts_list'
    raise_exception = True


def index_calc(request):
   context = {
       'latext_calc_list': Calc.objects.order_by('-calc_date')[:5] if request.user.is_authenticated else[]
   }
    # отсортировать в обратку ( - kak деск) и срез на 5
   return render(request, 'calc/list.html', context)

def detail(request, calc_id):
    try:
        a = Calc.objects.get( id = calc_id )
    except:
        raise Http404("Not found")
    latest_comment = a.comment_set.order_by('-id')[:10]
    return render(request, 'calc/detail.html', {'calc':a, 'latest_comment':latest_comment})

def comment(request, calc_id):
    try:
        a = Calc.objects.get( id = calc_id )
    except:
        raise Http404("Not found")

    a.comment_set.create(author_name = request.POST['name'], comment_text = request.POST['text'])
    return HttpResponseRedirect(reverse('detail', args = (a.id,)))

def users(request):
    userlist = User.objects.order_by('id')
    return render(request, 'calc/user.html', {'userlist':userlist})

def add_user(request):
    a = User(user_name = request.POST['name'])
    a.save()
    # можно сразу в базу без сейва a = User.objects.create(name = 123123)
    # регистронезависисый поиск xxx.objects.get(name__iexact = 'qweqwe')  - get возвр 1 обьект
    # лук ап контейнс  xxxx.objects.filter(name__contains = 'qweqwe') - фильрт возвр Кварисет
    # {{ post.body|truncatewords:15 }} - последние 15 слов из бади
    return HttpResponseRedirect(reverse('calc:users'))  

def calculation(request, user_id):
    try:
        user = User.objects.get( id = user_id )
    except:
        raise Http404("Not found")
    calculationlist = user.calculation_set.order_by('-id')[:10]
    return render(request, 'calc/calculations.html', {'user': user, 'calculationlist': calculationlist})

def add_calculation(request, user_id):
    try:
        user = User.objects.get( id = user_id )
    except:
        raise Http404("Not found")
    user.calculation_set.create(price_title = request.POST['name'], price_date = timezone.now())
    return HttpResponseRedirect(reverse('calc:calculation', args = (user.id,)))


