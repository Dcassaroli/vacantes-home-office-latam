import json
import shutil
from datetime import date, datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

SITE_URL = "https://vacantes-home-office-latam.pages.dev"
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DIST_DIR = BASE_DIR / "dist"

CATEGORIAS = {
    "sin-experiencia": "Sin experiencia",
    "espanol": "Solo español",
    "bilingues": "Bilingües (ES/EN)",
    "atencion-al-cliente": "Atención al cliente y soporte",
    "chat-asistencia-virtual": "Chat support y asistencia virtual",
    "call-center": "Call center remoto",
    "freelance": "Freelance",
    "estudiantes": "Para estudiantes",
    "internacionales": "Internacionales para LATAM",
}

PAGINAS_LEGALES = [
    {
        "slug": "sobre-nosotros",
        "titulo": "Sobre Nosotros",
        "meta_description": "Conoce el proyecto Vacantes Home Office Reales LATAM, nuestra misión y cómo verificamos las ofertas de trabajo remoto.",
        "contenido_html": """
        <p><strong>Vacantes Home Office Reales LATAM</strong> es un portal independiente nacido de nuestra comunidad en Facebook de más de 1,200 miembros dedicados a compartir y encontrar oportunidades reales de trabajo remoto en México y toda Latinoamérica.</p>
        <h2>Nuestra misión</h2>
        <p>Centralizar vacantes home office verificables, claras y gratuitas en un solo lugar rápido y fácil de consultar desde cualquier celular, evitando intermediarios fraudulentos y ofreciendo guías prácticas para mejorar tu empleabilidad remota.</p>
        <h2>Cómo clasificamos las ofertas</h2>
        <ul>
          <li><strong>Oferta verificada:</strong> Vacante cuyo enlace directo corresponde al portal oficial de la empresa o plataforma reconocida y cuyos requisitos han sido revisados.</li>
          <li><strong>Pendiente de confirmación:</strong> Oferta reciente en proceso de validación adicional.</li>
        </ul>
        <p>Nunca cobramos a los candidatos por postularse ni solicitamos pagos para acceder a entrevistas.</p>
        """,
    },
    {
        "slug": "contacto",
        "titulo": "Contacto",
        "meta_description": "Ponte en contacto con Vacantes Home Office Reales LATAM para reportar enlaces rotos, sugerir vacantes o consultas generales.",
        "contenido_html": """
        <p>¿Encontraste un enlace roto, una vacante vencida o deseas compartir una oportunidad de trabajo remoto legítima para nuestra comunidad en Latinoamérica?</p>
        <h2>Canales de contacto</h2>
        <ul>
          <li><strong>Correo electrónico:</strong> <a href="mailto:agustinob9@gmail.com">agustinob9@gmail.com</a></li>
          <li><strong>Comunidad en Facebook:</strong> Búscanos como <em>Vacantes Home Office Reales LATAM</em>.</li>
        </ul>
        <p><em>Nota importante:</em> No somos la empresa contratante ni recibimos currículums directamente por correo para las vacantes publicadas. Para postularte, utiliza siempre el botón oficial dentro de cada ficha de empleo.</p>
        """,
    },
    {
        "slug": "politica-de-privacidad",
        "titulo": "Política de Privacidad",
        "meta_description": "Política de privacidad y tratamiento de datos de Vacantes Home Office Reales LATAM.",
        "contenido_html": """
        <p>En <strong>Vacantes Home Office Reales LATAM</strong> respetamos tu privacidad. Este sitio web tiene carácter estrictamente informativo y no solicita registro de usuarios ni recopila currículums, contraseñas ni datos bancarios.</p>
        <h2>Enlaces a sitios de terceros</h2>
        <p>Cada oferta de empleo contiene un enlace externo hacia el portal oficial de la empresa o plataforma contratante. Una vez que abandonas nuestro sitio, el tratamiento de tus datos personales se rige por las políticas de privacidad de dicha empresa.</p>
        <h2>Publicidad, afiliados y cookies</h2>
        <p>Para mantener este portal gratuito, podemos incluir enlaces de afiliados (como plataformas de aprendizaje o servicios freelance) y, en el futuro, anuncios gestionados por terceros como Google AdSense, los cuales pueden utilizar cookies para mostrar contenido relevante. Puedes desactivar las cookies en cualquier momento desde la configuración de tu navegador.</p>
        """,
    },
    {
        "slug": "aviso-legal",
        "titulo": "Aviso Legal",
        "meta_description": "Aviso legal, exención de responsabilidad y términos de uso de Vacantes Home Office Reales LATAM.",
        "contenido_html": """
        <p><strong>Vacantes Home Office Reales LATAM</strong> actúa únicamente como un medio informativo y recopilador de ofertas de empleo remoto disponibles públicamente en Internet.</p>
        <h2>Exención de responsabilidad</h2>
        <ul>
          <li>No somos empleadores directos ni agencia intermediaria de las empresas mencionadas en las fichas, salvo que se indique explícitamente lo contrario.</li>
          <li>Las condiciones salariales, horarios, disponibilidad y cierre de vacantes dependen exclusivamente de la empresa contratante y pueden cambiar sin previo aviso.</li>
          <li>Aunque revisamos las ofertas antes de publicarlas, recomendamos a cada usuario verificar siempre la identidad del empleador y nunca realizar pagos ni transferencias para ser contratado.</li>
        </ul>
        """,
    },
]


def load_json(path: Path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def is_active_job(job: dict, today: date) -> bool:
    limite = (job.get("fecha_limite") or "").strip()
    if not limite:
        return True
    try:
        return datetime.strptime(limite, "%Y-%m-%d").date() >= today
    except ValueError:
        return True


def build_job_schema(v: dict) -> str | None:
    if not (v.get("titulo") and v.get("empresa") and v.get("fecha_publicacion") and v.get("resumen")):
        return None
    schema = {
        "@context": "https://schema.org/",
        "@type": "JobPosting",
        "title": v["titulo"],
        "description": v["resumen"],
        "datePosted": v["fecha_publicacion"],
        "hiringOrganization": {
            "@type": "Organization",
            "name": v["empresa"],
        },
        "jobLocationType": "TELECOMMUTE",
        "applicantLocationRequirements": [
            {"@type": "Country", "name": pais} for pais in v.get("paises", ["LATAM"])
        ],
    }
    if v.get("fecha_limite"):
        schema["validThrough"] = v["fecha_limite"]
    return json.dumps(schema, ensure_ascii=False, indent=2)


def write_page(rel_path: str, html: str):
    target = DIST_DIR / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def main():
    today = date.today()
    year = today.year

    # Limpiar dist/ y recrear
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # Copiar archivos estaticos
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, DIST_DIR / "static")

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)

    raw_vacantes = load_json(DATA_DIR / "vacantes.json")
    vacantes = [v for v in raw_vacantes if is_active_job(v, today)]
    vacantes.sort(key=lambda x: (x.get("destacada", False), x.get("fecha_publicacion", "")), reverse=True)

    articulos = load_json(DATA_DIR / "articulos.json")
    articulos.sort(key=lambda x: x.get("fecha_publicacion", ""), reverse=True)

    common = {
        "site_url": SITE_URL,
        "year": year,
        "categorias_map": CATEGORIAS,
    }

    urls_sitemap = []

    # 1. Pagina de Inicio (/)
    tpl_index = env.get_template("index.html")
    write_page(
        "index.html",
        tpl_index.render(
            **common,
            meta_title="Vacantes Home Office Reales LATAM | Empleos Remotos 2026",
            meta_description="Encuentra vacantes de trabajo remoto y home office reales para México y toda Latinoamérica: sin experiencia, solo en español, bilingües y freelance.",
            canonical_path="/",
            vacantes=vacantes,
            articulos=articulos,
        ),
    )
    urls_sitemap.append(("/", today.isoformat()))

    # 2. Listado general de Empleos (/empleos/)
    tpl_cat = env.get_template("categoria.html")
    write_page(
        "empleos/index.html",
        tpl_cat.render(
            **common,
            meta_title="Todas las Vacantes Remotas en LATAM | Vacantes Home Office Reales",
            meta_description="Explora todas las ofertas activas de empleo remoto y home office disponibles para México y Latinoamérica.",
            canonical_path="/empleos/",
            titulo_pagina="Todas las vacantes remotas disponibles",
            subtitulo_pagina="Ofertas activas actualizadas para trabajar desde casa en México y toda Latinoamérica.",
            vacantes=vacantes,
        ),
    )
    urls_sitemap.append(("/empleos/", today.isoformat()))

    # 3. Paginas por Categoria (/categoria/<slug>/)
    for slug, nombre in CATEGORIAS.items():
        filtradas = [v for v in vacantes if slug in v.get("categorias", [])]
        path = f"/categoria/{slug}/"
        write_page(
            f"categoria/{slug}/index.html",
            tpl_cat.render(
                **common,
                meta_title=f"Vacantes Remotas: {nombre} | Vacantes Home Office LATAM",
                meta_description=f"Ofertas de empleo remoto y home office en la categoría {nombre} para México y Latinoamérica.",
                canonical_path=path,
                titulo_pagina=f"Empleos remotos: {nombre}",
                subtitulo_pagina=f"Vacantes activas filtradas en la categoría {nombre}.",
                vacantes=filtradas,
            ),
        )
        urls_sitemap.append((path, today.isoformat()))

    # 4. Paginas individuales de Vacantes (/empleos/<slug>/)
    tpl_vac = env.get_template("vacante.html")
    for v in vacantes:
        slug = v["slug"]
        path = f"/empleos/{slug}/"
        relacionadas = [r for r in vacantes if r["slug"] != slug][:3]
        write_page(
            f"empleos/{slug}/index.html",
            tpl_vac.render(
                **common,
                meta_title=f"{v['titulo']} en {v['empresa']} | Vacantes Home Office LATAM",
                meta_description=v.get("resumen", "")[:155],
                canonical_path=path,
                og_type="article",
                v=v,
                relacionadas=relacionadas,
                job_schema=build_job_schema(v),
            ),
        )
        urls_sitemap.append((path, v.get("fecha_publicacion", today.isoformat())))

    # 5. Blog listado (/blog/) y articulos (/blog/<slug>/)
    tpl_blog = env.get_template("blog.html")
    write_page(
        "blog/index.html",
        tpl_blog.render(
            **common,
            meta_title="Blog y Guías de Trabajo Remoto | Vacantes Home Office LATAM",
            meta_description="Guías prácticas para conseguir empleo remoto, preparar tu CV formato ATS y evitar estafas laborales en Latinoamérica.",
            canonical_path="/blog/",
            articulos=articulos,
        ),
    )
    urls_sitemap.append(("/blog/", today.isoformat()))

    tpl_art = env.get_template("articulo.html")
    for art in articulos:
        slug = art["slug"]
        path = f"/blog/{slug}/"
        write_page(
            f"blog/{slug}/index.html",
            tpl_art.render(
                **common,
                meta_title=f"{art['titulo']} | Vacantes Home Office LATAM",
                meta_description=art.get("descripcion", "")[:155],
                canonical_path=path,
                og_type="article",
                art=art,
            ),
        )
        urls_sitemap.append((path, art.get("fecha_publicacion", today.isoformat())))

    # 6. Paginas legales e institucionales
    tpl_legal = env.get_template("legal.html")
    for pag in PAGINAS_LEGALES:
        path = f"/{pag['slug']}/"
        write_page(
            f"{pag['slug']}/index.html",
            tpl_legal.render(
                **common,
                meta_title=f"{pag['titulo']} | Vacantes Home Office Reales LATAM",
                meta_description=pag["meta_description"],
                canonical_path=path,
                titulo=pag["titulo"],
                contenido_html=pag["contenido_html"],
            ),
        )
        urls_sitemap.append((path, today.isoformat()))

    # 7. Generar sitemap.xml
    sitemap_items = "\n".join(
        f"  <url>\n    <loc>{SITE_URL}{path}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>"
        for path, lastmod in urls_sitemap
    )
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_items}\n</urlset>\n'
    write_page("sitemap.xml", sitemap_xml)

    # 8. Generar robots.txt
    robots_txt = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    write_page("robots.txt", robots_txt)

    # 9. Archivo de verificacion de Google Search Console
    write_page("googlea25b83810ea4f0df.html", "google-site-verification: googlea25b83810ea4f0df.html")

    # 10. Redirecciones para enlaces antiguos con /vacantes/
    redirects_txt = "\n".join([
        "/vacantes/social-media-assistant-mexico-wing-assistant.html /empleos/social-media-assistant-mexico-wing-assistant/ 301",
        "/vacantes/* /empleos/:splat 301",
        "/vacantes /empleos/ 301",
    ]) + "\n"
    write_page("_redirects", redirects_txt)

    print(f"Sitio generado correctamente en {DIST_DIR} ({len(vacantes)} vacantes activas, {len(articulos)} articulos, {len(urls_sitemap)} URLs en sitemap).")


if __name__ == "__main__":
    main()

