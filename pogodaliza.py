'''Декоратор (ПРИМЕР)

def message_decor(msg='Random'):
    def mydecorator(f):
        def wrapper(*args,**kwargs):
            print("Before func"+ msg)
            f(*args,**kwargs)
            print("After func")
        return wrapper
    return mydecorator

@message_decor(msg='Hello')
def print_name(famylia):
   # famil = input ('Как твоя фамилия')
    print('Sasha'+ famylia)
print_name('Gru')'''

'''Генератор (ПРИМЕР)

x = [1,3,5,7]
new_x = [x**2 for x in x]
sqrt_x = [x**0.5 for x in x if x//5 >= 0]
print(x, new_x, sqrt_x, sep='\n')
'''

''' Задача массив остаток от 6

import random
from tkinter import Y
a = []
LENGTH_a = 50
y = 1000
a = [random.randrange(1,1000,1) for i in range(LENGTH_a)]
print(a)
for i in range(LENGTH_a):
    if a[i]%6 > 0:
        y_curent = a[i]     
        if y_curent < y:
            y = y_curent
for i in range(LENGTH_a):
    if a[i]%6 > 0:
        a[i] = y
print(a)
'''

'''Простейший цикл функций         
def hi():
    name = input("Как звать?")
    print('You noobster' + name)

def loop(f, n): # f - funct, n - repeats time
    if n <=0:
        return
    else:
        f()
      #  n-=1
        loop(f,n-1)
loop(hi,3)
'''   

'''ПРИМЕРЫ str.___switch boolean
str = "это пример строки....wow!!!"
print (str.startswith( 'это' ))
print (str.startswith( 'строки', 11 ))
print (str.startswith( 'это', 2, 4 ))

my_str = 'Discworld'
print(my_str.endswith('jockey'))  # False
print(my_str.endswith('world'))  # True
print(my_str.endswith(('jockey', 'world')))  # True
print(my_str.endswith('wo', 0, 6))  # True
'''

'''Функции с переменными
from turtle import title
from unittest import result


stroka = 'pppqqqeee'
stroka *= 5
print(stroka[4:10])
#print(stroka[0],stroka[7])
list1 = list('router2$%@#$#@F34234')
print(list1[5::3]) # срезать с 5(6) элемента взять каждый 3й
#print(list1[-2],list1[::-1],list1[::-3])
list1.reverse()
print(list1)
list2 = [list1[::-4],list1,list1[-4::]]
#print(list2,len(list1),len(list2))
print(sorted(list1)) ##  работает с разными видами преременных,no work  вложенными списками

list1.append('300')
list1.extend(list1) # меняет список, а суммирование создаёт новый
list10 = list1 + list2
print('###'.join(list1)) # собирает список(строку) в строку join, не умеет с вложенными
print('$$$'.join(stroka))
list10.pop(-3) 
list10.remove('#') # удаляет первый такой элемент, не все
list10.insert(5,'XoXoX')
for i in range(len(list10)):
    if type(list10[i]) != str:
        list10[i].sort()

#list10.sort() # не может сравнить строку и список, не работает с строками вообще, только списки
print(list10.index('r')) # номер первого элемента
print(list10) # лист 2 при этом содержит двойной лист 1 
            #хотя операция присваивания была совершена раньше чем удвоение списка1

slovar = {'name': 'Liza', 'family': 'Gru', 'status': 'fishnoob'}
print(slovar['status'])
slovar['gamelevel'] = 1250
slovar['fishslovar'] = {
    'godofluck': True,
    'whathappens': 'Diediedie',
    'percentofwin': 30
}
print(slovar)
print(slovar['fishslovar']['godofluck']) 
print(sorted(slovar)) # возвр список с сортироваными ключами
d_keys = ['one','two','tri']
noinfo_slovar = dict.fromkeys(d_keys, 1) # создаёт словарь с None переменными (или что напишешь)
# если указать начальное значение ссылкой на изменяемый файл, выйдет что всё будет меняться от одного
print(noinfo_slovar)

vlans = [f'vlan {num}' for num in range(10,14)]
print(vlans)
numerss = [num for num in list1 if num.isdigit()] # нельзя ссылаться на вложенные списки (прямо)
print(numerss)

london_co = {
        'r1' : {
        'hostname': 'london_r1',
         'location': '21 New Globe Walk',
         'vendor': 'Cisco',
         'model': '4451',
         'IOS': '15.4',
         'IP': '10.255.0.1'
         },
         'r2' : {
         'hostname': 'london_r2',
         'location': '21 New Globe Walk',
         'vendor': 'Cisco',
         'model': '4451',
         'IOS': '15.4',
         'IP': '10.255.0.2'
         },
         'sw1' : {
         'hostname': 'london_sw1',
         'location': '21 New Globe Walk',
         'vendor': 'Cisco',
         'model': '3850',
         'IOS': '3.6.XE',
         'IP': '10.255.0.101'
         }
     }
print([london_co[device]['vendor'] for device in london_co])
# генератор вывода работает только с вложеными словарями


vlans = [[10,21,35], [101, 115, 150], [111, 40, 50]]
print([vlan for vlan_list in vlans for vlan in vlan_list if vlan%10==0])
newvlans = [vlan for vlan_list in vlans for vlan in vlan_list]
print(newvlans)
namess = ['one','two']
familys = ['gru', 'iva', 'wtf']
result = ['Name  {}\n Famy  {}'.format(name,fami) for name,fami in zip(namess,familys)]
print('\n'.join(result)) # только для одинаковых по длине списков

kvadrat = {num: num**2 for num in range(1,11)}
print(kvadrat)

slovar22 = {'NNName': 'Liza', 'family': 'Gru', 'status': 'fishnoob'}
newdict = {key.lower(): valu.lower() for key, valu in slovar22.items()}
print(newdict)

newdict2 = {devise: {key.lower(): valu.lower() for key,valu in params.items()} for devise, params in london_co.items()}
print(newdict2)

unique_vlan = {int(vlan) for vlan_list in vlans for vlan in vlan_list if vlan%50==0}
print(unique_vlan)

print(newdict.get('noob','Net noobs'))
print(newdict)
print(newdict.setdefault('status','25')) # возврат значение none или заданного по умолчанию и вписывание в словарь

del newdict['status']

newdict.update({'status': 1, 'whaaaat': 'nope'})
print(newdict)

tuple1 = ('password',)
tuple2 = tuple(stroka)
tuple3 = tuple(newdict)
sorted(tuple3)

vlans123 = set(newvlans) # создаёт множество исключающее равные числа
vlans12 = set(newdict) # уникальные ключи
print(vlans12)

line = "switchport trunk allowed vlan 10,20,30"
vlans = line.split()[-1].split(",")
print(vlans)

nat = "ip nat inside source list ACL interface FastEthernet0/1 overload"
vlannat = nat.split()
vlannat.insert(7,'GigabitEthernet0/1')
vlannat.pop(-2)
nat2 = (' '.join(vlannat))
print(nat2)
'''
'''
mac = "AAAA:BBBB:CCCC"
mac2 = '.'.join(mac.split()[0].split(":"))
print(mac2)

config = "switchport trunk allowed vlan 1,3,10,20,30,100"
vlans = config.split()[-1].split(',')
print(vlans)

vlans = [10, 20, 30, 1, 2, 100, 10, 30, 3, 4, 10]
result = list(set(vlans))
print(result)

command1 = "switchport trunk allowed vlan 1,2,3,5,8"
command2 = "switchport trunk allowed vlan 1,3,8,9"

vlan1 = set(command1.split()[-1].split(','))
vlan1 = list(vlan1.intersection(set(command2.split()[-1].split(','))))
print(vlan1)
'''

"""Итераторы примеры
class Iteraror1:
    def __init__(self,chislozadannoe):
        self.chislo1 = chislozadannoe
        self.counter = 0
    def __next__(self):

            self.chislo1 = self.chislo1 **2
            return self.chislo1
        
    def __iter__(self):
        return self
kvadrat = Iteraror1(5)
print(next(kvadrat))

class Iteraror2:
    def __init__(self,counter,chislo):
        self.chislo = chislo
        self.counter = counter
        self.begin = 0
    def __next__(self):
        while self.counter > self.begin:
            self.begin += 1
            self.chislo = self.chislo*2 + 1
        ##else:
            ##raise StopIteration # может быть дополнительным направлением в исполнении
        return self.chislo
    def __iter__(self):
        return self

func2 = Iteraror2(3,5)
print(next(func2))


circle_areas = [3.56773, 5.57668, 4.00914, 56.24241, 9.01344, 32.00013]
circle_areas = list(map(round,circle_areas,range(1,len(circle_areas)+1))) # Map пропускает каждый обьект через функцию
print(circle_areas)

my_strings = ['a', 'b', 'c', 'd', 'e']
my_numbers = [1,2,3,4,5,6,7]
results = zip(my_strings, my_numbers) # можно листом восстановить
print(results)
results1 = list(map(lambda x,y: (x,y), my_strings, my_numbers))
print(results1)

scores = [66, 90, 68, 59, 76, 60, 88, 74, 81, 65]
def otlichnik(ball):
    #if ball > 80:
    #    return True
    return ball > 80
print(list(filter(otlichnik,scores)))

dromes = ("demigod", "rewire", "madam", "freer", "anutforajaroftuna", "kiosk")
print(list(filter(lambda word: word[0]==word[-1],dromes)))

from functools import reduce 
# Use map to print the square of each numbers rounded to two decimal places 

my_floats = [4.35, 6.09, 3.25, 9.77, 2.16, 8.88, 4.59]
def func3(a):
    a = round(a**2,2)
    return a
print(list(map(func3,my_floats)))
 # Use filter to print only the names that are less than or equal to seven letters 
my_names = ["olumide", "akinremi", "josiah", "temidayo", "omoseun"] 
print(list(filter(lambda b: len(b) >= 7, my_names)))
# Use reduce to print the product of these numbers 
my_numbers = [4, 6, 9, 23, 5]
print(reduce(lambda a,b: a*b,my_numbers,1))
# # Fix all three respectively. map_result = list(map(lambda x: x, my_floats)) 
# filter_result = list(filter(lambda name: name, my_names, my_names)) 
# reduce_result = reduce(lambda num1, num2: num1 * num2, my_numbers, 0) 
# print(map_result) print(filter_result) print(reduce_result) 
# #### Map from functools import reduce my_floats = [4.35, 6.09, 3.25, 9.77, 2.16, 8.88, 4.59] 
# my_names = ["olumide", "akinremi", "josiah", "temidayo", "omoseun"] 
# my_numbers = [4, 6, 9, 23, 5] 
# map_result = list(map(lambda x: round(x ** 2, 3), my_floats))
#  filter_result = list(filter(lambda name: len(name) <= 7, my_names))
#  reduce_result = reduce(lambda num1, num2: num1 * num2, my_numbers) 
# print(map_result) print(filter_result) print(reduce_result) 
# test_output_contains("[18.922, 37.088, 10.562, 95.453, 4.666, 78.854, 21.068]") 
# test_output_contains("['olumide', 'josiah', 'omoseun']") 
# test_output_contains("24840") success_msg("Congrats! Nice work.")


from http import server
import socket
from urllib import request, response

URLS = {
    '/': 'hello index',
    '/blog': 'hello blog' 
}

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return (method,url)

def generate_headers(method,url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Mehtod not allowed\n\n',405)
    if not url is URLS:  # список все доступных урлов в джанго словарь в фласке список
        return ('HTTP/1.1 404 Not found\n\n',404)
    return ('HTTP/1.1 200 ok\n\n',200)

def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return '<h1>{}</h1>'.format(URLS[url])

def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method,url)
    body = generate_content(code, url)
    return (headers + body).encode()

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # убирает таймаут с повторного запуска программы
    server_socket.bind(('localhost',5000))                              # по умолчанию что о может не дойти и есть 1,5мин таймаут
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept() # возвращает кортеж клиет сокет и адрес
        request = client_socket.recv(1024) # kolvo bite v pakete
        print(request) # .decode('utf-8') можно так в декод виде
        print(addr)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close


if __name__ == '__main__':
    run()
    """

def genetare_nubmers(n,m,prefix=None):
    prefix = prefix or []
    if m == 0:
        print(prefix)
        return
    for digit in range(n):
        prefix.append(digit)
        genetare_nubmers(n,m-1,prefix)
        prefix.pop()

genetare_nubmers(2,2)

def genetare_perestanovki(n,m=-1,prefix=None):
    m = n if m == -1 else m
    prefix = prefix or []
    if m == 0:
        print(*prefix) # печатает список не в скобках а подряд через пробел (можно добавить end='' , sep='')
        return
    for number in range(1, n+1):
        if find(number, prefix):  # ищем есть ли уже текущее n в текущем префиксе
            continue
        prefix.append(number)
        genetare_perestanovki(n,m-1,prefix)
        prefix.pop()

def find(n,prefix):
    for x in prefix:
        if x == n:
            return True
    return False

genetare_perestanovki(3,3)


