from asyncore import write
import imp
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, freeze_support
from random import choice
import fake_useragent 
# users = fake_useragent.UserAgent()
# user = users.random
import selenium
from selenium import webdriver
import mysqlconnecter

URL = 'https://makmart.ru/catalog/drying/upper/'
Header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36', 'accept':'*/*'}
HOST = '' # если к ссылкам нужно добавить хост в начале для автоматического перехода для след парсеров
params = ''
FILE = 'items4_data.csv'


def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text

def get_ip(html):
    soup = BeautifulSoup(html, 'html.parser')
    ip = soup.find('span',class_='ip').text.strip()
    user_agent = soup.find('span',class_='ip').find_next_sibling('span').text.strip()
    # есть просто вариант next_sibling если не нужно поиска с файнд

def main():
    user_agents = open('useragents.txt').read().split('\n')
    proxys = open('proxy.txt').read().split('\n')

    for i in range(100):  # kol-vo zaprosov
        proxy = {'http': 'http://' + choice(proxys)}
        user_agent = {'User-Agent': choice(user_agents)}

        # какие то ИП быстро отваливаются и лучше использовать
        #try:    except:   

        # можно парсить сайт с задержкой по времени чтоб так же не банили sleep(60) # в секундах
        # randint(1,5) - рандом от секунд 1-5
        # random.uniform(1,5) - рандом с плавающей точкой
        html = get_html(URL, useragent=user_agent, proxy=proxy)


def scroll(url): # если нужно листать вместо пагинатора (Авито)
    users = fake_useragent.UserAgent()
    user = users.random

    options = selenium.webdriver.ChromeOptions()
    options.add_argument('--headless') # скрывает его режим работы
    options.add_argument(str(user))

    browser = webdriver.Chrome(options=options)
    browser.get(url)

    SCROLL_PAUSE_TIME = 0.5

    last_height = browser.execute_script('return document.body.scrollHeight') # замер экрана 1000

    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);') # крутим дальше
        new_height = browser.execute_script('return document.body.scrollHeight') # 2000
        time.sleep(SCROLL_PAUSE_TIME)
        if last_height == new_height:
            break
        last_height = new_height

    return browser.page_source # возвращаем прокрученный html

def write_sql(data):
    dbconfig = {'host': '127.0.0.1', 
                'user': 'admin',
                'password': 'admin',
                'database': 'db.sqlite3'}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert info db.sqlite3.'table' (id,title,price....) values (%s,%s,%s,...)""" # при дубликатах можно сделать replace вместо insert
    cursor.execute(_SQL,(data['id'],data['title'],data['price']....))
    conn.commit()
    cursor.close()
    conn.close()
if __name__ == '__main__':
    main()
