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
        return ('HTTP/1.1 405 Mehtod not allowed\n\n',405) # \n\n отделение заголовка от тела ответа
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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # перый порт IP(4 по умочнию) втрой TCP
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