"""Функция Левенштейна определение минимального редакционного растояние между двумя строками"""
def levenstein(A,B):
    F=[[(i+j) if i*j==0 else 0 for j in range(len(B)+1)] for i in range(len(A)+1)]
    for i in range(1, len(A)+1):
        for j in range(1, len(B)+1):
            if A[i-1]==B[j-1]:
                F[i][j]=F[i-1][j-1]
            else:
                F[i][j]=1+min(F[i-1][j],F[i][j-1],F[i-1][j-1])
    print(F[-1][-1])

levenstein('boommabmaboba','ooobammbaoboba3') # не правильно работает....
# правильно если не считать действием перестановку символов в одной строке местами


"""Функция проверки равенства строк""" # есть вероятоностная проверка каждый 5 символ для длинных
def equally_srt(A,B):
    if len(A)==len(B):
        for i in range(len(A)):
            if A[i]!=B[i]:
                return False
    else: return False

"""Поиск подстроки в строке"""
#def search_substr(str,substr): 
#    for i in range(0,len(str)-len(substr)):
#       if equal(str[i:i+len(substr),substr]):
#            print(i)

#Префикс функция Pi 'П' строки
#П - Длина максимального собственн суфикса(не равный самой строке) который является префиксом
'''def pi_f(str):
    pass

def prefix_str(A):
    prefix = [0 for i in range(len(A)+1)]
    for i in range(len(A)):
        p = pi_f[i-1]
        while p > 0 and A[i]!=A[p+1]:
            p = prefix[p]
            if A[i]==A[p+1]:
                p += 1
        prefix[i] = p
    print(prefix)
    return prefix

prefix_str('asdasdqweqwedsa')
'''

# Стэк stack LIFO (Last in First out) 
# push - засунуть в стэк / pop - вытащить из стэка / size - сколько всего
# top - верхний элемент / is_empty - пуст ли стэк (bool)
# clear() очистить стэк
# проверка корректности скобочной последовательности
# A = ''  B = (A)  C = AB (((())))( ) - корект  ()))((()- некоректн
# n - незакрытых скобок
# считать текущее кол-во открытых скобок и по ходу проверять как только отрицательное число то некоректн
# в конце должно остаться в нуле 

# 2 вида скобок ()[]  - корр [(]) - некорр
# для каждой очередной скобки - если она открывающ тогда её запоминаем в стэк
# если она закрывающая и стэк пуст - некоректно, 
# иначе pop() соответств ')' or ']' норм, если нет - плохо
# если стэк в конце пуст то норм иначе нет
import doctest
from os import access
from turtle import distance, right
from urllib import response
def check(S):
    """
    Проверяет корр скоб
    >>> check('(())[][]')
    True
    >>> check('[)]')
    0
    >>> check('[(])')
    False
    """
    stack = []
    for brace in S:
        if brace not in "()[]":
            continue
        if brace in "([":
            stack.append(brace)
        else:
            assert brace in ")]", 'Error! ожидали закрыв скобку'
            if len(stack)==0:
                return False
            left = stack.pop()
            if left == '(':
                right = ')'
            elif left == '[':
                right = ']'
            else:
                assert 'Vse ne tak opiat'
            if right != brace:
                return False
    if len(stack)==0:
        return True
    else:
        return False

print(check('qweqwe(([()_qwe()]))'))
#doctest.testmod(verbose=False)

# list -(это не массив), это список ссылок
# кортеж может хранить ссылку на список, т.е. будет внутри имя ссылок а обьект на который ссылаются может поменяться
A=[True, 2, 5.3, 'Hello']
B=(True, 2, 5.3, A)

C=[(1,2),(3,6),(7,5)]
for x,y in C:
    print(x,y)

s = 'Hello'
s.find('lo')
x = s.count('l')
t= s.replace('llo','ll') # ничего не сделает строка не изменяемая -- надо куда то сохранять
print(s,t)
z = s[::2]+s[::-2]
# в числах с новых версий можно x = 9999_8888_4444_2222 (просто как разделители для удобств)
#s[start:stop:step]
#s[0::2]
#s[::4]
#s[:]
# удобно для списков
A=[0,1,2,3,4]
B = A[1:3] # не меняет А присваивать чему то чтоб пользовать, но емко по памяти!!!! c 2 по 4 эл-т
С = A[::-1] # в обратную сторону отсортирует
# через срез можно вставить в середину списка больше элементов чем в среде
A[1:2]=[555,555,666,777,888]
# срезы с 2мя парам-рами всё норм никогда нет ошибок только 3й  step можно налажать двойным включ
print(A)
#A[::3]=[1,3,5,6]  - Error длина не равна

#sum = sum(A)
#min = min(A)
#max = max(A)
# reduce - пришвартовать какую то **часть** ко всему списку по порядку

# Список строк
# A = str.split() ' ' default 
# a.upper(), lower(), 
# stroka = '-'.join(A)  # A - список строк 

#Укладка рюкзака (минимальный вес при максимальной стоимости) (МР полная)
# 2**n  выборок при полном переборе(единственный точный способ)
N = 10 # кол-во предметов
M = [10,2,3,4,5,6,7,8,9,10] # масса предметов
V = [5,7,4,1,3,3,6,3,2,22]
MAX_M = 20  # масса рюкзака
F=[[0]*(N+1) for i in range(MAX_M+1)]
for i in range(0,N):           # ищем максимум по всем кол-вам предметов
    for k in range(1,MAX_M+1):   # по всем возможным массам
        if M[i] <= k:            # проверяем текущий элемент поместиться ли в обьём если да то
            F[k][i]=max(F[k][i-1], V[i]+F[k-M[i]][i-1])
            #print(F[k][i])       
        else:
            F[k][i]=F[k][i-1]
print(F[MAX_M][N-1])

# Именованные кортежи
import collections 
Point1 = collections.namedtuple('Point1', 'x y z')
A = Point1(1,2,3)
print(A.x) # 1  # но т.к. это кортеж он не изменяемый надо создавать новый если что
# A.x = 5  # Error

# Связный список (односвязный) лучше чем обычный при ооочень длинных списках и вставка в начало
a=[1]
a.append([2])
#a[1].append([3,a])
a[1].append([3,None])
p=a 
while p is not None:
    print (p[0])
    p=p[1]

class LinkedList: # можно добавить итерации
    def __init__(self):
        self._begin = None
    def insert(self,x):
        self._begin = [x,self._begin]
    def pop(self):
        assert self._begin is not None, 'List empty!'
        z = self._begin[0]
        self._begin = self._begin[1]
        return z
    
# Класс куча (пирамида) (слегка упорядоченное двоичное дерево)
class Heap:
    def __init__(self) -> None:
        self._values = []
        self._size = 0
    def insert(self,x):
        self._values.append(x)
        self._size += 1
        self.sift_up(self._size-1)
    def sift_up(self, i):
        while i!=0 and self._values[i] < self._values[(i-1)//2]:
            self._values[(i-1)//2], self._values[i] = self._values[i], self._values[(i-1)//2]
    def extract_min(self):
        #assert if not self._size, 'List empty!'
        tmp = self._values[0]
        self._values[0]=self._values[-1]
        self._values.pop()
        self._size -= 1
        self.sift_down(0)
        return tmp
    def sift_down(self,i):
        while (2*i+1) > self._size:
            if self._values[2*i+1] < self._values[i]:
                j = 2*i + 1
            if 2*i+2 < self._size and self._values[2*i+2] < self._values[j]:
                j = 2*i + 2
            if i == j:
                break
            self._values[j], self._values[i] = self._values[i], self._values[j]

# Хэш таблица не сохраняет порядок элементов (куда положить номер ячейки вычисляет функция от значения внутри ячейки)
# могут случатся колизии(совпадение номеров для разных значений)
# 2 варианта решения 
# Открытая храним в массиве - список значений для совпадающих номеров
# Зактырая адресация:
# Линейная адресация - класть совпадающие в следующую свободную или  со сдвигом или квадратичная
# 
# Двойное хэширование(
# хэш фун-я(сложность вычисл, разрядность вых данных, криптостойкость)


# Очередь Queue (FIFO) (First in First out FIFO)
from collections import deque
queue = deque(range(1000000))
queue.append(1)
queue.popleft() # быстрее работает чем лист 
'''
# Работа с графами
N,M = map(int, input().split())   # map применяет инт к числам в списке после инпут.сплита
graph = {i: set() for i in range(N)}
for i in range(M):
    v1,v2 = map(int, input().split())
    graph[v1].add(v2)
    graph[v2].add(v1)
# считали граф в словарь { i : {a,b}, i+1, {c,d},....}
distances = [None]*N
start_vertex = 0
queue = deque([start_vertex])
while queue:
    cur_v = queue.popleft()
    for neigh_v in graph[cur_v]:
        if distances[neigh_v] is None:
            distances[neigh_v] = distances[cur_v] + 1
            queue.append(neigh_v)
# 
end_vertex=9
parents = [None] * N
path = [end_vertex]
parent = parents[end_vertex]
while not parent is None:
    path.append(parent)
    parent = parents[parent]
'''
# Поход коня в определённую клетку - всего 64 вершины и рёбра будут соединенем туда куда может ходить
letters = 'abcdefgh'
numbers = '12345678'
graph = dict()
for l in letters:
    for n in numbers:
        graph[l+n] = set()

def add_edge(v1,v2):
    graph[v1].add(v2)
    graph[v2].add(v1)

for i in range(8):
    for j in range(8):
        v1 = letters[i]+numbers[j]
        if 0 <= i + 2 < 8 and 0 <= j + 1 < 8:
            v2 = letters[i+2] + numbers[j+1]
            add_edge(v1,v2)
        if 0 <= i - 2 < 8 and 0 <= j + 1 < 8:
            v2 = letters[i-2] + numbers[j+1]
            add_edge(v1,v2)
        if 0 <= i + 1 < 8 and 0 <= j + 2 < 8:
            v2 = letters[i+1] + numbers[j+2]
            add_edge(v1,v2)
        if 0 <= i - 1 < 8 and 0 <= j + 2 < 8:
            v2 = letters[i-1] + numbers[j+2]
            add_edge(v1,v2)
#print(graph)
#копируем код
distances = {v:None for v in graph}
parents = {v:None for v in graph}
start_vertex = 'a5'
end_vertex = 'b4'
distances[start_vertex] = 0
queue = deque([start_vertex])

while queue:
    cur_v = queue.popleft()
    for neigh_v in graph[cur_v]:
        if distances[neigh_v] is None:
            distances[neigh_v] = distances[cur_v] + 1
            parents[neigh_v] = cur_v
            queue.append(neigh_v)

path = [end_vertex]
parent = parents[end_vertex]
while not parent is None:
    path.append(parent)
    parent = parents[parent]

print(path[::-1])

#Наименьшнее расстояние между 2 людьми VK
import requests
import time
from tqdm import tqdm

HOST = 'https://api.vk.com/method/'
VERSION = '5.74' # 2018 year
access_token = 'qweqweqedvdfv2323f3v3rv2342f24'

r = requests.get(HOST +'user.get', params={'user_ids':'1231,1', 'access_token':access_token, 'v':VERSION})

print(r.json()['response'][0]) # принимаем файл джсон
id_start = 111900610
id_end = 1699912
def get_friends_list(id_user):
    r = requests.get(HOST +'friends.get', params={'user_id':id_user, 'access_token':access_token, 'v':VERSION})
    if 'response' in r.json():
        return r.json()['response']['items']
    return []

queueVK = deque(get_friends_list(id_start))
distancesVK = {v:1 for v in queueVK}
parentsVK = {v:id_start for v in queueVK}

while id_end not in distancesVK:
    cur_user = queueVK.popleft()
    new_users = get_friends_list(cur_user)
    time.sleep(0.2)
    for u in tqdm(new_users):
        if u not in distancesVK:
            queueVK.append(u)
            distancesVK[u] = distancesVK[cur_user] + 1
            parentsVK[u] = cur_user

pathVK = [id_end]
parent = parentsVK[id_end]
parentsVK[id_start] = None
while not parent is None:
    pathVK.append(parent)
    parent = parents[parent]

print(pathVK[::-1])


# Алгоритм дейкстры (поиск кратч. расстояния до всех вершин) во взвешенном графе 
# Требование : Веса - положительные числа

def read_graph():
    M = int(input()) # кол-во ребер, далее - строки А Б вес
    graphdijksrta = {}
    for i in range(M):
        a,b, weight = input().split()
        weight = float(weight)
        add_edgedijksrta(graphdijksrta, a, b, weight)
        add_edgedijksrta(graphdijksrta, b, a, weight)
    return graphdijksrta

def add_edgedijksrta(G, a, b, weigth):
    if a not in G:
        G[a] = {b:weigth}
    else:
        G[a][b] = weigth

def dijksrta(G, start):
    queueDIJ = deque([start])
    s = {}
    s[start] = 0
    while queueDIJ:
        current_V = queueDIJ.popleft()
        for u in G[current_V]:
            if u not in s or s[current_V]+G[current_V][u] < s[u]:
                s[u] = s[current_V] + G[current_V][u]
                queueDIJ.push(u)

def reveal_shortest_path(): # восстановить путь на основе вычитания с конца () 12 - 5 = 6 ()
    pass

def main():
    G = read_graph()
    start = input ('С какой вершины начать')
    #assert start in G 'Error, net nakoi vershini'
    while start not in G:
        start = input ('Error, С какой вершины начать')
    shortest_dist = dijksrta(G, start)
    finish = input ('До какой вершины путь построить')
    while finish not in G:
        finish = input ('Error, С какой вершины начать')
    shortest_path = reveal_shortest_path(G, start, finish, shortest_dist)

# Флойд-Уоршел ( Асимпт = N**3 ) Работает с отрицательными весами, но не с циклами отриц веса
# но может как раз детектировать цикл отриц веса, (много матриц )

###################################

# Двоичные деревья поиска
# ДДП это структура данных где в вершинах хранят элементы содержащие ключ 
# key in KEYS, при этом есть key1<key2
# в левую младшие в правую старшие
# должно быть правильным и сбалансированным
# баланс - левое и правое поддерево отличается на ~1
# Малый *левый* поворот
# Большой *правый* поворот
# 
# АВЛ ддп
# Красно-чёрное ддп

class Node:
    def __init__(self,key,value) -> None:
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
    