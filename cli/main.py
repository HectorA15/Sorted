import uuid
from core.fs_utils import get_desktop_path
from engine.engine import apply_rules, dry_run
from cli.config import file_destinations


DESKTOP = get_desktop_path()

if __name__ == "__main__":
    batch_id = uuid.uuid4().hex  # One batch id per manual run

    results = dry_run(DESKTOP, file_destinations)
    for result in results:
        print(result)
    print('-------------------------------------')

    confirm = input('Confirm changes? (y/n): ').strip().lower() in ("y", "yes")
    if confirm:
        results = apply_rules(source_directory=DESKTOP, rules=file_destinations, batch_id=batch_id)
        for result in results:
            print(result)

