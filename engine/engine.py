
from persistence.sqlite import FileHistoryDB
from core.fs_utils import move_file, get_desktop_path
from engine.rules import load_rules, Rule

def apply_rules(source_directory, rules_yaml_path, batch_id):
    rules = load_rules(rules_yaml_path)  # Cargar del YAML
    db = FileHistoryDB()  # keep one DB session per run
    logs = []
    for rule in rules:
        files = source_directory.glob(f"**/*")
        for file in files:
            try:  
                if rule.matches(file):
                    result = rule.apply(file)
                    db.log_move(
                        batch_id,
                        str(result["source"]),          # ← str()
                        str(result["destination"]),     # ← str()
                        result["rule_name"]
                    )
                    break
            except Exception as e:
                print(f"Error moving {file}: {e}")
    
    db.close()
    return logs 
    
def dry_run(source_directory, rules_yaml_path):
    rules = load_rules(rules_yaml_path)
    logs = []
    
    for rule in rules:
        files = source_directory.glob(f"**/*")
        for file in files:
            if file.is_file() and rule.matches(str(file)):
                destination = rule.actions[0].destination
                # Normalizar paths para comparar
                file_str = str(file).replace("\\", "/")
                dest_str = destination.replace("\\", "/")
                
                if not file_str.startswith(dest_str):
                    logs.append(f"{file} --> {destination}")
    
    return logs