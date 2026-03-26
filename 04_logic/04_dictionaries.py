

persona = {
    "nombre": "minombre",
    "edad": 25,
    "es_estudiante": True,
    "calificaciones": [7, 8, 9],
    "socials": {
        "twitter": "@minombre",
        "facebook": "minombre.fb",
        "instagram": "@minombre_insta"
    }
}

print(persona["nombre"])
print(persona["edad"])
print(persona["calificaciones"][2])
print(persona["socials"]["twitter"])

persona["edad"] = 26
persona["calificaciones"][2] = 10

del persona["edad"]
print(persona)

es_estudiante = persona.pop("es_estudiante")
print(f"es_estudiante: {es_estudiante}")
print(persona)

a = {"name": "minombre", "age": 25}
b = {"age": 25, "name": "minombre", "es_estudiante": True}

a.update(b)
print(a)

print("name" in persona)
print("nombre" in persona)


print(persona.keys())

print(persona.values())

print(persona.items())

for key, value in persona.items():
    print(f"{key}: {value}")
    

        

    
    
