
from persistence.sqlite import FileHistoryDB
from core.fs_utils import move_file, get_desktop_path


def apply_rules(source_directory, rules, batch_id):
    logs = []
    db = FileHistoryDB()  # keep one DB session per run
    
    for extension, dest_folder in rules.items():
        matching_files = list(source_directory.glob(f"**/*{extension}"))
        matching_files = [f for f in matching_files if not str(f).startswith(dest_folder)]
        
        for file_path in matching_files:
            try:
                source_file = str(file_path)
                move_record = f'{source_file} --> {dest_folder}'
                logs.append(move_record)
                move_file(source=source_file, dest_dir=dest_folder)
                db.log_move(batch_id, source_file, dest_folder, extension)
            except Exception as e:
                print(f"Error moving {file_path}: {e}")
    
    db.close()
    return logs
    
def dry_run(source_directory, rules):
    
    logs = []
    
    for extension, dest_folder in rules.items():
        matching_files = list(source_directory.glob(f"**/*{extension}"))
        matching_files = [f for f in matching_files if not str(f).startswith(dest_folder)]
        
        for file_path in matching_files:
            source_file = str(file_path)
            move_record = f'{source_file} --> {dest_folder}'
            logs.append(move_record)

    return logs