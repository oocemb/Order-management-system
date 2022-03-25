
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