'''import asyncio
from time import time

#@asyncio.coroutine
async def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(1)

#@asyncio.coroutine
async def print_time():
    count = 0 
    while True:
        if count % 3 == 0:
            print("{} seconds have passed".format(count))
        count += 1
        await asyncio.sleep(1)

#@asyncio.coroutine с пайтон 3.5 и вместо декоратора и заменили yield from  === await
async def main(): # подписывать саму функцию async
    task1 = asyncio.create_task(print_nums())   ## заменили  .ensure_future(
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1,task2)  # создаём очередь из задач

#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())
#loop.close()
asyncio.run(main())'''

import requests
from time import time


url = 'https://loremflickr.com/320/240'

def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r

def write_file(response):
    #https://loremflickr.com/cache/resized/65535_51310547397_619bec890a_320_240_nofilter.jpg
    filename = response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)
    
def main():
    t0 = time()

    for i in range(10):
        write_file(get_file(url))

    print(time()-t0)

main()

import asyncio
import aiohttp

def write_img(data):
    filename = 'file-{}.jpeg'.format(int(time()*1000))
    with open(filename, 'wb') as file:
        file.write(data)

async def fetch_content(url,session): # запрашиваем контент
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read() # возавращает бинарный файл картинки
        write_img(data)

async def main2():
    tasks = []
    async with aiohttp.ClientSession() as session: # открываем сессию асинк(т.к. всё асинхронн)
        for i in range (10):
            task = asyncio.create_task(fetch_content(url,session))
            tasks.append(task)
        await asyncio.gather(*tasks) # *tasks - раскладывает список по элементам в ряд 


t0 = time()
asyncio.get_event_loop().run_until_complete(main2())
print(time()-t0)
