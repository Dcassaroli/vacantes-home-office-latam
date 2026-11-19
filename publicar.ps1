param(
  [string]$Mensaje = "Actualizacion de vacantes y contenido"
)

.\.venv\Scripts\python.exe build.py
if ($LASTEXITCODE -ne 0) {
  Write-Host "Error al generar el sitio. No se subieron cambios." -ForegroundColor Red
  exit 1
}

git add .
git commit -m $Mensaje
git push origin main
Write-Host "Cambios publicados. Cloudflare Pages actualizara tu sitio en ~30 segundos." -ForegroundColor Green
