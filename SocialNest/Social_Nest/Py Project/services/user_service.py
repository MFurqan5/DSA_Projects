# services/user_service.py
from utils.file_handler import FileHandler
from core.linked_list import LinkedList
import time

class User:
    def __init__(self, user_id, username, email, password="", name="", bio="", profile_pic="", created_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password        # ← ADDED
        self.name = name or username    # ← ADDED (fallback to username)
        self.bio = bio
        self.profile_pic = profile_pic
        self.created_at = created_at or time.time()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password': self.password,      # ← ADDED
            'name': self.name,              # ← ADDED
            'bio': self.bio,
            'profile_pic': self.profile_pic,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            data['user_id'],
            data['username'],
            data['email'],
            data.get('password', ''),           # old users won't have password
            data.get('name', data['username']), # old users won't have name
            data.get('bio', ''),
            data.get('profile_pic', ''),
            data.get('created_at')
        )

class UserService:
    def __init__(self):
        self.users = []
        self.current_user = None
        self.load_users()
    
    def load_users(self):
        data = FileHandler.read_json('data/users.json')
        self.users = [User.from_dict(u) for u in data]
    
    def save_users(self):
        data = [u.to_dict() for u in self.users]
        FileHandler.write_json('data/users.json', data)
    
    def create_user(self, username, email, password="", name=""):  # ← password + name added
        if self.get_user_by_username(username):
            return None
        
        user_id = len(self.users) + 1
        user = User(user_id, username, email, password, name)     # ← pass new fields
        self.users.append(user)
        self.save_users()
        return user
    
    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def get_user_by_username(self, username):
        for user in self.users:
            if user.username.lower() == username.lower():
                return user
        return None
    
    def update_user(self, user_id, username=None, email=None, bio=None):
        user = self.get_user_by_id(user_id)
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            if bio is not None:
                user.bio = bio
            self.save_users()
            return user
        return None
    
    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            self.save_users()
            return True
        return False
    
    def login(self, username, password=""):  # ← password added
        user = self.get_user_by_username(username)
        if user and user.password == password:  # ← check password
            self.current_user = user
            return user
        return None
    
    def logout(self):
        self.current_user = None
    
    def get_all_users(self):
        return self.users

class FriendService:
    def __init__(self, user_service):
        self.user_service = user_service
        self.friends_data = {}
        self.load_friends()
    
    def load_friends(self):
        data = FileHandler.read_json('data/friends.json')
        self.friends_data = {}
        for item in data:
            user_id = item['user_id']
            friends_list = LinkedList()
            for friend_id in item['friends']:
                friends_list.append(friend_id)
            self.friends_data[user_id] = friends_list
    
    def save_friends(self):
        data = []
        for user_id, friends_list in self.friends_data.items():
            data.append({
                'user_id': user_id,
                'friends': friends_list.to_list()
            })
        FileHandler.write_json('data/friends.json', data)
    
    def add_friend(self, user_id, friend_id):
        if user_id not in self.friends_data:
            self.friends_data[user_id] = LinkedList()
        
        if not self.friends_data[user_id].search(friend_id):
            self.friends_data[user_id].append(friend_id)
            
            if friend_id not in self.friends_data:
                self.friends_data[friend_id] = LinkedList()
            if not self.friends_data[friend_id].search(user_id):
                self.friends_data[friend_id].append(user_id)
            
            self.save_friends()
            return True
        return False
    
    def remove_friend(self, user_id, friend_id):
        if user_id in self.friends_data:
            self.friends_data[user_id].remove(friend_id)
        
        if friend_id in self.friends_data:
            self.friends_data[friend_id].remove(user_id)
        
        self.save_friends()
        return True
    
    def get_friends(self, user_id):
        if user_id not in self.friends_data:
            return []
        
        friend_ids = self.friends_data[user_id].to_list()
        friends = []
        for fid in friend_ids:
            user = self.user_service.get_user_by_id(fid)
            if user:
                friends.append(user)
        return friends
    
    def is_friend(self, user_id, friend_id):
        if user_id in self.friends_data:
            return self.friends_data[user_id].search(friend_id)
        return False