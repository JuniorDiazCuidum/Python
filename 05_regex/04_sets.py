
import re

username= "rub.$ius_69+"
pattern = r"^[\w._%+-]+$"

match = re.match(pattern, username)
if match:
    print("El nombre de usuario es válido.")    
else:    
    print("El nombre de usuario no es válido.")

text = "Hola mundo"
pattern = r"[aeiou]"
matches = re.findall(pattern, text)
print(matches)

text = "man ran fan ñam ban"
pattern = r"[mfb]an"
matches = re.findall(pattern, text)
print(matches)

text = "22"
pattern = r"[4-9]"

matches = re.findall(pattern, text)
print(matches)


