from time import time
from typing import Type

from django.utils.text import slugify
from django.core.paginator import Paginator, Page
from django.db.models import Q, CharField, QuerySet
from django.http.request import HttpRequest

from config.models import BaseModel
from config.settings import env


def gen_slug(s: CharField) -> str:
    """Генерирует уникальный слаг для поста добавляет таймстамп"""
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


def paginator_create(objects: QuerySet[BaseModel], item_per_page: int, request: HttpRequest) -> tuple[bool, str, str, Page]:
    """Создание пагинатора и необходимых для него ссылок *вперёд *назад"""
    paginator = Paginator(objects, item_per_page)  # http://127.0.0.1:8000/posts/?page=2
    page_number = request.GET.get('page', 1)  # дефолтное значение если не нашёл в запросе этот параметр
    current_page = paginator.get_page(page_number)
    is_paginated = current_page.has_other_pages()
    if current_page.has_previous():
        prev_url = '?page={}'.format(current_page.previous_page_number())
    else:
        prev_url = False
    if current_page.has_next():
        next_url = '?page={}'.format(current_page.next_page_number())
    else:
        next_url = False
    return is_paginated, prev_url, next_url, current_page


def default_or_search_posts(request: HttpRequest, post: Type[BaseModel]) -> tuple[QuerySet[BaseModel], int]:
    """Получает список все постров по умолчанию, 
    отслеживает есть ли запрос на поиск по постам и выводит"""
    POST_PER_PAGE = env("POST_PER_PAGE")
    search_query = request.GET.get('search', '')
    if search_query:  # если в фильтре через запятую параметры, то это оператор AND
        posts = post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        POST_PER_PAGE = len(posts)
        return posts, POST_PER_PAGE
    else:
        return post.objects.all(), POST_PER_PAGE
