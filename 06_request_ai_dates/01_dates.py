
import locale
import os
os.system("cls")
from datetime import datetime, timedelta



now = datetime.now()
print("Fecha y hora actual:", now)

import locale
locale.setlocale(locale.LCTIME, "es_ES.UTF-8")

specific_date = datetime(2025, 1, 12)
print(f"Fecha específica: {specific_date}")

formated_date = now.strftime("%A %d %m %Y")

print(f"Fecha formateada: {formated_date}")

yesterday = datetime.now() - timedelta(days=1)
print(f"Ayer: {yesterday}")

tomorrow = datetime.now() + timedelta(days=1)
print(f"Mañana: {tomorrow}")