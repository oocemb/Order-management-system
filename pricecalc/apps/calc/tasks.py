from http.client import HTTPException

from calc.models import Furniture, Ldstp
from pricecalc.celery import app
from pricecalc.apps.base.crawler import *
from pricecalc.apps.base.crawler_ldstp import update_ldstp_data


@app.task(name='get_data_curent_page')
def get_data_in_current_page(page: int, url: str, category_id: int) -> list:
    """Получает список словарей фурнитуры с конкретной страницы."""
    return get_all_data_on_furniture_with_current_page(page, url, category_id)


@app.task(name='update_ldstp')
def update_ldstp_task():
    """Удаляет старую и добавляет новую информацию о наличии и ценах ЛДСП."""
    data_list = update_ldstp_data()
    bulk_create_list = []
    for item in data_list:
        bulk_create_list.append(Ldstp(**item))
    Ldstp.objects.all().delete()
    Ldstp.objects.bulk_create(bulk_create_list)


@app.task(name='update_data_makmart')
def update_data_furniture():
    """Контроллер обновления данных о фурнитуре МакМарт
    Создаёт, обновляет, удаляет модели Furniture в базе данных
    """
    _html_catalog = get_html(URL_Makmart)
    _dict_urls = sort_required_makmart_links(get_all_links_in_catalog(_html_catalog))
    _categories = list(_dict_urls.keys())
    _update_list = []
    for _category in _categories:
        for url in _dict_urls[_category]:
            http = get_http(url)
            if http.status_code == 200:
                print(url)
                _html = get_html(url)
                pages_count = get_pages_count(_html)
                for page in range(1, pages_count+1):
                    print(page)
                    result = get_data_in_current_page.delay(page, url, _category)          
                    _update_list += result.wait()
            else:
                print('Error http')
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
        fields = ['price', 'price_retail', 'availability']) 

    # если вычесть разницу из всего что есть и что есть для обновления получаем элементы для удаления
    queryset_to_delete = furnitures.difference(queryset_update_in_database)
    list_article_to_delete = list(queryset_to_delete.values_list('article', flat=True))
    del_items = Furniture.objects.filter(article__in=list_article_to_delete).delete()
    print('Delete items: ', del_items)

    # вычисляем какие из всех артикулов есть в базе данных
    articles_in_database = list(queryset_update_in_database.values_list('article', flat=True))

    # вычитаем из всех артикулов те что есть получаем список новых артикулов
    list_new_items = list(set(articles_list).difference(set(articles_in_database)))
    print('New items: ',list_new_items)
    for row_dict in _update_list:
        if row_dict['article'] in list_new_items:
            bulk_create_list.append(Furniture(**row_dict))
    Furniture.objects.bulk_create(bulk_create_list)


# @app.task
# def send_spam_email():
#     for contact in User.objects.all():
#         send_email(
#             'You subscrib', # title
#             'We spam you', # text
#             'ooo@ooo.com', # from email
#             [contact.email],
#             fail_silently=False,
#         )

# my_task.apply_async((args,kwargs),(countdown=60),) # запустит через 60 сек а не сразу


# @app.task(bind=True) # default_retry_delay=3 * 60
# def update_data_regularly(self):
#     i = 1
#     while i < 3:  
#         multiproc(i)
#         i += 1
#     try:
#         return 'Success'
#     except HTTPException as exc:
#         raise self.retry(exc=exc, countdown=60)
    

