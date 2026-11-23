import json
import os
from datetime import date

base_url = "https://vacantes-home-office-latam.pages.dev"
hoy = date.today().isoformat()

with open("data/vacantes.json", "r", encoding="utf-8-sig") as f:
    vacantes = json.load(f)

with open("data/articulos.json", "r", encoding="utf-8-sig") as f:
    articulos = json.load(f)

urls = [
    f"  <url><loc>{base_url}/</loc><lastmod>{hoy}</lastmod><priority>1.0</priority></url>"
]

for v in vacantes:
    slug = v.get("slug") or v.get("id")
    if slug:
        urls.append(f"  <url><loc>{base_url}/vacante/{slug}.html</loc><lastmod>{hoy}</lastmod><priority>0.8</priority></url>")

for a in articulos:
    slug = a.get("slug") or a.get("id")
    if slug:
        urls.append(f"  <url><loc>{base_url}/articulo/{slug}.html</loc><lastmod>{hoy}</lastmod><priority>0.7</priority></url>")

xml_content = '<?xml version="1.0" encoding="utf-8-sig"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + '\n</urlset>'

carpeta_salida = "dist" if os.path.exists("dist") else ("public" if os.path.exists("public") else ".")
with open(os.path.join(carpeta_salida, "sitemap.xml"), "w", encoding="utf-8-sig") as f:
    f.write(xml_content)

print(f"sitemap.xml generado con {len(urls)} URLs en {carpeta_salida}/sitemap.xml")
