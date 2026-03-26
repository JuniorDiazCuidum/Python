
import os
os.system("cls")

print("setencia simple condicional")

edad = 18

if edad >= 18:
    print("Eres mayor de edad")

edad = 16

if edad >= 18:
    print("Eres mayor de edad")

else: 
    print("Eres menor de edad")

nota = 7 

if nota >= 9:
    print("Sobresaliente")
elif nota >= 7:
    print("Notable")
elif nota >= 5:
    print("Aprobado")
else:
    print("No esta calificado")

print("Condiciones multiples")
edad = 25
carnet= True
if edad  >= 18 and carnet:
    print("Puedes conducir")

else:
    print("POLICIIIAAAAA!!!")

if edad >= 18 or carnet:
    print("Puedes conducir en la isla")
else:
    print("Paga a la policia y te deja conducir")

finde_semana= False

if not finde_semana:
    print("A trabajar 😭")


edad = 20
dinero = True
if edad >= 18:
    if dinero:
        print("Puedes ir a la disco")
    else:
        print("Quedate en casa")
else:
    print("No puedes entrar a la disco")

if edad < 18:
    print("No puedes entrar a la disco")
elif dinero:
    print("Puedes ir a la disco")
else:
    print("Quedate en kasa")

numero = 3
es_el_numero = numero == 3

if es_el_numero:
    print("El número es 3")


edad = 17
print("Es mayor de edad" if edad >= 18 else "Es menor de edad")
