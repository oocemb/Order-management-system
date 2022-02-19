""""
from colorama import init
from colorama import Fore, Back, Style
init()

#print( Back.GREEN)
print ('hellonoob')
massiv = list()
try:
    while True:
        print("Посчитать что то? а? а? y/n")
        vhod = input()
        if vhod == "n":
            break
        elif vhod == "y":
            print ('Введите первое число')
            x = int(input())
            print ('Введите второе число')
            y = int(input())
            oper = input ('Что нужно сделать (+,-,/,*)')
            
            if oper == '+':
                z = x + y
            elif oper == '-':
                z = x - y
            elif oper == '/':
                z = x / y
            elif oper == '*':
                z = x * y
            else:
                print('Error')
                break
            print(z)
            massiv.append(str(z))
        else: raise
except:
    massiv = " error"
    print("Ошибка ввода данных")
"""
'''
try:
    somefile = open("hello.txt", "w")
    try:
        somefile.write("hello world")
    except Exception as e:
        print(e)
    finally:
        somefile.close()
except Exception as ex:
    print(ex)
'''
"""
print(massiv)
print (' '.join(massiv))
with open("hello2.txt", "a") as somefile1:
    somefile1.write(' '.join(massiv))
    somefile1.write('\n')
"""
import csv
from os import stat
from tkinter import Y, messagebox

 
FILENAME = "users.csv"
 
users = [
    {"name": "Tom", "age": 28},
    {"name": "Alice", "age": 23},
    {"name": "Bob", "age": 34}
]
 
with open(FILENAME, "w", newline="") as file:
    columns = ["name", "age","qwe"]
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
     
    # запись нескольких строк
    writer.writerows(users)
     
    user = {"name" : "Sam","age":"1","qwe":1}
    # запись одной строки
    writer.writerow(user)
 
with open(FILENAME, "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["name"], "-", row["age"])


import pickle
 
FILENAME = "users.dat"
 
users = [
    ["Tom", 28, True],
    ["Alice", 23, False],
    ["Bob", 34, False]
]
 
with open(FILENAME, "wb") as file:
    pickle.dump(users, file)
 
 
with open(FILENAME, "rb") as file:
    users_from_file = pickle.load(file)
    for user in users_from_file:
        print("Имя:", user[0], "\tВозраст:", user[1], "\tЖенат(замужем):", user[2])

import shelve 

FILENAME = "states2"
with shelve.open(FILENAME) as states: # бинарные файлы с прицнипом словаря МОЖНО МУЛЬТИ ВЛОЖЕННЫЙ
    states["London"] = ["Great Britain",13]
    states["Paris"] = "France"
    states["Berlin"] = "Germany"
    states["Madrid"] = "Spain"
 
with shelve.open(FILENAME) as states: 
    print(states["London"]) # по ключу возвращаем значения
    print(states["Madrid"])
i=0
k=0
with shelve.open(FILENAME) as states:
    for key in states:
        print(key," - ", states[key]) # вывод всего массива
    print(states.get("Moscow","None"))
    for state in states.items(): # вернёт кортежи, можно вернуть ключи или значения (key,value)
        print(state)

import os # создание, удаление, переименование файлов и папок
 
# путь относительно текущего скрипта
#os.mkdir("hello")
# абсолютный путь
#os.mkdir("c://somedir")
#s.mkdir("c://somedir/hello")

#filename = input("Введите путь к файлу: ")
#if os.path.exists(filename):
#    print("Указанный файл существует") 
#else:
#    print("Файл не существует") 

'''
text = "Hello, {first_name}.".format(first_name="Tom")
print(text)     # Hello, Tom.
 
info = "Name: {name}\t Age: {age}".format(name="Bob", age=23)
print(info)     # Name: Bob  Age: 23

info = "Name: {0}\t Age: {1}".format("Bob", 23)
print(info)     # Name: Bob  Age: 23
#При этом аргументы можно вставлять в строку множество раз:
text = "Hello, {0} {0} {0}.".format("Tom")
'''
"""
number = 23.8589578
print("{:.2f}".format(number))   # 23.86

print("{:10.2f}".format(23.8589578))    #     23.86
print("{:8d}".format(25))               #      25
#Для вывода процентов лучше воспользоваться кодом "%":


number = .12345
print("{:7.2%}".format(number))        # 12.345000%
print("{:15.0%}".format(number))      # 12%
print("{:15.1%}".format(number))      # 12.3%
"""

class Person:
    def __init__(self, name, age):
        self.__name = name  # устанавливаем имя
        self.__age = age  # устанавливаем возраст
 
    @property
    def name(self):
        return self.__name
 
    @property
    def age(self):
        return self.__age
 
    @age.setter
    def age(self, age):
        if age in range(1, 100):
            self.__age = age
        else:
            print("Недопустимый возраст")
 
    def display_info(self):
        print("Имя:", self.__name, "\tВозраст:", self.__age)
 
 
class Employee(Person):
    # определение конструктора
    def __init__(self, name, age, company):
        Person.__init__(self, name, age)
        self.company = company
 
    # переопределение метода display_info
    def display_info(self):
        Person.display_info(self)
        print("Компания:", self.company)
 
 
class Student(Person):
    # определение конструктора
    def __init__(self, name, age, university):
        Person.__init__(self, name, age)
        self.university = university
 
    # переопределение метода display_info
    def display_info(self):
        print("Студент", self.name, "учится в университете", self.university)
 
people = [Person("Tom", 23), Student("Bob", 19, "Harvard"), Employee("Sam", 35, "Google")]
 
for person in people:
    person.display_info()
    print()

"""
from tkinter import *
from tkinter import messagebox
clicks = 0
def click_button():
    global clicks
    clicks += 1
    #root.title("Clicks - {}".format(clicks))
    button_text.set("Clicks - {}".format(clicks))
    #btn.config(text="Clicks {}".format(clicks)) # изменение просто через функцию Конфига
def show_message():
    messagebox.showinfo("ФИО", "Имя {} ФИО {}".format(message.get(),message2.get()))

root = Tk()
root.title("Графическая программа на Python")
root.geometry("400x300+300+250")
button_text = StringVar()
button_text.set("Clicks - {}".format(clicks))

btn = Button(
    textvariable=button_text,
    background="#425",
    foreground="#ccc",
    padx="25",
    pady="5",
    font="16",
    highlightcolor="#222",
    relief=RIDGE,
    command=show_message) #SUNKEN, RAISED, GROOVE, RIDGE
#btn.pack(fill=X, side=BOTTOM)
btn.place(relx=.3, rely=.3, anchor="c", height=300, width=130, bordermode=OUTSIDE)

message = StringVar()
message_entry = Entry(textvariable=message)
message_entry.place(relx=.5, rely=.1, anchor="c")
message2 = StringVar()
message_entry = Entry(textvariable=message2)
message_entry.place(relx=.5, rely=.3, anchor="c")

#for r in range(5):
#    for c in range(5):
#        btn = Button(text="None")
#        btn.grid(row=r,column=c,ipadx=5,ipady=5,padx=1,pady=1)
 
poetry = "Вот мысль, которой весь я предан,\nИтог всего, что ум скопил.\nЛишь тот, кем бой за жизнь изведан,\nЖизнь и свободу заслужил."
label2 = Label(text=poetry, justify=RIGHT,anchor="nw")
label2.place(relx=.45, rely=.75)
root.mainloop()"""
"""
from tkinter import *
from tkinter import messagebox
 
 
def clear():
    name_entry.delete(0, END)
    surname_entry.delete(0, END)
 
 
def display():
    messagebox.showinfo("GUI Python", name_entry.get() + " " + surname_entry.get())
 
root = Tk()
root.title("GUI на Python")
 
name_label = Label(text="Введите имя:")
surname_label = Label(text="Введите фамилию:")
 
name_label.grid(row=0, column=0, sticky="w")
surname_label.grid(row=1, column=0, sticky="w")
 
name_entry = Entry()
surname_entry = Entry()
 
name_entry.grid(row=0,column=1, padx=5, pady=5)
surname_entry.grid(row=1,column=1, padx=5, pady=5)
 
# вставка начальных данных
name_entry.insert(0, "Tom")
surname_entry.insert(0, "Soyer")
 
display_button = Button(text="Display", command=display)
clear_button = Button(text="Clear", command=clear)
 
display_button.grid(row=2, column=0, padx=5, pady=5, sticky="e")
clear_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")

ismarried = IntVar()
 
ismarried_checkbutton = Checkbutton(text="Женат/Замужем", variable=ismarried)
ismarried_checkbutton.grid(row=3, column=0)
 
ismarried_label = Label(textvariable=ismarried)
ismarried_label.grid(row=3, column=1)

lang = IntVar()
 
python_checkbutton = Radiobutton(text="Python", value=1, variable=lang, padx=15, pady=10)
python_checkbutton.grid(row=4, column=0, sticky=W)
 
javascript_checkbutton = Radiobutton(text="JavaScript", value=2, variable=lang, padx=15, pady=10)
javascript_checkbutton.grid(row=5, column=0, sticky=W)
 
selection = Label(textvariable=lang, padx=15, pady=10)
selection.grid(row=6, column=0, sticky=W)
 
root.mainloop()"""
"""
from tkinter import *
 
languages = ["Python", "JavaScript", "C#", "Java", "C/C++", "Swift",
             "PHP", "Visual Basic.NET", "F#", "Ruby", "Rust", "R", "Go",
             "T-SQL", "PL-SQL", "Typescript"]
 
root = Tk()
root.title("GUI на Python")
 
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
 
languages_listbox = Listbox(yscrollcommand=scrollbar.set, width=40, selectmode=MULTIPLE)
 
for language in languages:
    languages_listbox.insert(END, language)
 
languages_listbox.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=languages_listbox.yview)

root.mainloop()"""
"""
from tkinter import *
 
 
# удаление выделенного элемента
def delete():
    selection = languages_listbox.curselection()
    # мы можем получить удаляемый элемент по индексу
    # selected_language = languages_listbox.get(selection[0])
    languages_listbox.delete(selection[0])
 
 
# добавление нового элемента
def add():
    new_language = language_entry.get()
    languages_listbox.insert(0, new_language)
 
root = Tk()
root.title("GUI на Python")
 
# текстовое поле и кнопка для добавления в список
language_entry = Entry(width=40)
language_entry.grid(column=0, row=0, padx=6, pady=6)
add_button = Button(text="Добавить", command=add).grid(column=1, row=0, padx=6, pady=6)
 
# создаем список
languages_listbox = Listbox()
languages_listbox.grid(row=1, column=0, columnspan=2, sticky=W+E, padx=5, pady=5)
 
# добавляем в список начальные элементы
languages_listbox.insert(END, "Python")
languages_listbox.insert(END, "C#")
 
delete_button = Button(text="Удалить", command=delete).grid(row=2, column=1, padx=5, pady=5)
 
root.mainloop()
"""
"""
from tkinter import *
def display():
    messagebox.showinfo("Что меняем бро?")

root = Tk()
root.title("GUI на Python")
root.geometry("300x250")
 
main_menu = Menu()
 
file_menu = Menu(tearoff=0)
file_menu.add_command(label="New")
file_menu.add_command(label="Save")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Exit")
 
 
main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Edit")
main_menu.add_cascade(label="View",command=display)
 
root.config(menu=main_menu)
 
root.mainloop()"""

class Base:
    def __init__(self, x):
        self.x = x
    def show(self):
        print('Base', self.x)


class Dev(Base):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y

class Mev(Dev):
    def __init__(self, x, y):
        super().__init__(x, y)