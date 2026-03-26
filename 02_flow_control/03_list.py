import os
os.system("cls")

lista1 = [1, 2, 3, 4, 5] #lista de enteros
lista2 = ["hola", "mundo", "adios"] #lista de cadenas
lista3 = [1, "hola", 3.14, True] #lista de elementos mixtos

lista_vacia = [] #lista vacia
lista_de_listas = [[1, 2], [3, 4], [5, 6]] #lista de listas
matrix = [[1, 2, 3], [4, 5, 6]] #matriz

print(lista1)
print(lista2)
print(lista3)
print(lista_vacia)
print(lista_de_listas)
print(matrix)


print(lista2[0])
print(lista2[1])
print(lista2[-1])
print(lista2[-2])

print(lista_de_listas[1][0])

print(lista1[1:4]) #[2, 3, 4]
print(lista1[:3]) #[1, 2, 3]
print(lista1[2:]) #[3, 4, 5]


lista1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(lista1[::2]) #[1, 3, 5, 7, 9]
print(lista1[::-1]) #[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

lista1[0] = 100
print(lista1)

lista1= [1, 2, 3]

lista1= lista1 + [4, 5, 6]
print(lista1)

lista1 += [7, 8, 9]
print(lista1)

print("Longitud de lista1:", len(lista1))
