import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

from .services import calculate_furniture_price

from calc.models import CategoryFurniture, Furniture

URL = 'https://makmart.ru/catalog/drying/upper/'
Header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36', 'accept':'*/*'}
HOST = 'https://makmart.ru' # если к ссылкам нужно добавить хост в начале для автоматического перехода для след парсеров
params = ''


def get_http(url):
    """ Получает http response от получаемого URL
    """
    response = requests.get(url) 
    return response


def get_html(url, params=None):
    """ Получает Html код страницы по URL и заданным параметрам
    params: int - номер страницы пагинатора
    """
    response = requests.get(url, params=params)
    return response.text


def get_pages_count(html):
    """ Узнаёт количество страниц в пагинаторе
    """
    soup = BeautifulSoup(html, 'html.parser')
    paginator = soup.find('div', class_='module-pagination').find_all('a', class_='dark_link')
    pagin_nub = paginator.pop()
    last_page = int(pagin_nub.get_text())
    if paginator:
        return last_page
    else:
        return 1


def get_all_data_on_furniture(html, object, category):
    """ Собирает все элементов фурнитуры на конкретной странице html
    и создаёт список для дальнейшего обновления в БД
    """
    items_data_bulk_list = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='catalog_block items block_list').find_all('div', class_='item_block')
    for item in items:
        price = round(float(item.find('div', class_='price').get('data-value')),0)
        
        row_dict = {
            'category_id': category,
            'title': item.find('div', class_='item-title').get_text(strip=True),
            'article': item.find('div', class_='article_block').get('data-value'),
            'price': price,
            'availability': item.find('div', class_='sa_block').get_text(strip=True),
            'price_retail': calculate_furniture_price(price)
        }
        
        items_data_bulk_list.append(object(**row_dict))
    return items_data_bulk_list
        

def add_data_in_current_page_furniture(page, object, URL, category):
    """ Добавляет в общий словарь данные конкретной страницы
    TODO: Каждная страница сейчас вызывает базу данных лучше сделать возврат списка
    и после того все нужные списки обьеденить и разом засунуть в БД
    """
    html = get_html(URL, params={'PAGEN_1':page})
    object_list = get_all_data_on_furniture(html, object, category)
    object.objects.bulk_create(object_list)


def update_data_makmart():
    """ Контроллер цикла парсигра данных по конкретной фурнитуре
    Создаёт обьекты в базе данных
    """
    html = get_html('https://makmart.ru/catalog/')
    urls = sort_required_links(get_all_links_in_catalog(html))
    category = list(urls.keys())
    urls = list(urls.values())
    # category = CategoryFurniture.objects.get(id=category[0])
    category = category[0]
    urls = urls[0]
    for url in urls:
        http = get_http(url)
        if http.status_code == 200:
            print(url) ###
            pages_count = get_pages_count(get_html(url))
            for page in range(1, pages_count+1):
                print(page) ###
                add_data_in_current_page_furniture(page, Furniture, url, category)
        else:
            print('Error http')


def get_all_links_in_catalog(html):
    """Получает список всех ссылок на пункты из каталога."""
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='catalog_section_list').find_all('li', class_='name')
    links_list = []
    for item in items:
        links_list.append(item.find('a', class_='dark_link').get('href'))  
    return links_list


def sort_required_links(links_list: list) -> dict:
    """Получает список необходимых ссылок и формирует соответствие с нужными моделями.
    ВАЖНО:
    чтобы настоить данную функцию нужно сверится с текущими данными с сайта!! 
    данная функция не автоматизирована, при изменениях данных на сайте возможно некоректная работа.
    Проверить какие пункты меню можно сложить в общую фурнитуру *OtherFurniture*
    Остальные пункты сравнить по номеру к названию к моделям БД (список с 0 элемента)."""
    # _NOT_NEEDED = [1,9,12,17,20,23,27,28,31,37,38,39,40,41]
    _USE_LIST = []
    _OTHER_FURNITURE = [11,13,19,29,34,35] # петли, магниты, защелки, навески, замки
    _OTHER_KITCHEN_FURNITURE = [6,7,16,18,22,26,30]
    _COUNTERTOPS_AND_ADDS = [2,3,4] # плинтусы, профили для столешниц, столешницы
    _SINK_AND_DRYING = [5,15] # мойки, сушки
    _LIFT_AND_BOX = [14,21] # ящики, подьёмники
    _MENSOLO_AND_HANGERS_AND_LEG = [24,25,8,10] # менсоло, крючки, ножки опоры
    _WARDROBE_FURNITURE = [32,33] # гардеробная фурнитура
    _HANDLE = [36]
    # TODO: Можно добавить сравнительный анализ категорий в БД и вставлять сюда в список ссылок правильный Id
    _USE_LIST = {
        1: _OTHER_FURNITURE, 
        2: _OTHER_KITCHEN_FURNITURE, 
        3: _COUNTERTOPS_AND_ADDS,
        4: _SINK_AND_DRYING,
        5: _LIFT_AND_BOX,
        6: _MENSOLO_AND_HANGERS_AND_LEG,
        7: _WARDROBE_FURNITURE,
        8: _HANDLE}
    for _list in _USE_LIST.values():
        for i, item in enumerate(_list, 0):
            _list[i] = HOST + links_list[item-1] # item - 1, для корректных индексов
    return _USE_LIST


