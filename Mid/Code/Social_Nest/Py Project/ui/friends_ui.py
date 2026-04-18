import customtkinter as ctk
from ui.theme import Theme
from core.sort import Sort
from core.search import Search
import datetime


class FriendsUI:
    def __init__(self, parent, user_service, friend_service):
        self.parent = parent
        self.user_service = user_service
        self.friend_service = friend_service
        self.user = user_service.current_user
        
        self.setup_ui()
    
    def setup_ui(self):
        header_frame = ctk.CTkFrame(self.parent)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(header_frame, text="Friends", 
                            font=(Theme.FONT_FAMILY, 28, "bold"))
        title.pack(side="left", padx=10)
        
        add_friend_btn = ctk.CTkButton(header_frame, text="+ Add Friend", width=150,
                                      command=self.show_add_friend_dialog)
        add_friend_btn.pack(side="right", padx=10)
        
        search_frame = ctk.CTkFrame(self.parent)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Search Friends:",
                                   font=(Theme.FONT_FAMILY, 14))
        search_label.pack(side="left", padx=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=250,
                                        placeholder_text="Enter username...")
        self.search_entry.pack(side="left", padx=5)
        
        search_btn = ctk.CTkButton(search_frame, text="Search", width=80,
                                  command=self.search_friends)
        search_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(search_frame, text="Clear", width=80,
                                 command=self.clear_search)
        clear_btn.pack(side="left", padx=5)
        
        sort_frame = ctk.CTkFrame(self.parent)
        sort_frame.pack(fill="x", padx=20, pady=10)
        
        sort_label = ctk.CTkLabel(sort_frame, text="Sort by:",
                                 font=(Theme.FONT_FAMILY, 14))
        sort_label.pack(side="left", padx=10)
        
        alpha_btn = ctk.CTkButton(sort_frame, text="A-Z", width=80,
                                 command=lambda: self.sort_friends("alpha"))
        alpha_btn.pack(side="left", padx=5)
        
        self.friends_frame = ctk.CTkScrollableFrame(self.parent)
        self.friends_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        self.load_friends()
    
    def load_friends(self, friends_list=None):
        for widget in self.friends_frame.winfo_children():
            widget.destroy()
        
        if friends_list is None:
            friends = self.friend_service.get_friends(self.user.user_id)
        else:
            friends = friends_list
        
        if not friends:
            no_friends = ctk.CTkLabel(self.friends_frame, text="No friends yet. Add some friends!",
                                     font=(Theme.FONT_FAMILY, 16), text_color="gray")
            no_friends.pack(pady=50)
        else:
            for friend in friends:
                self.create_friend_widget(friend)
    
    def create_friend_widget(self, friend):
        friend_frame = ctk.CTkFrame(self.friends_frame)
        friend_frame.pack(fill="x", pady=10, padx=10)
        
        info_frame = ctk.CTkFrame(friend_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        username_label = ctk.CTkLabel(info_frame, text=f"@{friend.username}",
                                     font=(Theme.FONT_FAMILY, 16, "bold"))
        username_label.pack(anchor="w")
        
        email_label = ctk.CTkLabel(info_frame, text=friend.email,
                                  font=(Theme.FONT_FAMILY, 12), text_color="gray")
        email_label.pack(anchor="w")
        
        if friend.bio:
            bio_label = ctk.CTkLabel(info_frame, text=friend.bio,
                                    font=(Theme.FONT_FAMILY, 11), wraplength=500)
            bio_label.pack(anchor="w", pady=5)
        
        button_frame = ctk.CTkFrame(friend_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=10)
        
        view_btn = ctk.CTkButton(button_frame, text="View Posts", width=100, height=30,
                                command=lambda: self.view_friend_posts(friend))
        view_btn.pack(side="left", padx=5)
        
        remove_btn = ctk.CTkButton(button_frame, text="Unfriend", width=100, height=30,
                                  fg_color=Theme.DANGER,
                                  command=lambda: self.remove_friend(friend))
        remove_btn.pack(side="left", padx=5)
    
    def show_add_friend_dialog(self):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Add Friend")
        dialog.geometry("500x400")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Add Friend",
                            font=(Theme.FONT_FAMILY, 20, "bold"))
        title.pack(pady=20)
        
        search_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="Search users:",
                                   font=(Theme.FONT_FAMILY, 14))
        search_label.pack(anchor="w", pady=5)
        
        search_entry = ctk.CTkEntry(search_frame, width=400,
                                   placeholder_text="Enter username...")
        search_entry.pack(pady=5)
        
        results_frame = ctk.CTkScrollableFrame(dialog, height=200)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        def search_users():
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            query = search_entry.get().strip().lower()
            if query:
                all_users = self.user_service.get_all_users()
                matching_users = [u for u in all_users 
                                if query in u.username.lower() 
                                and u.user_id != self.user.user_id
                                and not self.friend_service.is_friend(self.user.user_id, u.user_id)]
                
                if not matching_users:
                    no_results = ctk.CTkLabel(results_frame, text="No users found",
                                            text_color="gray")
                    no_results.pack(pady=20)
                else:
                    for user in matching_users:
                        user_frame = ctk.CTkFrame(results_frame)
                        user_frame.pack(fill="x", pady=5, padx=5)
                        
                        user_label = ctk.CTkLabel(user_frame, text=f"@{user.username}",
                                                 font=(Theme.FONT_FAMILY, 14))
                        user_label.pack(side="left", padx=10)
                        
                        add_btn = ctk.CTkButton(user_frame, text="Add", width=80,
                                              command=lambda u=user: self.add_friend(u, dialog))
                        add_btn.pack(side="right", padx=10, pady=5)
        
        search_btn = ctk.CTkButton(dialog, text="Search", width=150,
                                  command=search_users)
        search_btn.pack(pady=10)
    
    def add_friend(self, friend, dialog):
        if self.friend_service.add_friend(self.user.user_id, friend.user_id):
            self.load_friends()
            dialog.destroy()
    
    def remove_friend(self, friend):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Confirm Unfriend")
        dialog.geometry("400x200")
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, 
                            text=f"Are you sure you want to unfriend @{friend.username}?",
                            font=(Theme.FONT_FAMILY, 14))
        label.pack(pady=30)
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def confirm():
            self.friend_service.remove_friend(self.user.user_id, friend.user_id)
            self.load_friends()
            dialog.destroy()
        
        yes_btn = ctk.CTkButton(button_frame, text="Yes", width=100,
                               fg_color=Theme.DANGER, command=confirm)
        yes_btn.pack(side="left", padx=10)
        
        no_btn = ctk.CTkButton(button_frame, text="No", width=100,
                              command=dialog.destroy)
        no_btn.pack(side="left", padx=10)
    
    def view_friend_posts(self, friend):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"@{friend.username}'s Posts")
        dialog.geometry("700x600")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text=f"@{friend.username}'s Posts",
                            font=(Theme.FONT_FAMILY, 20, "bold"))
        title.pack(pady=20)
        
        posts_frame = ctk.CTkScrollableFrame(dialog)
        posts_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        friend_posts = self.user_service.post_service.get_user_posts(friend.user_id) if hasattr(self.user_service, 'post_service') else []
        
        from services.post_service import PostService
        post_service = PostService()
        friend_posts = post_service.get_user_posts(friend.user_id)
        friend_posts.sort(key=lambda x: x.created_at, reverse=True)
        
        if not friend_posts:
            no_posts = ctk.CTkLabel(posts_frame, text="No posts yet",
                                   font=(Theme.FONT_FAMILY, 14), text_color="gray")
            no_posts.pack(pady=50)
        else:
            for post in friend_posts:
                post_widget = ctk.CTkFrame(posts_frame)
                post_widget.pack(fill="x", pady=10, padx=10)
                
                date_str = datetime.datetime.fromtimestamp(post.created_at).strftime("%b %d, %Y")
                date_label = ctk.CTkLabel(post_widget, text=date_str,
                                         font=(Theme.FONT_FAMILY, 10), text_color="gray")
                date_label.pack(anchor="w", padx=10, pady=5)
                
                content_label = ctk.CTkLabel(post_widget, text=post.content,
                                            font=(Theme.FONT_FAMILY, 13), wraplength=600)
                content_label.pack(anchor="w", padx=10, pady=10)
                
                stats_label = ctk.CTkLabel(post_widget, 
                                          text=f"❤️ {post.likes} likes • 💬 {len(post.comments)} comments",
                                          font=(Theme.FONT_FAMILY, 11), text_color="gray")
                stats_label.pack(anchor="w", padx=10, pady=5)
    
    def search_friends(self):
        query = self.search_entry.get().strip().lower()
        if query:
            all_friends = self.friend_service.get_friends(self.user.user_id)
            matching_friends = [f for f in all_friends if query in f.username.lower()]
            self.load_friends(matching_friends)
        else:
            self.load_friends()
    
    def clear_search(self):
        self.search_entry.delete(0, "end")
        self.load_friends()
    
    def sort_friends(self, sort_type):
        friends = self.friend_service.get_friends(self.user.user_id)
        if sort_type == "alpha":
            friends = Sort.quick_sort(friends, key='username')
        self.load_friends(friends)