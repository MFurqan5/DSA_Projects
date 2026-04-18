from utils.file_handler import FileHandler
import time

class Post:
    def __init__(self, post_id, user_id, content, likes=0, comments=None, created_at=None, edited_at=None):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.likes = likes
        self.comments = comments or []
        self.created_at = created_at or time.time()
        self.edited_at = edited_at
        self.liked_by = []
    
    def to_dict(self):
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'likes': self.likes,
            'comments': self.comments,
            'created_at': self.created_at,
            'edited_at': self.edited_at,
            'liked_by': self.liked_by
        }
    
    @staticmethod
    def from_dict(data):
        post = Post(
            data['post_id'],
            data['user_id'],
            data['content'],
            data.get('likes', 0),
            data.get('comments', []),
            data.get('created_at'),
            data.get('edited_at')
        )
        post.liked_by = data.get('liked_by', [])
        return post

class PostService:
    def __init__(self):
        self.posts = []
        self.load_posts()
    
    def load_posts(self):
        data = FileHandler.read_json('data/posts.json')
        self.posts = [Post.from_dict(p) for p in data]
    
    def save_posts(self):
        data = [p.to_dict() for p in self.posts]
        FileHandler.write_json('data/posts.json', data)
    
    def create_post(self, user_id, content):
        post_id = len(self.posts) + 1
        post = Post(post_id, user_id, content)
        self.posts.append(post)
        self.save_posts()
        return post
    
    def get_post_by_id(self, post_id):
        for post in self.posts:
            if post.post_id == post_id:
                return post
        return None
    
    def update_post(self, post_id, content):
        post = self.get_post_by_id(post_id)
        if post:
            post.content = content
            post.edited_at = time.time()
            self.save_posts()
            return post
        return None
    
    def delete_post(self, post_id):
        post = self.get_post_by_id(post_id)
        if post:
            self.posts.remove(post)
            self.save_posts()
            return True
        return False
    
    def like_post(self, post_id, user_id):
        post = self.get_post_by_id(post_id)
        if post:
            if user_id not in post.liked_by:
                post.likes += 1
                post.liked_by.append(user_id)
                self.save_posts()
                return True
        return False
    
    def unlike_post(self, post_id, user_id):
        post = self.get_post_by_id(post_id)
        if post:
            if user_id in post.liked_by:
                post.likes -= 1
                post.liked_by.remove(user_id)
                self.save_posts()
                return True
        return False
    
    def add_comment(self, post_id, user_id, comment_text):
        post = self.get_post_by_id(post_id)
        if post:
            comment = {
                'user_id': user_id,
                'comment': comment_text,
                'created_at': time.time()
            }
            post.comments.append(comment)
            self.save_posts()
            return True
        return False
    
    def get_user_posts(self, user_id):
        return [p for p in self.posts if p.user_id == user_id]
    
    def get_all_posts(self):
        return self.posts