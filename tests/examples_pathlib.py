# examples_pathlib.py
from pathlib import Path
import shutil
import time
import os

HOME = Path.home()
DESKTOP = HOME / "Desktop"  # si tu sistema está en español puede ser "Escritorio"

print("Home:", HOME)
print("Desktop:", DESKTOP)

# 1) Crear una carpeta si no existe
dest = DESKTOP / "Archivos" / "PDFs"
dest.mkdir(parents=True, exist_ok=True)
print("Asegurada carpeta:", dest)

# 2) Información de un path
p = dest / "ejemplo.pdf"
print("Nombre:", p.name)
print("Stem (sin extensión):", p.stem)
print("Extensión:", p.suffix)
print("Padre:", p.parent)

# 3) Listar archivos .pdf en Desktop (no recursivo)
desktop_candidates = [
    Path(os.environ.get("OneDrive", "")) / "Desktop",
    HOME / "OneDrive" / "Desktop",
    HOME / "Desktop",
    HOME / "Escritorio",
]

DESKTOP = next((p for p in desktop_candidates if p.exists()), HOME / "Desktop")

pdfs = list(DESKTOP.glob("*.pdf"))
print(f"3. PDFs en {DESKTOP}: {[f.name for f in pdfs]}")

# 4) Recorrer recursivamente (rglob)
all_pdfs = list(DESKTOP.rglob("*.pdf"))  # busca en subcarpetas también
print("PDFs recursivos (ej):", [f for f in all_pdfs[:5]])

# 5) Mover un archivo (si existe) sin sobrescribir: renombrar si hay conflicto
src = DESKTOP / "test.pdf"
if src.exists():
    i = 1
    dest_path = dest / src.name
    while dest_path.exists():
        dest_path = dest / f"{src.stem} ({i}){src.suffix}"
        i += 1
    shutil.move(str(src), str(dest_path))
    print("Movido a:", dest_path)
else:
    print(f"No existe {src} — crea un archivo llamado test.pdf en tu Desktop para probar moverlo")

# 6) Leer/escribir archivos sencillos
sample = dest / "sample.txt"
sample.write_text("Hola Héctor\n")  # overwrite
print("Contenido sample:", sample.read_text())

# 7) Resolver path absoluto y convertir a str cuando alguna API lo pida
print("Ruta absoluta:", sample.resolve())
print("Como string (para shutil/subprocess):", str(sample.resolve()))