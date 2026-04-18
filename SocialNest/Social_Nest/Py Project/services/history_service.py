from core.stack import Stack
from utils.file_handler import FileHandler
import time

class HistoryService:
    def __init__(self):
        self.history_stack = Stack()
        self.load_history()
    
    def load_history(self):
        data = FileHandler.read_json('data/history.json')
        for item in data:
            self.history_stack.push(item)
    
    def save_history(self):
        data = self.history_stack.to_list()
        FileHandler.write_json('data/history.json', data)
    
    def add_action(self, action_type, data):
        action = {
            'type': action_type,
            'data': data,
            'timestamp': time.time()
        }
        self.history_stack.push(action)
        self.save_history()
    
    def undo_last_action(self):
        if not self.history_stack.is_empty():
            action = self.history_stack.pop()
            self.save_history()
            return action
        return None
    
    def get_history(self):
        return self.history_stack.to_list()
    
    def clear_history(self):
        self.history_stack.clear()
        self.save_history()