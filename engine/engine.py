
from persistence.sqlite import FileHistoryDB
from core.fs_utils import move_file, get_desktop_path
from engine.rules import load_rules, Rule

def apply_rules(source_directory, rules_yaml_path, batch_id):
    rules = load_rules(rules_yaml_path)
    db = FileHistoryDB()
    logs = []
    
    files = list(source_directory.glob(f"**/*"))
    for file in files:
        if not file.is_file():
            continue
        
        for rule in rules:
            try:  
                if rule.matches(file):
                    # Skip if already inside destination
                    destination = rule.actions[0].destination
                    file_str = str(file).replace("\\", "/")
                    dest_str = str(destination).replace("\\", "/")
                    if file_str.startswith(dest_str.rstrip("/")):
                        break

                    result = rule.apply(file)
                    db.log_move(
                        batch_id,
                        str(result["source"]),
                        str(result["destination"]),
                        result["rule_name"]
                    )
                    logs.append(result)
                    break  # First matching rule wins
            except Exception as e:
                print(f"Error moving {file}: {e}")
    
    db.close()
    return logs 
    
def dry_run(source_directory, rules_yaml_path):
    rules = load_rules(rules_yaml_path)
    logs = []
    
    files = list(source_directory.glob(f"**/*"))
    for file in files:
        if not file.is_file():
            continue
        
        for rule in rules:
            if rule.matches(file):
                destination = rule.actions[0].destination
                # Normalize paths for comparison
                file_str = str(file).replace("\\", "/")
                dest_str = destination.replace("\\", "/")
                
                if not file_str.startswith(dest_str):
                    logs.append(f"{file} --> {destination}")
                break  # First matching rule wins
    
    return logs
