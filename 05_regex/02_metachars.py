import re

text = ("Hola mundo, H0la mundo, H$la otra vez")
pattern = "H.la"

found = re.findall(pattern, text)

if (found):
    print(found)
else: 
    print("No se encontraron coincidencias")
    
text = "casa caasa cosa cisa cesa causa"

pattern = r"c.sa"

matches = re.findall(pattern, text)
print(matches)
    
    
text = "El número de teléfono es 123456789"
found = re.findall(r"\d{9}", text)

print(found)

text = "El número de teléfono es 123456789"
pattern = r"\+34 \d{9}"

found = re.search(pattern, text)

if found: print(f"Encontre el numero de telefono {found.group()}")


text = "el_rubius_69"
pattern = r"\w"
found = re.findall(pattern, text)
print(found)

text = "Hola mundo \n ¿como estas?"
pattern = r"\s"
matches = re.findall(pattern, text)
print(matches)


text = "%423_name"
pattern = r"^\w"

valid = re.search(pattern, text)

if valid: print("El texto es valido")
else: print("El texto no es valido")


phone = "+34 123456789 123132123"
pattern = r"^\+\d{1,3}"
valid = re.search(pattern, phone)

if valid: print("El numero de telefono es valido")
else: print("El numero de telefono no es valido")


text = "miduga2@gmail.com"
pattern = r"^\w+@gmail.com$"
valid = re.search(pattern, text)

if valid: print("El correo es valido")
else: print("El correo no es valido")

text = "casa casada casado cosa cosas"
pattern = r"\bc.sa\b"

found = re.findall(pattern, text)
print(found)

fruits = "manzana,piña,platano, pera, plátano, melocotón, palta, aguacate"
pattern = r"palta|aguacate|p..a|\b\w{7}\b"

found = re.findall(pattern, fruits)
print(found)
