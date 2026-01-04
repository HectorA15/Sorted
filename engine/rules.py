import yaml
from .matchers import Matcher, ExtensionMatcher, NameStartsWithMatcher, NameEndsWithMatcher, NameContainsMatcher, RegexMatcher
from .actions import MoveAction

class Rule:
    def __init__(self, name, matchers, actions, priority=10):
        self.name = name
        self.matchers = matchers      # Lista de Matcher objects
        self.actions = actions        # Lista de Action objects
        self.priority = priority
    
    def matches(self, file_path):
        for matcher in self.matchers:
            if not matcher.matches(file_path):  # Llama el método
                return False
        return True
    
    def apply(self, file_path):
        result = {
            "source": file_path,
            "destination": None,
            "rule_name": self.name
        }
        
        for action in self.actions:
            if isinstance(action, MoveAction):
                action.execute(file_path)
                result["destination"] = action.destination
                
        return result
            


def load_matchers(filters_list):
    matchers = []
    for filter_dict in filters_list:
        
        if 'extension' in filter_dict:
            matcher = ExtensionMatcher(filter_dict['extension'])
            matchers.append(matcher)
            
        if 'name_contains' in filter_dict:
            matcher = NameContainsMatcher(filter_dict['name_contains'])
            matchers.append(matcher)
        
        if 'name_starts_with' in filter_dict:
            matcher = NameStartsWithMatcher(filter_dict['name_starts_with'])
            matchers.append(matcher)
        
        if 'name_ends_with' in filter_dict:
            matcher = NameEndsWithMatcher(filter_dict['name_ends_with'])
            matchers.append(matcher)
            
        if 'name_pattern' in filter_dict:
            matcher = RegexMatcher(filter_dict['name_pattern'])
            matchers.append(matcher)

    return matchers



def load_rules(yaml_path):
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    
    rules = []
    for rule_dict in config['rules']:
        name = rule_dict['name']
        priority = rule_dict.get('priority', 10)  # default 10
        matchers = load_matchers(rule_dict['filters'])
        actions = load_actions(rule_dict['actions'])  # similar a load_matchers
        
        rule = Rule(name, matchers, actions, priority)
        rules.append(rule)
    
    # Ordenar por prioridad (menor número = más prioritario)
    rules.sort(key=lambda r: r.priority)
    return rules

def load_actions(actions_list):
    actions = []
    for action_dict in actions_list:
        if 'move' in action_dict:
            destination = action_dict['move']
            action = MoveAction(destination)
            actions.append(action)
            
    return actions