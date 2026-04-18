from utils.file_handler import FileHandler
from services.user_service import UserService, FriendService
from services.post_service import PostService
from services.feed_service import FeedService
from services.history_service import HistoryService
from ui.main_ui import MainUI
import datetime

def initialize_system():
    FileHandler.ensure_data_files()
    
    user_service = UserService()
    post_service = PostService()
    friend_service = FriendService(user_service)
    feed_service = FeedService(post_service, friend_service)
    history_service = HistoryService()
    
    return user_service, post_service, feed_service, friend_service, history_service

def main():
    user_service, post_service, feed_service, friend_service, history_service = initialize_system()
    
    app = MainUI(user_service, post_service, feed_service, friend_service, history_service)
    app.run()

if __name__ == "__main__":
    main()