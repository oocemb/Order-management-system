from calc.models import Furniture, Ldstp
from config.celery import app
from crawler.handlers.makmart import (
    MAKMART_CATALOG_URL, get_pages_count_makmart, get_all_links_in_catalog_makmart, sort_required_makmart_links,
    get_all_data_on_makmart_furniture_from_current_page
)
from crawler.utils import get_http, get_html
from crawler.handlers.ldstp_mebelet import update_ldstp_data
from config.logger import logger


@app.task(name='update_ldstp')
def update_ldstp_task():
    """Задача для Селери удаляет старую и добавляет новую информацию о наличии и ценах ЛДСП"""
    _bulk_create_list = [Ldstp(**item) for item in update_ldstp_data()]
    Ldstp.objects.all().delete()
    Ldstp.objects.bulk_create(_bulk_create_list)


@app.task(name='update_data_makmart')
def update_makmart_data_task():
    """Задача для Селери по обновлению данных о фурнитуре МакМарт
    Создаёт, обновляет, удаляет модели Furniture в базе данных"""
    _html_catalog = get_html(MAKMART_CATALOG_URL)
    _dict_urls = sort_required_makmart_links(get_all_links_in_catalog_makmart(_html_catalog))
    _categories = list(_dict_urls.keys())
    _update_list = []
    for _category in _categories:
        for url in _dict_urls[_category]:
            http = get_http(url)
            if http.status_code == 200:
                logger.info(url)
                _html = get_html(url)
                pages_count = get_pages_count_makmart(_html)
                for page in range(1, pages_count + 1):
                    logger.info(page)
                    result = get_all_data_on_makmart_furniture_from_current_page(page, url, _category)
                    _update_list += result
            else:
                logger.error('Error http')
    # получили словарь всех элементов для обновления и создания новых

    bulk_create_list = []
    articles_list = []
    furnitures = Furniture.objects.all()

    # создаём список всех артикулов для обновления и создания новых
    for row_dict in _update_list:
        articles_list.append(row_dict['article'])

    # создаём кварисэт для обновления элементов (сравнивая всё что есть с списком артикулов)
    queryset_update_in_database = Furniture.objects.filter(article__in=articles_list)
    for item in queryset_update_in_database:
        for row_dict in _update_list:
            if item.article == row_dict['article']:
                item.price = row_dict['price']
                item.price_retail = row_dict['price_retail']
                item.availability = row_dict['availability']
    Furniture.objects.bulk_update(queryset_update_in_database,
                                  fields=['price', 'price_retail', 'availability'])

    # если вычесть разницу из всего что есть и что есть для обновления получаем элементы для удаления
    queryset_to_delete = furnitures.difference(queryset_update_in_database)
    list_article_to_delete = list(queryset_to_delete.values_list('article', flat=True))
    del_items = Furniture.objects.filter(article__in=list_article_to_delete).delete()
    logger.info(f'Delete items: {del_items}')

    # вычисляем какие из всех артикулов есть в базе данных
    articles_in_database = list(queryset_update_in_database.values_list('article', flat=True))

    # вычитаем из всех артикулов те что есть получаем список новых артикулов
    list_new_items = list(set(articles_list).difference(set(articles_in_database)))
    logger.info(f'New items: {list_new_items}')
    for row_dict in _update_list:
        if row_dict['article'] in list_new_items:
            bulk_create_list.append(Furniture(**row_dict))
    Furniture.objects.bulk_create(bulk_create_list)
