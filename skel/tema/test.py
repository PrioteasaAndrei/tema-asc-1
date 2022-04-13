

# flag = 0 

# for i in range(10):
#     print('I',i)
#     if i == 0 and flag == 0:
#         i-=1
#         flag = 1
#     else:
#         print(i)


import queue


iter = 0
flag = 0
while iter < 10:
    if iter == 0 and flag == 0:
        iter -=1
        flag = 1
    else:
        print(iter)
    
    iter +=1


lista = [10,20,30,40,50,60,70,80]


# flag_2 = 0
# for item in lista:
#     while True:
#         if item == 40:
#             break

#     print(item)



a = queue.Queue(-1)
a.put(1)
a.put(2)
a.put(3)
a.put(4)


lista = [] 


while not a.empty():
    lista.append(a.get())
    

# for i in range(4):
#     print(a.empty())
#     lista.append(a.get())

print(lista)