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


