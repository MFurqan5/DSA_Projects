from core.queue import Queue
from core.sort import Sort
from core.search import Search

class FeedService:
    def __init__(self, post_service, friend_service):
        self.post_service = post_service
        self.friend_service = friend_service
        self.feed_queue = Queue()
    
    def generate_feed(self, user_id):
        self.feed_queue.clear()
        
        friends = self.friend_service.get_friends(user_id)
        friend_ids = [f.user_id for f in friends]
        friend_ids.append(user_id)
        
        all_posts = self.post_service.get_all_posts()
        
        feed_posts = [p for p in all_posts if p.user_id in friend_ids]
        
        feed_posts = Sort.quick_sort(feed_posts, key='created_at', reverse=True)
        
        for post in feed_posts:
            self.feed_queue.enqueue(post)
        
        return self.feed_queue.to_list()
    
    def get_feed(self, user_id):
        return self.generate_feed(user_id)
    
    def get_trending_posts(self):
        all_posts = self.post_service.get_all_posts()
        sorted_posts = Sort.quick_sort(all_posts, key='likes', reverse=True)
        return sorted_posts[:10]
    
    def search_posts(self, keyword):
        all_posts = self.post_service.get_all_posts()
        return Search.search_by_keyword(all_posts, keyword, 'content')
    
    def sort_feed_by_likes(self, user_id):
        feed = self.get_feed(user_id)
        return Sort.quick_sort(feed, key='likes', reverse=True)
    
    def sort_feed_by_date(self, user_id):
        feed = self.get_feed(user_id)
        return Sort.quick_sort(feed, key='created_at', reverse=True)