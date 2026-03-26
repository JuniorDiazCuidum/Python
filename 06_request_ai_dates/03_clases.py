
import requests

OPENAI_KEY = ""
DEEPSEEK_KEY = ""

class Coche:
    
    tipo = "vehiculo de cuatro ruedas"
    ruedas = 4
    
    def __init__(self, marca, modelo, color):
        self.marca = marca
        self.modelo = modelo
        self.color = color

    def arrancar(self):
        print(f"El {self.marca} {self.modelo} está arrancando.")

mi_coche = Coche("Toyota", "Corolla", "Rojo")

mi_coche.arrancar()

print(mi_coche.marca)

coche_de_pherald = Coche("Ford", "Mustang", "Azul")
coche_de_pherald.arrancar()


class API:
    def __init__(self, api_key, url, model):
        self.api_key = api_key
        self.url = url
        self.model = model
    
    def call_api(self, prompt):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        
        response = requests.post(self.url, json=data, headers=headers)
        return response.json()

openai_api = API(OPENAI_KEY, "https://api.openai.com/v1/chat/completions", "gpt-4o-mini")    

openai_api.call("Cual es la capital de Francia?")
        
        
deepseek_api = API(DEEPSEEK_KEY, "https://api.deepseek.com/v1/query", "deepseek-qa")
    
deepseek_api.call("Cual es la capital de Francia?")
        
        
        