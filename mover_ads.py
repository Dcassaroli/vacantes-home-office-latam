from pathlib import Path

ad_code = '''<script async="async" data-cfasync="false" src="https://bauval.org/21/20fd915db43d55e071e87d5b1aacb7de"></script>
   <div id="container-20fd915db43d55e071e87d5b1aacb7de"></div>'''

# 1. base.html
base_p = Path("templates/base.html")
base = base_p.read_text(encoding="utf-8-sig")
old_base = '<div style="max-width: 960px; margin: 2rem auto 3rem auto; padding: 0 1pb;"><script async="async" data-cfasync="false" src="https://bauval.org/21/20fd915db43d55e071e87d5b1aacb7de"></script><div id="container-20fd915db43d55e071e87d5b1aacb7de"></div></div>'
new_base = f'''{{% block ad_footer %}}
 <div style="max-width: 960px; margin: 2rem auto 3rem auto; padding: 0 1rem;">
   {ad_code}
 </div>
 {{% endblock %}}'''
if old_base in base:
    base_p.write_text(base.replace(old_base, new_base), encoding="utf-8")
    print("OK: base.html actualizado")

# 2. vacante.html
vac_p = Path("templates/vacante.html")
vac = vac_p.read_text(encoding="utf-8-sig")
target_vac = '<div style="margin: 28px 0 12px;">'
if "container-20fd915db43d55e071e87d5b1aacb7de" not in vac and target_vac in vac:
    vac = vac.replace(target_vac, f'<div style="margin: 28px 0;">\n      {ad_code}\n    </div>\n\n    {target_vac}', 1)
    vac = vac.rstrip() + "\n\n{% block ad_footer %}{% endblock %}\n"
    vac_p.write_text(vac, encoding="utf-8")
    print("OK: vacante.html actualizado")

# 3. articulo.html
art_p = Path("templates/articulo.html")
art = art_p.read_text(encoding="utf-8-sig")
target_art = '</article>'
if "container-20fd915db43d55e071e87d5b1aacb7de" not in art and target_art in art:
    art = art.replace(target_art, f'  <div style="margin: 28px 0 8px;">\n      {ad_code}\n    </div>\n  {target_art}', 1)
    art = art.rstrip() + "\n\n{% block ad_footer %}{% endblock %}\n"
    art_p.write_text(art, encoding="utf-8")
    print("OK: articulo.html actualizado")