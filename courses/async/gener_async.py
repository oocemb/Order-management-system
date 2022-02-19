from asyncio import tasks
from pydoc import cli
import socket
from select import select
from urllib import response

tasks = []
to_read = {}
to_write = {}

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # перый прмрт IP(4 по умочнию) втрой TCP
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # убирает таймаут с повторного запуска программы
    server_socket.bind(('localhost',5001))                              # по умолчанию что о может не дойти и есть 1,5мин таймаут
    server_socket.listen()

    while True:
        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()
        print('connect',addr)
        tasks.append(client(client_socket))

def client(client_socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)
        print('client1')
        if not request:
            break
        else:
            response = 'Hello noob\n'.encode()
            print('client2')
            yield ('write',client_socket)
            client_socket.send(response)
            print('client resp')
    client_socket.close()

def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock)) # значение ключа с сокетом является генератор и он добавл в таск
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
        try:
            task = tasks.pop(0)
            reason, sock = next(task)
            if reason == 'read':
                to_read[sock] = task    
            if reason == 'write':
                to_write[sock] = task
        except: pass

tasks.append(server())
event_loop()  
