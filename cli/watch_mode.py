from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
import uuid
from core.fs_utils import move_file, get_desktop_path
from persistence.sqlite import FileHistoryDB
from cli.config import file_destinations


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

    def on_created(self, event):
        if event.is_directory:
            return
        # avoid moving partially written files
        if not wait_until_stable(event.src_path, checks=2, interval=1.0):
            print(f"Skipped (not stable): {event.src_path}")
            return

        file_extension = Path(event.src_path).suffix
        if file_extension in file_destinations:
            db = FileHistoryDB()
            batch_id = uuid.uuid4().hex  # one batch per moved file in watch mode
            destination = file_destinations[file_extension]
            move_file(event.src_path, destination)
            db.log_move(batch_id, event.src_path, destination, file_extension)
            db.close()
            print(f"{event.src_path} -> {destination}")
            

#create Observer
observer = Observer()

# Tell observer what to watch and what handler to use
observer.schedule(MyHandler(), path=get_desktop_path(), recursive=False)

# Start watching
observer.start()

# Keep it running (Ctrl+C to stop)
try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()


