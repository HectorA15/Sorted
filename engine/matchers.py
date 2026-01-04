import re
from pathlib import Path

class Matcher:
    def matches(self, file_path):
        raise NotImplementedError
    
class ExtensionMatcher(Matcher):
    def __init__(self, extensions):
        if isinstance(extensions, str):
            self.extensions = [extensions]
        else:
            self.extensions = extensions
    
    def matches(self, file_path):
        ext = Path(file_path).suffix.lstrip('.')  # .pdf → pdf
        return ext in self.extensions

class NameStartsWithMatcher(Matcher):
    def __init__(self, prefix):
        self.prefix = prefix
    
    def matches(self, file_path):
        name = Path(file_path).stem  # File.pdf → File
        return name.startswith(self.prefix)
   
   
class NameContainsMatcher(Matcher):
    def __init__(self, prefix):
        self.prefix = prefix
        
    def matches(self, file_path):
        name = Path(file_path).stem 
        return self.prefix in name
    
class NameEndsWithMatcher(Matcher):
    def __init__(self, prefix):
        self.prefix = prefix
        
    def matches(self, file_path):
        name = Path(file_path).stem 
        return name.endswith(self.prefix)
    
class RegexMatcher(Matcher):
    def __init__(self, pattern):
        self.pattern = pattern
        self.regex = re.compile(pattern)
    
    def matches(self, file_path):
        name = Path(file_path).stem
        return self.regex.search(name) is not None