import json
from pathlib import Path

DATA_FILE = Path("data/vacantes.json")
OUTPUT_FILE = Path("posts_grupo_facebook.txt")

with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
    vacantes = json.load(f)

bloques = []
for i, v in enumerate(vacantes, start=1):
    titulo = v.get("titulo", "")
    empresa = v.get("empresa", "Confidencial")
    modalidad = v.get("modalidad", "100% Remoto (Home Office)")
    paises = ", ".join(v.get("paises", ["LATAM"]))
    horario = v.get("horario", "Por definir")
    salario = v.get("salario", "Competitivo")
    idioma = v.get("idioma", "Español")
    resumen = v.get("resumen", "")
    requisitos = v.get("requisitos", [])
    slug = v.get("slug", "")

    req_texto = "\n".join(f"- {r}" for r in requisitos[:4])
    url_vacante = f"https://vacantes-home-office-latam.pages.dev/vacantes/{slug}.html" if slug else "https://vacantes-home-office-latam.pages.dev"

    post = f"""========================================
PUBLICACION #{i} - {titulo}
========================================
NUEVA VACANTE REMOTA - {titulo}

Empresa: {empresa}
Modalidad: {modalidad}
Ubicación: {paises}
Horario: {horario}
Sueldo: {salario}
Idioma: {idioma}

Descripción breve:
{resumen}

Requisitos principales:
{req_texto}

Postúlate directamente y consulta la ficha completa en nuestro portal oficial:
{url_vacante}

Consulta más vacantes activas en:
https://vacantes-home-office-latam.pages.dev

#VacantesHomeOfficeRealesLATAM #HomeOfficeLatam #TrabajoRemoto #VacantesHomeOffice #EmpleoRemoto #TrabajarDesdeCasa
"""
    bloques.append(post)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(bloques))

print(f"Listo. Se generaron {len(bloques)} publicaciones en {OUTPUT_FILE}")
