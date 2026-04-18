import json
import os

class FileHandler:
    @staticmethod
    def read_json(filepath):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []
    
    @staticmethod
    def write_json(filepath, data):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    
    @staticmethod
    def ensure_data_files():
        files = {
            'data/users.json': [],
            'data/posts.json': [],
            'data/friends.json': [],
            'data/history.json': []
        }
        
        for filepath, default_data in files.items():
            if not os.path.exists(filepath):
                FileHandler.write_json(filepath, default_data)