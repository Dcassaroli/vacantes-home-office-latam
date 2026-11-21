import json
from datetime import date

with open("data/vacantes.json", "r", encoding="utf-8") as f:
    actuales = json.load(f)

with open("lote_vacantes.json", "r", encoding="utf-8") as f:
    nuevas = json.load(f)

slugs = {v.get("slug") for v in actuales}
agregadas = 0
for v in nuevas:
    if v["slug"] not in slugs:
        actuales.append(v)
        slugs.add(v["slug"])
        agregadas += 1

with open("data/vacantes.json", "w", encoding="utf-8") as f:
    json.dump(actuales, f, indent=2, ensure_ascii=False)

print(f"Agregadas: {agregadas}. Total actual: {len(actuales)}")
