from asyncore import write
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, freeze_support


URL = 'https://makmart.ru/catalog/drying/upper/'
Header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36', 'accept':'*/*'}
HOST = '' # если к ссылкам нужно добавить хост в начале для автоматического перехода для след парсеров
params = ''
FILE = 'items4_data.csv'

def get_http(url):
    response = requests.get(url) 
    return response

def get_html(url, params=None):
    response = requests.get(url, params=params) # Response (class) # тут можно отправить Headers если сайт блочит как бота
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
    items_data = []

    # Можно спарсить только ссылки
    #items = soup.find('div', class_='catalog_block items block_list').find_all('div', class_='image_wrapper_block')
    #for item in items:
    #    url_a_href =item.find('a').get('href')
    #    items_data.append(url_a_href)  

    # Можно спарсить целый массив данных
    for item in items:   

        #eur_price = item.find('span',class_='current')
        #if eur_price:
        #    eur_price = eur_price.get_text()
        #else:
        #    eur_price = 'Цены в евро нет'  # и в требуемый параметр записывать уже отформатированную переменную

        #Удаление каких либо маркеров :
        # get_text().replace('#####','')

        # 'city': item.find('svg', class_='svg115').find_next('span').get_text() # поиск внутрь 'span' если нет точной ссылки
        # лучше данные добавлять через try: except:
        items_data.append({
            'title': item.find('div', class_='item-title').get_text(strip=True),
            'art': item.find('div', class_='article_block').get('data-value'),
            'price': round(float(item.find('div', class_='price').get('data-value')),0),
            'available': item.find('div', class_='sa_block').get_text(strip=True)
        })

    return items_data

def save_file(items, path):
    """Функция сохранения информации **items в файл по нужному пути **path """
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';') # делимитер - разделитель для экселя
        writer.writerow(['Название', 'Артикул', 'Цена', 'Наличие'])
        for item in items:
            writer.writerow([item['title'], item['art'], item['price'], item['available']])
        

def multiproc(page):
    html = get_html(URL, params={'PAGEN_1':page})
    data = get_all_data(html)
    save_file(data,FILE)

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

        #проверям что за данные напарсили    
        #for i in items_data:
        #    print(i)

        #Мультипоточный парсинг
        with Pool(10) as pool:
            pool.map(multiproc,range(1, pages_count+1)) # функцию указываем как саму функцию без () - т.е. не результат а её


    else:
        print('Error http')
    


if __name__ == '__main__':
    main()
