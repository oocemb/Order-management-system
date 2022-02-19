from email import message


class Blabla(Exception):
    print('wtf?')

def coroutine(func):
    def inner(*args,**kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g 
    return inner
'''
@coroutine
def average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
            break
        except Blabla:
            print('Blabla')
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)
            #print(average)

    return average

try:
    g = average()
    #next(g) # нужно отправить значение none чтобы запустить генератор (или g.send(None))
    g.send(5)
    g.send(25)
    g.throw(Blabla)
    g.throw(StopIteration)
except StopIteration as stop:
    print('last average', stop.value) # в велью значение из ретёрна в цикле
'''

#@coroutine
def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            print('end1')
            break
        except Blabla:
            print('blabla')
        else:
            print('Opopop', message)
    return 'Return from subg'


@coroutine
def delegator(subg):
    result = yield from subg    # содержит инициализацию сенд(ноне), можно убрать декоратор с субген
    '''
    while True:
        try:
            data = yield
            subg.send(data)      
        except StopIteration:
            print('end2')
        except Blabla as stop1:
            subg.trow(stop1)
    '''
    print(result)

try:
    sg = subgen()
    g = delegator(sg)
    g.send('lala')
    sg.send('lala')
    g.throw(StopIteration)
except: pass
