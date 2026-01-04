from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
import uuid
from core.fs_utils import get_desktop_path
from persistence.sqlite import FileHistoryDB
from engine.rules import load_rules

rules_path = Path(__file__).parent.parent / "rules.yaml"
rules = load_rules(str(rules_path))

def wait_until_stable(path, checks=3, interval=1.0):
    """Return True when size is unchanged for `checks` consecutive samples."""
    p = Path(path)
    if not p.exists():
        return False
    last_size = None
    stable = 0
    for _ in range(checks * 2):  # give it some tries
        if not p.exists():
            return False
        size = p.stat().st_size
        if size == last_size:
            stable += 1
            if stable >= checks:
                return True
        else:
            stable = 0
        last_size = size
        time.sleep(interval)
    return False

class MyHandler(FileSystemEventHandler):
    def __init__(self, rules):
        self.rules = rules
        self.processed = set()

    def _try_process(self, event, checks=3, interval=1.0):
        """Intenta procesar un archivo. Devuelve True si lo procesó, False si no."""
        if event.is_directory or event.src_path in self.processed:
            return False
        
        name = Path(event.src_path).stem.lower()
        
        # Ignorar archivos con nombre default (el usuario aún no los renombró)
        default_names = ["nuevo documento", "document", "new file", "sin nombre", "untitled"]
        if any(default in name for default in default_names):
            return False  # Esperar a que on_modified lo agarre cuando cambien de nombre
        
        if not wait_until_stable(event.src_path, checks=checks, interval=interval):
            return False
        
        db = FileHistoryDB()
        
        for rule in self.rules:
            if rule.matches(event.src_path):
                try:
                    result = rule.apply(event.src_path)
                    batch_id = uuid.uuid4().hex
                    db.log_move(
                        batch_id,
                        str(result["source"]),
                        str(result["destination"]),
                        result["rule_name"]
                    )
                    print(f"Moved: {event.src_path} -> {result['destination']}")
                    self.processed.add(event.src_path)
                    db.close()
                    return True
                except Exception as e:
                    print(f"Error: {e}")
        
        db.close()
        return False

    def on_created(self, event):
        # Intento inmediato para archivos rápidos (copias, archivos pequeños)
        time.sleep(2)
        self._try_process(event, checks=2, interval=0.5)

    def on_modified(self, event):
        # Backup para archivos que tardan (descargas, renombrados)
        self._try_process(event, checks=4, interval=1.0)
            
#create Observer
observer = Observer()



# Tell observer what to watch and what handler to use
observer.schedule(MyHandler(rules), path=get_desktop_path(), recursive=False)

# Start watching
observer.start()

# Keep it running (Ctrl+C to stop)
try:
    while True:
        time.sleep(1) # avoid high CPU
except KeyboardInterrupt:
    observer.stop()

observer.join()


