import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, freeze_support
# from .models import *

URL = 'https://mebelet.com/catalog/ldsp-tolcshina-16mm/?count=10000'
Header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36', 'accept':'*/*'}
HOST = '' # используется если ссылки идут укороченные и нужно добавить хост в начале для автоматического перехода для след парсеров



def get_http(url):
    """ Получает ответ от данного url
    """
    response = requests.get(url) 
    return response



def get_html(url):
    """ Возвращает html код страницы по --> (url)
    """
    response = requests.get(url)
    return response.text



def get_all_data(html):
    """ Получает необходимые данные из html кода
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('tbody').find_all('tr')
    items_data_bulk_list = []
    print(items)
    for item in items:
        print(item.find('td', 'tsvalue').find('a').get_text())   

        print(item.find('td', class_='price_cell').find('nobr').get_text())   
        # row_dict = {
        #     'title': item.find('a').text(strip=True),
        #     # 'price': round(float(item.find('div', class_='price').get('data-value')),0),
        #     # 'availability': item.find('div', class_='sa_block').get_text(strip=True)
        # }
        # # items_data_bulk_list.append(Ldstp(**row_dict))
        # items_data_bulk_list.append(row_dict)

    return items_data_bulk_list
        


def multiproc(page):
    html = get_html(URL, params={'PAGEN_1':page})
    data = get_all_data(html)
    Ldstp.objects.bulk_create(data)



def main():
    """ Контроллер парсинга наличия цветов ЛДСП
    """
    http = get_http(URL)
    if http.status_code == 200:

        # Парсинг в одном потоке   
        get_all_data(get_html(URL))

    else:
        print('Error http')
    


if __name__ == '__main__':
    main()
