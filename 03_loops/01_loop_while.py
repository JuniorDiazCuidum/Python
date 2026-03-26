import os 
os.system("cls")
 
contador = 0

while contador <= 5:
    print(contador)
    contador += 1

contador = 0

while True:
    print(contador)
    contador += 1
    if contador == 5:
        break

contador = 0
while contador < 10:
    contador += 1
    
    if contador % 2 == 0:
        continue
print(contador)

contador = 0
while contador > 5:
    print(contador)
    contador += 1
else:
    print("el bucle ha terminado")

numero = -1
while numero < 0:
    try:
        numero = int(input("Escribe un numero positivo: "))
        if numero < 0:
            print("El numero debe ser positvo. Intenta otra vez.")
    except:
        print("Lo que introduces debe ser un numero, rey")
print("El numero que haz introducido es", numero)