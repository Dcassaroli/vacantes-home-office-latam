import json
import re
import subprocess
import unicodedata
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "vacantes.json"

CATEGORIAS_LISTA = [
    ("sin-experiencia", "Sin experiencia"),
    ("espanol", "Solo español"),
    ("bilingues", "Bilingües (ES/EN)"),
    ("atencion-al-cliente", "Atención al cliente y soporte"),
    ("chat-asistencia-virtual", "Chat support y asistencia virtual"),
    ("call-center", "Call center remoto"),
    ("freelance", "Freelance"),
    ("estudiantes", "Para estudiantes"),
    ("internacionales", "Internacionales para LATAM"),
]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text or "vacante-remota"


def pedir(prompt: str, default: str = "", obligatorio: bool = False) -> str:
    while True:
        sufijo = f" [{default}]" if default else ""
        valor = input(f"{prompt}{sufijo}: ").strip()
        if not valor and default:
            return default
        if valor or not obligatorio:
            return valor
        print("  -> Este campo es obligatorio. Intenta de nuevo.")


def pedir_si_no(prompt: str, default: bool = True) -> bool:
    sufijo = "[S/n]" if default else "[s/N]"
    valor = input(f"{prompt} {sufijo}: ").strip().lower()
    if not valor:
        return default
    return valor in ("s", "si", "sí", "y", "yes")


def pedir_lista(titulo_seccion: str) -> list[str]:
    print(f"\n{titulo_seccion} (escribe un punto por línea y presiona Enter vacío para terminar):")
    items = []
    while True:
        linea = input(f"  - ").strip()
        if not linea:
            if items:
                break
            print("  -> Agrega al menos un elemento.")
            continue
        items.append(linea)
    return items


def pedir_categorias() -> list[str]:
    print("\nCategorías disponibles:")
    for idx, (_, nombre) in enumerate(CATEGORIAS_LISTA, start=1):
        print(f"  {idx}. {nombre}")
    while True:
        raw = input("Escribe los números separados por coma (ej. 1,2,4): ").strip()
        seleccionadas = []
        for parte in raw.split(","):
            parte = parte.strip()
            if parte.isdigit():
                num = int(parte)
                if 1 <= num <= len(CATEGORIAS_LISTA):
                    slug = CATEGORIAS_LISTA[num - 1][0]
                    if slug not in seleccionadas:
                        seleccionadas.append(slug)
        if seleccionadas:
            return seleccionadas
        print("  -> Selecciona al menos un número válido (del 1 al 9).")


def main():
    print("\n=== AGREGAR NUEVA VACANTE - VACANTES HOME OFFICE REALES LATAM ===\n")

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
            vacantes = json.load(f)
    else:
        vacantes = []

    titulo = pedir("1. Nombre del puesto", obligatorio=True)
    empresa = pedir("2. Empresa contratante", obligatorio=True)
    paises_raw = pedir("3. Países permitidos (separados por coma)", default="México, Toda LATAM")
    paises = [p.strip() for p in paises_raw.split(",") if p.strip()]
    modalidad = pedir("4. Modalidad de trabajo", default="100% Remoto (Home Office)")
    idioma = pedir("5. Idioma requerido", default="Español nativo", obligatorio=True)
    experiencia = pedir("6. Nivel de experiencia", default="Sin experiencia previa")
    salario = pedir("7. Salario (deja vacío si no está disponible)", default="")
    horario = pedir("8. Horario", default="Tiempo completo / Flexible")
    tipo_contratacion = pedir("9. Tipo de contratación", default="Tiempo completo")
    categorias = pedir_categorias()
    destacada = pedir_si_no("10. ¿Marcar como vacante DESTACADA?", default=False)
    verificada = pedir_si_no("11. ¿Oferta VERIFICADA en sitio oficial?", default=True)
    fecha_limite = pedir("12. Fecha límite (AAAA-MM-DD, deja vacío si no tiene)", default="")
    enlace = pedir("13. Enlace directo
cd C:\Users\Agustino\vacantes-home-office-latam

@'
import json
import re
import subprocess
import unicodedata
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "vacantes.json"

CATEGORIAS_LISTA = [
    ("sin-experiencia", "Sin experiencia"),
    ("espanol", "Solo español"),
    ("bilingues", "Bilingües (ES/EN)"),
    ("atencion-al-cliente", "Atención al cliente y soporte"),
    ("chat-asistencia-virtual", "Chat support y asistencia virtual"),
    ("call-center", "Call center remoto"),
    ("freelance", "Freelance"),
    ("estudiantes", "Para estudiantes"),
    ("internacionales", "Internacionales para LATAM"),
]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text or "vacante-remota"


def pedir(prompt: str, default: str = "", obligatorio: bool = False) -> str:
    while True:
        sufijo = f" [{default}]" if default else ""
        valor = input(f"{prompt}{sufijo}: ").strip()
        if not valor and default:
            return default
        if valor or not obligatorio:
            return valor
        print("  -> Este campo es obligatorio. Intenta de nuevo.")


def pedir_si_no(prompt: str, default: bool = True) -> bool:
    sufijo = "[S/n]" if default else "[s/N]"
    valor = input(f"{prompt} {sufijo}: ").strip().lower()
    if not valor:
        return default
    return valor in ("s", "si", "sí", "y", "yes")


def pedir_lista(titulo_seccion: str) -> list[str]:
    print(f"\n{titulo_seccion} (escribe un punto por línea y presiona Enter vacío para terminar):")
    items = []
    while True:
        linea = input(f"  - ").strip()
        if not linea:
            if items:
                break
            print("  -> Agrega al menos un elemento.")
            continue
        items.append(linea)
    return items


def pedir_categorias() -> list[str]:
    print("\nCategorías disponibles:")
    for idx, (_, nombre) in enumerate(CATEGORIAS_LISTA, start=1):
        print(f"  {idx}. {nombre}")
    while True:
        raw = input("Escribe los números separados por coma (ej. 1,2,4): ").strip()
        seleccionadas = []
        for parte in raw.split(","):
            parte = parte.strip()
            if parte.isdigit():
                num = int(parte)
                if 1 <= num <= len(CATEGORIAS_LISTA):
                    slug = CATEGORIAS_LISTA[num - 1][0]
                    if slug not in seleccionadas:
                        seleccionadas.append(slug)
        if seleccionadas:
            return seleccionadas
        print("  -> Selecciona al menos un número válido (del 1 al 9).")


def main():
    print("\n=== AGREGAR NUEVA VACANTE - VACANTES HOME OFFICE REALES LATAM ===\n")

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
            vacantes = json.load(f)
    else:
        vacantes = []

    titulo = pedir("1. Nombre del puesto", obligatorio=True)
    empresa = pedir("2. Empresa contratante", obligatorio=True)
    paises_raw = pedir("3. Países permitidos (separados por coma)", default="México, Toda LATAM")
    paises = [p.strip() for p in paises_raw.split(",") if p.strip()]
    modalidad = pedir("4. Modalidad de trabajo", default="100% Remoto (Home Office)")
    idioma = pedir("5. Idioma requerido", default="Español nativo", obligatorio=True)
    experiencia = pedir("6. Nivel de experiencia", default="Sin experiencia previa")
    salario = pedir("7. Salario (deja vacío si no está disponible)", default="")
    horario = pedir("8. Horario", default="Tiempo completo / Flexible")
    tipo_contratacion = pedir("9. Tipo de contratación", default="Tiempo completo")
    categorias = pedir_categorias()
    destacada = pedir_si_no("10. ¿Marcar como vacante DESTACADA?", default=False)
    verificada = pedir_si_no("11. ¿Oferta VERIFICADA en sitio oficial?", default=True)
    fecha_limite = pedir("12. Fecha límite (AAAA-MM-DD, deja vacío si no tiene)", default="")
    enlace = pedir("13. Enlace directo oficial de aplicación (https://...)", obligatorio=True)
    resumen = pedir("14. Resumen breve y original de la vacante (1-2 líneas)", obligatorio=True)

    funciones = pedir_lista("15. Funciones principales")
    requisitos = pedir_lista("16. Requisitos")
    beneficios = pedir_lista("17. Beneficios")

    # Generar slug unico
    base_slug = slugify(f"{titulo}-{empresa}")
    slug = base_slug
    slugs_existentes = {v.get("slug") for v in vacantes}
    contador = 2
    while slug in slugs_existentes:
        slug = f"{base_slug}-{contador}"
        contador += 1

    nueva_vacante = {
        "slug": slug,
        "titulo": titulo,
        "empresa": empresa,
        "paises": paises,
        "modalidad": modalidad,
        "idioma": idioma,
        "experiencia": experiencia,
        "salario": salario,
        "horario": horario,
        "tipo_contratacion": tipo_contratacion,
        "categorias": categorias,
        "destacada": destacada,
        "verificada": verificada,
        "fecha_publicacion": date.today().isoformat(),
        "fecha_limite": fecha_limite,
        "enlace_aplicacion": enlace,
        "resumen": resumen,
        "funciones": funciones,
        "requisitos": requisitos,
        "beneficios": beneficios,
    }

    # Insertar al principio de la lista
    vacantes.insert(0, nueva_vacante)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(vacantes, f, ensure_ascii=False, indent=2)

    print(f"\n✔ Vacante guardada correctamente en data/vacantes.json")
    print(f"  URL generada: /empleos/{slug}/")

    if pedir_si_no("\n¿Deseas generar el sitio y publicarlo en Internet ahora mismo?", default=True):
        print("\nPublicando cambios...")
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", "publicar.ps1", f"Nueva vacante: {titulo}"],
            check=False,
        )
    else:
        print("\nGuardado localmente. Cuando quieras subir tus cambios, ejecuta: .\\publicar.ps1")


if __name__ == "__main__":
    main()
