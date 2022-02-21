# def around_fib(n):
#     f1=0
#     f2=1
#     for i in range(1,n):
#         f2, f1 = (f1 + f2), f2
#     return f2

# strf2=list(str(around_fib(666)))

# dict = {i:0 for i in range(10)}
# for i in range(0,len(strf2)):
#     dict[int(strf2[i])] += 1

# maxcnt=dict[0]
# key = 0
# for n in range(1,10):
#     if dict[n]>maxcnt:
#         maxcnt = dict[n]
#         key = n
# if len(strf2)%25 == 0: chunk = 25;
# else: chunk = -(len(strf2)%25)
# print("Last chunk {}; Max is {} for digit {}".format(''.join(strf2[chunk:]),maxcnt,key))
# print(dict)
# print(maxcnt, key)
# print(around_fib(100))

# def split(x):
#     if x.split("x")[0] == "-": return "-1"
#     if x.split("x")[0] == "": return "1"
#     return x.split("x")[0]

# def differentiate(poly):
#     if "x" not in poly: return "0"
#     if "^" not in poly: 
#         return split(poly)
#     a = int(poly.split('^')[-1])
#     b = int(split(poly))
#     return str(a*b)+"x"+"^"+str(a-1) if a-1 != 1 else str(a*b)+"x"

# print(differentiate("7x"))

# def histogram(values, bin_width):
#     dict = {i:0 for i in range(max(values)+1)}
#     for i in range(0,len(values)):
#         dict[values[i]] += 1
#     n,cnt=0,0
#     result=[0]
#     for y in range(0,len(dict)):
#             cnt+=1  
#             result[n] += dict[y]
#             if cnt%bin_width == 0 and y+1!=len(dict): result.append(0); n+=1
#     print(result)

# histogram([1, 1, 0, 1, 3, 2, 6], 1)

# room=["+-----123---+",
#       "|           |",
#       "|           |",
#       "|    UUUU   |",
#       "|           |",
#       "+-----------+"]

# leftwall,rightwall = [],[]
# for i in range(len(room)):
#     leftwall.append(room[i][0])
#     rightwall.append(room[i][len(room[0])-1])
# upwall = list(room[0])
# downwall = list(room[-1])
# expected = [0]*10
# def run(w1,w2,w3,w4,w5):
#     walls = w1+w2+w3+w4+w5
#     for i in range(0,len(walls)):
#         print(walls[i], end="")
#         if walls[i] != '|' and walls[i] != '-' and walls[i] != '+': return int(walls[i])

# for y in range (1,len(room)-1):
#     for x in range(1,len(room[0])):
#         if room[y][x] == 'U':
#             expected[run(upwall[x::-1],leftwall,downwall,rightwall[::-1],upwall[:x:-1])] +=1
#         elif room[y][x] == 'D':
#              expected[run(downwall[x:],rightwall[::-1],upwall[::-1],leftwall,downwall[0:x])] +=1
#         elif room[y][x] == 'R':
#             expected[run(rightwall[y::-1],upwall[::-1],leftwall,downwall,rightwall[:y:-1])] +=1
#         elif room[y][x] == 'L':
#             expected[run(leftwall[y:],downwall,rightwall[::-1],upwall[::-1],leftwall[0:y])] +=1
        
# print(expected)

# def f(n):
#     nums=[2]
#     for n in range(2,n):
#         flag = True
#         for num in nums:
#             if n%num == 0:
#                 flag = False
#                 break
#         if flag: nums.append(n)
#     print(len(nums))
# f(199)

# def Arr(N,k):
#     lensubN = len(N)//k
#     subN=[[0 for i in range(lensubN)] for j in range(k)]
#     for i in range(len(N)%k):
#         subN[i].append(0)
#     z=0
#     for i in range(k):
#         for j in range(len(subN[i])):
#             subN[i][j] = N[z]
#             z+=1
#     print(subN)
 
# Arr([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],7)
# Arr([1,2,3,4,5,6,7,8,9,10],4)
# Arr([1,2,3,4,5,6,7],2)

# def str(str):
#     if len(str.split()) > 1: return print('{} False'.format(str))
#     if str[0] == " " or str[-1] == " ": return print('{} False'.format(str)) # можно использовать strip
#     hi = 0
#     for i in str:
#         if i.isdigit(): return print('{} False'.format(str))
#         if not i.islower():
#             hi +=1
#             if hi > 1: return print('{} False'.format(str))
#     return True if hi == 1 else print('{} False'.format(str))


# str("Мама")
# str("аTТо")
# str("гриБ1")
# str('Яблоко')

# def count_letter(words,letter):
#   i = 0
#   for word in words:
#     for w in word:
#       if w == letter:
#         i += 1
#         break
#   return print(i)

# count_letter(['python', 'c++', 'c', 'scala', 'java'],"a")


# import random
# from tkinter import Y
# a = []
# LENGTH_a = 50
# y = 1000
# a = [random.randrange(1,1000,1) for i in range(LENGTH_a)]
# print(a)
# for i in range(LENGTH_a):
#     if a[i]%6 > 0:
#         y_curent = a[i]     
#         if y_curent < y:
#             y = y_curent
# for i in range(LENGTH_a):
#     if a[i]%6 > 0:
#         a[i] = y
# print(a)

# def rot13(message):
#     alpha = 'abcdefghijklmnopqrstuvwxyz'
#     message = list(message)
#     for i in range(len(message)):
#         flag=False
#         if message[i].isalpha() and message[i].isupper():
#             flag=True
#             message[i] = message[i].lower()
#         for j in range(len(alpha)):
#             if message[i]==alpha[j]:
#                 if flag: 
#                     message[i] = alpha[(j+13)%len(alpha)].upper()
#                     break
#                 message[i] = alpha[(j+13)%len(alpha)]
#                 break
#     return print(''.join(message))

# rot13('qweQQwwW')

# def up_array(arr):
#     for i in range(len(arr)):
#         if arr[i] < 0: return None
#         arr[i] = str(arr[i])
#     arr = list(str(int(''.join(arr))+1))
#     for i in range(len(arr)):
#         arr[i] = int(arr[i])
#     return arr
# up_array([5,7,4])

# def done_or_not(board):
#     for i in range(len(board)):
#         if len(set(board[i])) < 9: return "Try again!"
#         if len({board[j][i] for j in range(len(board))}) < 9: return "Try again!"
#     for i in range(3):
#         for j in range(3):
#             for k in range(3):
#                 set1=set()
#                 set1=set1.union({board[i*3+k][j*3] for k in range(3)},{board[i*3+k][j*3+1] for k in range(3)},{board[i*3+k][j*3+2] for k in range(3)})
#                 print(set1)
#             if len(set1) < 9: return "Try again!"
#     return "Finished!"

# done_or_not([[1, 3, 2, 5, 7, 9, 4, 6, 8]
#             ,[4, 9, 8, 2, 6, 1, 3, 7, 5]
#             ,[7, 5, 6, 3, 8, 4, 2, 1, 9]
#             ,[6, 4, 3, 1, 5, 8, 7, 9, 2]
#             ,[5, 2, 1, 7, 9, 3, 8, 4, 6]
#             ,[9, 8, 7, 4, 2, 6, 5, 3, 1]
#             ,[2, 1, 4, 9, 3, 5, 6, 8, 7]
#             ,[3, 6, 5, 8, 1, 7, 9, 2, 4]
#             ,[8, 7, 9, 6, 4, 2, 1, 5, 3]])


# def dirReduc(arr):
#     Flag=True
#     while Flag:
#         Flag=False
#         if len(arr) == 0: return []
#         for i in range(1,len(arr)):
#             if Flag: break
#             for x,y in zip(('NORTH','SOUTH','WEST','EAST'),('SOUTH','NORTH','EAST','WEST')):
#                 if arr[i] == x and arr[i-1] == y:
#                     arr.pop(i)
#                     arr.pop(i-1)
#                     Flag=True
#                     break
#     return arr

# print(dirReduc(["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]))

# def next_bigger(n):
#     if n < 10 or list(str(n))[::-1] == sorted(list(str(n)[::-1])): return -1
#     n = list(str(n))
#     for i in range(len(n)-1,0,-1):   
#         if n[i] > n[i-1]:
#             n =n[:i]+sorted(n[i:])
#             for j in range(i,len(n)): 
#                 if n[i-1] < str(int(n[j])): 
#                     n[i-1],n[j]=n[j],n[i-1]
#                     return int("".join(n))

# next_bigger(551321)
# next_bigger(552983)
# next_bigger(555983)

# def rgb(r, g, b):
#     a=[r,g,b]
#     for i in range(len(a)):
#         if a[i]<0: a[i] = 0
#         if a[i]>255: a[i] = 255
#         a[i]=str(hex(a[i]))[2:].upper()
#         if len(a[i]) == 1: a[i]='0'+a[i]
#     return ''.join(a)
# print(rgb(148,0,211))

# def rgb2(r,g,b):
#     round = lambda x: min(255, max(x,0))
#     return "{:02X}{:02X}{:02X}".format(round(r),round(g),round(b))
# print(rgb2(148,0,211))

# import re

# def top_3_words(text):
#     counter = {}
#     text = re.sub('[,]', ' ',text)
#     text = re.sub(r'[^a-z,\']', ' ', text.lower()).split()
#     for txt in text:
#         txt = re.sub('[\']','Z',txt)
#         if not txt.isalpha(): continue
#         txt = re.sub('[Z]','\'',txt)
#         if set(txt) == {"'"}: continue
#         counter[txt] = int(counter.get(txt) or 0) + 1
#     list=[]
#     for i in range(len(counter)):
#         key1 = sorted(counter, key=counter.__getitem__)[-1]
#         list.append(str(key1))
#         if len(list) == 3: return list
#         counter.pop(key1)
#     return list

# print(top_3_words("  //wont Won't wOn't "))
# print(top_3_words("e e e e DDD ddd 7DdD: ddd7ddd ddd aa aA7Aa, bb cc cC e e e"))
# from collections import Counter
# def top_3_words(text):
#     c = Counter(re.findall(r"(?=.*[a-z])[a-z']+", text.lower()))
#     return [w for w, _ in c.most_common(3)]

# import timeit

# code = """
# def f(n):
#     nums=[2]
#     for n in range(2,n):
#         flag = True
#         for num in nums:
#             if n%num == 0:
#                 flag = False
#                 break
#         if flag: nums.append(n)
#     return nums
# f(423727)
# """
# # time1 = timeit.timeit(code, number=10)/10 
# # print(time1) # очень долго..... плохой код


# code2 = """
# def primfacs(n):
#    i = 2
#    primfac = set()
#    while i * i <= n:
#        while n % i == 0:
#            primfac.add(i)
#            n //= i
#        i += 1
#    if n > 1:
#        primfac.add(n)
#    return primfac

# def sum_for_list(lst):
#     arr = {}
#     d = 2
#     ps = set()
#     for num in lst:
#         for p in primfacs(abs(num)):
#             if num%p == 0:
#                 arr[p] = int(arr.get(p) or 0) + num
#     return [list(b) for b in sorted(arr.items())]

# print(sum_for_list([15,210000,744721,30,-45]))
# """
# time1 = timeit.timeit(code2, number=10)/10 
# print(time1)

# def sum_for_list(lst):
#     arr = {}
#     for num in lst:
#         p = 2
#         m = abs(num)
#         while p*p <= m:
#             t = 0
#             while m % p == 0:
#                 if t < 1: arr[p] = int(arr.get(p) or 0) + num
#                 m //= p
#                 t += 1
#             p += 1
#         if m > 1: arr[m] = int(arr.get(m) or 0) + num
#     return [list(b) for b in sorted(arr.items())]

# print(sum_for_list([15,210000,744721,30,-45]))

# def genetare_perestanovki(n,m=-1,prefix=None):
#     m = n if m == -1 else m
#     prefix = prefix or []
#     if m == 0:
#         print(*prefix) # печатает список не в скобках а подряд через пробел (можно добавить end='' , sep='')
#         return
#     for number in range(0, n+1):
#         if find(number, prefix):  # ищем есть ли уже текущее n в текущем префиксе
#             continue
#         prefix.append(number)
#         genetare_perestanovki(n,m-1,prefix)
#         prefix.pop()

# def find(n,prefix):
#     for x in prefix:
#         if x == n:
#             return True
#     return False

# def u3(str1):
#     answer = str1.split(" + ")[-1].split(" = ")[-1]
#     example = str1.split(" + ")[:-1] 
#     example.append(str1.split(" + ")[-1].split(" = ")[0])
#     letts = {i for i in str1 if i.isupper()}
#     dict = {let:i for i,let in enumerate(letts)}
#     genetare_perestanovki(9,len(letts))
#     an,ex = 1,2
#     while an != ex:
#         for i in range(len(example)):
#             example[i] = [dict[j] for j in example[i]]
#         answer = [dict[j] for j in answer]
#         an = int(''.join(map(str,answer)))
#         ex = sum([int(''.join(map(str,exam))) for exam in example])
#     return answer,example,letts,dict,an,ex

# print(u3("ELEVEN + NINE + FIVE + FIVE = THIRTY"))

