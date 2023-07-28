import re

from bs4 import BeautifulSoup

from config.logger import logger
from crawler.utils import get_http, get_html

URL_LIST = ('https://mebelet.com/catalog/?count=10000&section=13357',
            'https://mebelet.com/catalog/ldsp-tolcshina-16mm/?count=10000',
            'https://mebelet.com/catalog/?count=10000&section=18408',
            'https://mebelet.com/catalog/?count=10000&section=14068',
            'https://mebelet.com/catalog/ldsp-egger-tolcshina-16mm/?count=10000')


def get_ldstp_mebelet_data(html):
    """Получает необходимые данные из html кода"""
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('table', id='myTable').find('tbody').find_all('tr')
    update_data_list = []
    for item in items:
        prices = item.find_all('td', class_='price_cell')  # в МЭ 2 ячейки с ценой берём 0 для примера
        price = float(re.sub(' ', '', prices[0].find('nobr').get_text()))
        title = item.find('a').get('title') or 'default title'
        row_dict = {
            'title': title,
            'price': price,
            'availability': item.find('abbr').get('title')
        }
        update_data_list.append(row_dict)
    return update_data_list


def update_ldstp_data(url_list: tuple[str] = URL_LIST) -> list:
    """Контроллер парсинга наличия цветов ЛДСП"""
    update_list = []
    for url in url_list:
        http = get_http(url)
        if http.status_code == 200:
            update_list.extend(get_ldstp_mebelet_data(get_html(url)))
        else:
            logger.error(f'Error http code from URL:{url}, status code:{http.status_code}')
    return update_list
