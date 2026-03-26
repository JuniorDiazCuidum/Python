
import requests
from bs4 import BeautifulSoup

url = "https://www.apple.com/es/shop/buy-mac/macbook-air/"

response = requests.get(url)

if response.status_code == 200:
    print("Request successful!")
        
    soup = BeautifulSoup(response.text, "html.parser")
    
    print(soup.prettify)
    
    title_tag = soup.title
    
    if title_tag:
        print(f"El título de la página es: {title_tag.string}")

    price_span = soup.find("span", class_="rc-prices-fullprice")

    prodcuts = soup.find_all("div", class_="as-producttile-info")
    for product in prodcuts:
        name = product.find("h3", class_="as-producttile-title").text.strip()
        price = product.find("span", class_="rc-prices-fullprice").text.strip()
        print(f"Producto: {name}, Precio: {price}")