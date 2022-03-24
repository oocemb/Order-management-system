
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, freeze_support


URL = 'https://makmart.ru/catalog/drying/upper/'
Header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36', 'accept':'*/*'}
HOST = '' # если к ссылкам нужно добавить хост в начале для автоматического перехода для след парсеров
params = ''
FILE = 'items2_data.csv'

def get_http(url):
    response = requests.get(url) 
    return response

def get_html(url, params=None):
    response = requests.get(url, params=params)
    return response.text # возвращает html код страницы  (url)

def get_pages_count(html):
    """Узнаём количество страниц в пагинаторе"""
    soup = BeautifulSoup(html, 'html.parser')
    paginator = soup.find('div', class_='module-pagination').find_all('a', class_='dark_link')
    pagin_nub = paginator.pop()
    last_page = int(pagin_nub.get_text())
    if paginator:
        return last_page
    else:
        return 1

def get_all_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='catalog_block items block_list').find_all('div', class_='item_block')
    links_list = []
 
    # Можно спарсить целый массив данных
    for item in items:
        links_list.append(item.get('href'))

    return links_list


def get_all_links_in_catalog(html):
    """Получает список всех ссылок на пункты из каталога."""
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='catalog_section_list').find_all('li', class_='name')
    links_list = []
    for item in items:
        links_list.append(item.find('a', class_='dark_link').get('href'))
    print(links_list, len(links_list))  
    return links_list


def sort_required_links(links_list: list) -> list:
    """Получает список необходимых ссылок и формирует соответствие с нужными моделями.
    ВАЖНО:
    чтобы настоить данную функцию нужно сверится с текущими данными с сайта!! 
    данная функция не автоматизирована, при изменениях данных на сайте возможно некоректная работа.
    Проверить какие пункты меню можно сложить в общую фурнитуру *OtherFurniture*
    Остальные пункты сравнить по номеру к названию к моделям БД (список с 0 элемента)."""
    _NOT_NEEDED = [1,9,12,17,20,23,27,28,31,37,38,39,40,41]
    _NOT_NEEDED = [i-1 for i in _NOT_NEEDED]
    _OTHER_FURNITURE = [11,13,19,29,34,35] # петли, магниты, защелки, навески, замки
    _OTHER_KITCHEN_FURNITURE = [6,7,16,18,22,26,30]
    _COUNTERTOPS_AND_ADDS = [2,3,4] # плинтусы, профили для столешниц
    _SINK = [5]
    _LEG = [8,10]
    _LIFT = [14]
    _DRYING = [15]
    _BOX = [21]
    _MENSOLO_AND_HANGERS = [24,25]
    _WARDROBE_FURNITURE = [32,33]
    _HANDLE = [36]
    _OTHER_FURNITURE = [i-1 for i in _OTHER_FURNITURE]
    for i, item in enumerate(_OTHER_FURNITURE, 0):
        _OTHER_FURNITURE[i] = links_list[item]
    return print(_OTHER_FURNITURE)


def main():
    http = get_http(URL)
    if http.status_code == 200:
        items_data = []
        pages_count = get_pages_count(get_html(URL))

        #Парсинг в одном потоке
        #for page in range(1, pages_count+1): # для всех страниц в пагинаторе сделать парсинг данных (+1 к стр)
        #    items_data.extend(get_all_data(get_html(URL, params={'PAGEN_1':page}))) # расширяем список
        #    print('Parse {}'.format(page))
        #save_file(items_data, FILE)

        #Мультипоточный парсинг
        # with Pool(10) as pool:
        #     pool.map(multiproc,range(1, pages_count+1)) # функцию указываем как саму функцию без () - т.е. не результат а её


    else:
        print('Error http')
    


html = get_html('https://makmart.ru/catalog/')

sort_required_links(get_all_links_in_catalog(html))