"""
Action manager module for handling game actions
"""
from dataclasses import dataclass
from typing import Callable, List, Any, Optional

@dataclass
class Action:
    """Class representing an action in the game"""
    name: str
    callback: Callable
    args: Optional[Any] = None
    
    def execute(self):
        """Execute the action"""
        if self.args is not None:
            return self.callback(self.args)
        else:
            return self.callback()

class ActionManager:
    """Manager for handling available actions in the game"""
    
    def __init__(self, config):
        """Initialize the action manager"""
        self.config = config
        self.actions = []
    
    def add_action(self, name, callback, args=None):
        """Add a new action to the available actions"""
        action = Action(name, callback, args)
        self.actions.append(action)
        return action
    
    def clear_actions(self):
        """Clear all actions"""
        self.actions.clear()
    
    def get_actions(self) -> List[Action]:
        """Get all available actions"""
        return self.actions
    
    def get_action_by_name(self, name):
        """Get an action by its name"""
        for action in self.actions:
            if action.name.lower() == name.lower():
                return action
        return None
    
    def execute_action(self, name):
        """Execute an action by its name"""
        action = self.get_action_by_name(name)
        if action:
            return action.execute()
        return False 