from asyncore import write
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, freeze_support
from .models import *

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
    items_data_bulk_list = []
 
    # Можно спарсить целый массив данных
    for item in items:   

        row_dict = {
            'title': item.find('div', class_='item-title').get_text(strip=True),
            'article': item.find('div', class_='article_block').get('data-value'),
            'price': round(float(item.find('div', class_='price').get('data-value')),0),
            'availability': item.find('div', class_='sa_block').get_text(strip=True)
        }
        items_data_bulk_list.append(Furniture(**row_dict))
        # items_data.append({
        #     'title': item.find('div', class_='item-title').get_text(strip=True),
        #     'art': item.find('div', class_='article_block').get('data-value'),
        #     'price': round(float(item.find('div', class_='price').get('data-value')),0),
        #     'available': item.find('div', class_='sa_block').get_text(strip=True)
        # })

    return items_data_bulk_list

def save_file(items, path):
    """Функция сохранения информации **items в файл по нужному пути **path """
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';') # делимитер - разделитель для экселя
        # writer.writerow(['Название', 'Артикул', 'Цена', 'Наличие'])
        for item in items:
            writer.writerow([item['title'], item['art'], item['price'], item['available']])
        

def multiproc(page):
    html = get_html(URL, params={'PAGEN_1':page})
    data = get_all_data(html)
    # save
    Furniture.objects.bulk_create(data)

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
        with Pool(10) as pool:
            pool.map(multiproc,range(1, pages_count+1)) # функцию указываем как саму функцию без () - т.е. не результат а её


    else:
        print('Error http')
    


if __name__ == '__main__':
    main()
