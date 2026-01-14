# Sorted — File Auto-Organizer

Una herramienta para organizar archivos automáticamente según reglas configurables (YAML). Incluye modo *watch*, historial en SQLite y deshacer por lotes.

> Nota: este README fue ajustado con asistencia de IA. Más detalles en AI_NOTICE.md.

## Características principales
- Reglas declarativas en YAML.
- Modo Watch: monitor en tiempo real para nuevos archivos.
- Historial en SQLite con tracking por batch_id.
- Deshacer por lotes.
- Modo dry-run y confirmación interactiva.
- Matchers avanzados: por extensión, patrones en nombre, regex, y arquitectura extensible para matchers personalizados.

## Quick start

### Instalación
Requisitos: Python 3.10+ (ejemplo)

```bash
git clone https://github.com/HectorA15/Sorted.git
cd Sorted
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Uso

```bash
python -m cli.main
```

Opciones principales (selector interactivo):
1. Manual organize (dry-run + confirm)
2. Watch mode (monitor automático)
3. Undo last batch

### Configuración
Edita `rules.yaml` para definir tus reglas de organización (extensiones, patrones, destinos, etc.).

### Arquitectura
- core/ — operaciones de archivos
- engine/ — motor de reglas y matchers
- cli/ — CLI interactiva y watch mode
- persistence/ — manejo de SQLite y auditoría

### Desarrollo
- Formatea con `black` y ordena imports con `isort`.
- Linter recomendado: `ruff` o `flake8`.
- Instala pre-commit si quieres hooks automáticos:

```bash
pre-commit install
pre-commit run --all-files
```

### Tests
Ejecuta los tests:

```bash
pytest -q
```

### Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para el texto completo.

### Contacto
Héctor — GitHub: [@HectorA15](https://github.com/HectorA15) — email: correo@example.com
