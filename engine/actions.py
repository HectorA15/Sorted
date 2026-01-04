from pathlib import Path
from core.fs_utils import move_file

class Action:
    def execute(self, file_path):
        raise NotImplementedError

class MoveAction(Action):
    def __init__(self, destination):
        self.destination = destination
    
    def execute(self, file_path):
        move_file(file_path, self.destination)