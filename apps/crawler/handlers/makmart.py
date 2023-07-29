from bs4 import BeautifulSoup

from crawler.utils import get_html, calculate_furniture_price
from config.logger import logger

MAKMART_URL = 'https://makmart.ru'  # К ссылкам нужно добавить хост для след парсеров
MAKMART_CATALOG_URL = MAKMART_URL + '/catalog/'


def get_pages_count_makmart(html) -> int:
    """Узнаёт количество страниц в пагинаторе"""
    soup = BeautifulSoup(html, 'html.parser')
    paginator = soup.find('div', class_='module-pagination')
    if paginator is not None:
        paginator_link = paginator.find_all('a', class_='dark_link')
        last_page = int(paginator_link.pop().get_text())
        return last_page
    else:
        return 1


def get_all_links_in_catalog_makmart(html) -> list:
    """Получает список всех ссылок на пункты из каталога"""
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='catalog_section_list').find_all('li', class_='name')
    links_list = []
    for item in items:
        links_list.append(item.find('a', class_='dark_link').get('href'))
    return links_list


def sort_required_makmart_links(links_list: list) -> dict:
    """Получает список всех ссылок и формирует соответствие с нужными моделями.
    ВАЖНО:
    Чтобы настроить данную функцию, нужно свериться с текущими данными с сайта!
    Данная функция не автоматизирована, при изменениях данных на сайте возможно некорректная работа.
    Проверить какие пункты меню можно сложить в общую фурнитуру *OtherFurniture*
    Остальные пункты сравнить по номеру к названию к моделям БД"""
    # Цифры соответствуют номеру категории на сайте МакМарта
    # _NOT_NEEDED = [1,9,12,17,20,23,27,28,31,37,38,39,40,41]
    _OTHER_FURNITURE = [11, 13, 19, 29, 34, 35]  # петли, магниты, защелки, навески, замки
    _OTHER_KITCHEN_FURNITURE = [6, 7, 16, 18, 22, 26, 30]
    _COUNTERTOPS_AND_ADDS = [2, 3, 4]  # плинтусы, профили для столешниц, столешницы
    _SINK_AND_DRYING = [5, 15]  # мойки, сушки
    _LIFT_AND_BOX = [14, 21]  # ящики, подъёмники
    _MENSOLO_AND_HANGERS_AND_LEG = [24, 25, 8, 10]  # менсоло, крючки, ножки опоры
    _WARDROBE_FURNITURE = [32, 33]  # гардеробная фурнитура
    _HANDLE = [36]
    result_dict = {
        1: _OTHER_FURNITURE,
        2: _OTHER_KITCHEN_FURNITURE,
        3: _COUNTERTOPS_AND_ADDS,
        4: _SINK_AND_DRYING,
        5: _LIFT_AND_BOX,
        6: _MENSOLO_AND_HANGERS_AND_LEG,
        7: _WARDROBE_FURNITURE,
        8: _HANDLE}
    for categories_links in result_dict.values():
        for i, real_nmb in enumerate(categories_links):
            categories_links[i] = MAKMART_URL + links_list[real_nmb - 1]  # Т.к. список ссылок начинается с нуля
    return result_dict  # Список номеров real_nmb это цифры по каталогу МакМарта, нужно сделать смещение на -1


def get_all_data_on_makmart_furniture_from_current_page(page: int, url: str, category_id: int) -> list:
    """Собирает все элементов фурнитуры на конкретной странице html
    и создаёт список словарей фурнитуры для дальнейшего обновления в БД"""
    items_data_bulk_list = []
    html = get_html(url, params={'PAGEN_1': page})
    if not html:
        logger.warning(f"Unknown error from URL:{url}?PAGEN_1={page}")
        return []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='catalog_block items block_list').find_all('div', class_='item_block')
    for item in items:
        if item.find('div', class_='price'):
            price = round(float(item.find('div', class_='price').get('data-value')), 0)
        else:
            price = 0
        row_dict = {
            'category_id': category_id,
            'title': item.find('div', class_='item-title').get_text(strip=True),
            'article': item.find('div', class_='article_block').get('data-value'),
            'price': price,
            'availability': item.find('div', class_='sa_block').get_text(strip=True),
            'price_retail': calculate_furniture_price(price)
        }

        items_data_bulk_list.append(row_dict)
    return items_data_bulk_list
