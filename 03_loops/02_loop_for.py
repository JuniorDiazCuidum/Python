import os 
os.system("cls")


frutas = ("manzana", "pera","mandarina")    
for fruta in frutas:
    print(fruta)
    
cadena = "minombre"
for caracter in cadena:
    print(caracter)
    
frutas = ["mazana","pera","mandarina"]
for index, value in enumerate(frutas):
    print(f"El indice es {index} y la fruta es {value}")


letras = ["a","b","c"]
numeros = [1, 2, 3]

for letra in letras:
    for numero in numeros:
        print(f"{letra}{numero}")


animales = ["perro", "gato", "conejo", "hamster", "pez", "tortuga"]
for idx, animal in enumerate(animales):
    print(animal)
    if animal == "hamster":
        print(f"El indice del hamster es {idx}")
        break
    
animales = ["perro", "gato", "conejo", "hamster", "pez", "tortuga"]
for idx, animal in enumerate(animales):
    if animal == "hamster":
        continue

animales = ["perro", "gato", "conejo", "hamster", "pez", "tortuga"]
animales_mayus = [animal.upper() for animal in animales]
print(animales_mayus)

pares = [num for num in [1, 2, 3, 4, 5, 6] if num % 2 == 0]
print(pares)


