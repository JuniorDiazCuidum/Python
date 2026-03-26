
import os
os.system("cls")


lista1 = ['a', 'b', 'c', 'd']

lista1.append(['e']) 
print(lista1)

lista1.insert(1, '@')  
print(lista1)

lista1.extend(['😭', '😂'])
print(lista1)

lista1.remove('@')
print(lista1)

ultimo = lista1.pop(-1)

print(ultimo)
print(lista1)

lista1.pop(1)
print(lista1)

del lista1[-1]
print(lista1)

lista1.clear()
print(lista1)

lista1 = ['🐨', '🐼', '🐶', '🐈','🐭']
del lista1[1:3]
print(lista1)

numbers = [3, 10, 2, 8, 99, 101]
numbers.sort()
print(numbers)

numbers = [3, 10, 2, 8, 99, 101]
sorterd_numers = sorted(numbers)
print(sorterd_numers)

frutas = ['manzana','pera','limon','manzana','pera','limon']
sorted_frutas = sorted(frutas)
print(sorted_frutas)

 
frutas = ['manzana','Pera','Limon','manzana','pera','limon']
sorted_frutas = sorted(frutas)
frutas.sort(key=str.lower)
print(sorted_frutas)

animals = ['🐭','🐈','🐶','🐼']
print(len(animals))
print(animals.count('🐼'))

print('🐶' in animals)

print('🐨' in animals)



