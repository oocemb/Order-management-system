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
