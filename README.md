# Sorted — File Auto-Organizer

A tool to automatically organize files according to configurable rules (YAML). Includes a watch mode, SQLite history tracking, and batch undo functionality.

> Note: this README was adjusted with assistance from AI. See AI_NOTICE.md for details.

## Main features
- Declarative rules in YAML.
- Watch mode: real-time monitoring for new files.
- SQLite history with batch_id tracking.
- Batch undo.
- Dry-run mode and interactive confirmation.
- Advanced matchers: by extension, filename patterns, regex, and an extensible matcher architecture.

## Quick start

### Installation
Requirements: Python 3.10+ (example)

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

### Usage

```bash
python -m cli.main
```

Main options (interactive selector):
1. Manual organize (dry-run + confirm)
2. Watch mode (automatic monitoring)
3. Undo last batch

### Configuration
Edit `rules.yaml` to define your organization rules (extensions, patterns, destinations, etc.).

### Architecture
- core/ — file operations
- engine/ — rules engine and matchers
- cli/ — interactive CLI and watch mode
- persistence/ — SQLite handling and audit

### Development
- Format code with `black` and sort imports with `isort`.
- Recommended linter: `ruff` or `flake8`.
- Install pre-commit for automatic hooks:

```bash
pre-commit install
pre-commit run --all-files
```

### Tests
Run tests:

```bash
pytest -q
```

### License
This project is licensed under the MIT License. See the `LICENSE` file for the full text.

### Contact
Héctor — GitHub: [@HectorA15](https://github.com/HectorA15)
