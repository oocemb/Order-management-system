from http.client import HTTPException

from pricecalc.celery import app
from pricecalc.apps.base.crawler import *


@app.task(name='update_data_curent_page')
def update_data_in_current_page(page: int, url: str, category_id: int) -> None:
    add_data_in_current_page_furniture(page, url, category_id)


@app.task(name='update_data_makmart')
def update_data_furniture():
    """ Контроллер цикла парсигра данных по конкретной фурнитуре
    Создаёт обьекты в базе данных модель Furniture
    """
    _html = get_html(URL_Makmart)
    _dict_urls = sort_required_makmart_links(get_all_links_in_catalog(_html))
    _categories = list(_dict_urls.keys())
    for _category in _categories:
        for url in _dict_urls[_category]:
            http = get_http(url)
            if http.status_code == 200:
                print(url)
                pages_count = get_pages_count(get_html(url))
                for page in range(1, pages_count+1):
                    print(page)
                    update_data_in_current_page.delay(page, url, _category)
            else:
                print('Error http')


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
    

