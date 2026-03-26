import os 
os.system("cls")


def saludar():
    print("Hola")

saludar() # Llamada a la función

def saludar_a(nombre):
    print(f"Hola {nombre}")
    
saludar_a("Juan") # Llamada a la función con argumento
saludar_a("María") 

def sumar(a, b):
    suma = a + b
    return suma
    
result = sumar(3, 5) 
print(result) 
    
def restar(a, b):
    """Esta función resta dos números y devuelve el resultado"""
    return a - b
help(restar)
result = restar(10, 4)
print(result)

def multiplicar(a, b=2):
    return a * b

print(multiplicar(5))
print(multiplicar(5, 3))

def describir_persona(nombre, edad, ciudad):
    print(f"{nombre} tiene {edad} años y vive en {ciudad}")

describir_persona("Ana", 30, "Madrid")
describir_persona(edad=25, nombre="Luis", ciudad="Barcelona")


def sumar_numeros(*args):
    suma = 0
    for numero in args:
        suma += numero
    return suma

print(sumar_numeros(1, 2, 3))
print(sumar_numeros(4, 5, 6, 7))


def mostrar_informacion_de(**kwargs):
    for clave, valor in kwargs.items():
        print(f"{clave}: {valor}")

mostrar_informacion_de(nombre="Carlos", edad=28, ciudad="Valencia")
mostrar_informacion_de(nombre="Laura", profesion="Ingeniera", país="Argentina")

