from typing import Union 
from pathlib import Path
import shutil
import time
import os

#function to move files
def move_file(source: Union[str,Path], dest_dir:  Union[str,Path]) -> Path:
    
    src = Path(source)
    dest = Path(dest_dir)
    
    if not src.exists():
        raise FileNotFoundError(src)
    if not src.is_file():
        raise IsADirectoryError(src)
    else:
        dest.mkdir(parents=True, exist_ok=True)
        dest_path = dest / src.name
        
    i = 1
    while dest_path.exists(): 
        dest_path = dest / f"{src.stem} ({i}){src.suffix}"
        i += 1 
        
    shutil.move(str(src), str(dest_path))
    return dest_path


#function to locate the desktop path to reach the files
def get_desktop_path() -> Path:
    
    HOME = Path.home()
    desktop_candidates = [
        Path(os.environ.get("OneDrive", "")) / "Desktop",
        HOME / "OneDrive" / "Desktop",
        HOME / "Desktop",
        HOME / "Escritorio",
    ]
    DESKTOP = next((p for p in desktop_candidates if p.exists()), HOME / "Desktop")
    return DESKTOP

