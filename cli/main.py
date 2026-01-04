import uuid
from core.fs_utils import get_desktop_path
from engine.engine import apply_rules, dry_run


DESKTOP = get_desktop_path()

if __name__ == "__main__":
    batch_id = uuid.uuid4().hex  # One batch id per manual run
    rules_path = "rules.yaml"
    results = dry_run(DESKTOP, rules_path)
    if results:
        for result in results:
            print(result)
        print('-------------------------------------')
        confirm = input('Confirm changes? (y/n): ').strip().lower() in ("y", "yes")
        if confirm:
            results = apply_rules(source_directory=DESKTOP, rules_yaml_path=rules_path, batch_id=batch_id)
            for result in results:
                print(result)
    else:
        print('no changes')

