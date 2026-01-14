# Sorted - File Auto-Organizer

A powerful, intelligent file organization tool that automatically sorts your files based on customizable rules. Similar to organize by tfeldmann, but with watch mode, SQLite history tracking, and batch undo capabilities.

## Features

### Core Features
- YAML-based Rules Engine - Define file organization rules declaratively
- Watch Mode - Automatic real-time monitoring and organizing of new files
- SQLite History - Complete audit trail with batch_id tracking
- Batch Undo - Revert entire file organization sessions
- Dry-run Mode - Preview changes before applying
- Interactive Confirmation - Approve changes before executing

### Advanced Matchers
- Extension matching (.pdf, .docx, etc.)
- Filename pattern matching (starts with, contains, ends with)
- Regular expression patterns
- Extensible matcher architecture for custom logic

## Quick Start

### Installation
\\\ash
git clone https://github.com/HectorA15/Sorted.git
cd Sorted
pip install -r requirements.txt
\\\

### Usage
\\\ash
python -m cli.main
\\\

Then select:
- Option 1: Manual organize (dry-run + confirm)
- Option 2: Watch mode (automatic monitoring)
- Option 3: Undo last batch

## Configuration

Edit rules.yaml to define your organization rules.

## Architecture
- core/ - File operations
- engine/ - Rules engine and matchers
- cli/ - Interactive CLI and watch mode
- persistence/ - SQLite database

## License

MIT License
