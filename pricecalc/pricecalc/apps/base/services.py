from django.utils.text import slugify
from time import time
from django.core.paginator import Paginator
from django.db.models import Q



def gen_slug(s):
    """Генерирует уникальный слаг для поста добавляет таймстамп
    """
    new_slug = slugify(s, allow_unicode=True)
    return (new_slug + '-' + str(int(time())))


def paginator_create(objects, post_per_page, request):
    """Создание пагинатора и необходимых для него ссылок *вперёд *назад
    """
    paginator = Paginator(objects,post_per_page) # http://127.0.0.1:8000/posts/?page=2
    page_number = request.GET.get('page', 1) # дефолтное значение если не нашёл в запросе этот параметр
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


def default_or_search_posts(request, object):
    """Получает список все постров по умолчанию, 
    отслеживает есть ли запрос на поиск по постам и выводит"""
    POST_PER_PAGE = 3
    search_query = request.GET.get('search', '')
    if search_query:  # если в фильтре через запятую параметры то это аператор AND и там и там
        posts = object.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        POST_PER_PAGE = len(posts)
        return posts, POST_PER_PAGE
    else:
        return object.objects.all(), POST_PER_PAGE


def calculate_furniture_price(price):
    """Расчитывает цену фурнитуры по заданной формуле."""
    MULTIPLIER = 1.5
    MULTIPLIER_MAX = 1.4
    COEFFICIENT_MIN = 100
    COEFFICIENT = 500
    MAX_PRICE = 10000
    MIN_PRICE = 200
    if price < MIN_PRICE:
        return price * MULTIPLIER + COEFFICIENT_MIN
    elif price > MAX_PRICE:
        return price * MULTIPLIER_MAX
    else:
        return price * MULTIPLIER + COEFFICIENT