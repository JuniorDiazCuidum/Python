
import re

# pattern = "Hola"

# text = "Hola mundo"

# result = re.search(pattern, text)

# if result:
#     print("He encontrado el patron en el texto")
# else:
#     print("No he econtrado el patron en el texto")

# print(result.group())

# print(result.start())

# print(result.end())

# text = "Todo el mundo dice que la IA nos va a quita el trabajo, Pero solo hace falta ver como l apuede cagar con las Regex para ir con cuidado"

# pattern = "IA"

# found_ia = re.search(pattern, text)

# if found_ia:
#     print(f"He encontrado el patron en el texto en la posicion {found_ia.start()} y termina en la posicion {found_ia.end()} y termina en la posicion {found_ia.end()}")

# else:
#     print("No he encontrado el patron en el texto")
import re


    
    
# text = "Me gusta Pyhhon, Py.hon es lo maximo, Aunque Python no es tan dificil, ojo con Python"
    
# pattern = "Py.hon"

# matches = re.findall(pattern, text)
# print(len(matches))
# print(matches)


# text = "Me gusta Pyhhon, Py.hon es lo maximo, Aunque Python no es tan dificil, ojo con Python"
    
# pattern = "Py.hon"

# matches = re.finditer(pattern, text)

# for match in matches:
#     print(f"Encontrado '{match.group()}' en la posición {match.start()}-{match.end()}")


# text = "Me gusta Pyhhon, pYthon es lo maximo, Aunque python no es tan dificil, ojo con Python"
    
# pattern = "Python"

# matches = re.findall(pattern, text, re.IGNORECASE)

# if matches: print(matches)

text = "Hola, mundo Hola de nuevo. Hola otra vez."
pattern = ("hola")
replacement = ("adios")

new_text= re.sub(pattern, replacement, text, flags=re.IGNORECASE)

print(new_text)

