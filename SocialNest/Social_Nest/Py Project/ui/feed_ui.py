import customtkinter as ctk
from ui.theme import Theme
import datetime
from core.sort import Sort

class FeedUI:
    def __init__(self, parent, user_service, post_service, feed_service, friend_service, history_service):
        self.parent = parent
        self.user_service = user_service
        self.post_service = post_service
        self.feed_service = feed_service
        self.friend_service = friend_service
        self.history_service = history_service
        self.user = user_service.current_user
        
        self.current_filter = "recent"
        self.search_query = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        header_frame = ctk.CTkFrame(self.parent)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title = ctk.CTkLabel(header_frame, text="Feed", 
                            font=(Theme.FONT_FAMILY, 28, "bold"))
        title.pack(side="left", padx=10)
        
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=250, 
                                        placeholder_text="Search posts...")
        self.search_entry.pack(side="left", padx=5)
        
        search_btn = ctk.CTkButton(search_frame, text="Search", width=80,
                                  command=self.search_posts)
        search_btn.pack(side="left", padx=5)
        
        filter_frame = ctk.CTkFrame(self.parent)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        filter_label = ctk.CTkLabel(filter_frame, text="Sort by:",
                                   font=(Theme.FONT_FAMILY, 14))
        filter_label.pack(side="left", padx=10)
        
        recent_btn = ctk.CTkButton(filter_frame, text="Recent", width=100,
                                  command=lambda: self.apply_filter("recent"))
        recent_btn.pack(side="left", padx=5)
        
        popular_btn = ctk.CTkButton(filter_frame, text="Popular", width=100,
                                   command=lambda: self.apply_filter("popular"))
        popular_btn.pack(side="left", padx=5)
        
        trending_btn = ctk.CTkButton(filter_frame, text="Trending", width=100,
                                    command=lambda: self.apply_filter("trending"))
        trending_btn.pack(side="left", padx=5)
        
        undo_btn = ctk.CTkButton(filter_frame, text="⟲ Undo", width=80,
                                fg_color=Theme.WARNING,
                                command=self.undo_action)
        undo_btn.pack(side="right", padx=10)
        
        self.posts_frame = ctk.CTkScrollableFrame(self.parent)
        self.posts_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        self.load_feed()
    
    def load_feed(self):
        for widget in self.posts_frame.winfo_children():
            widget.destroy()
        
        if self.search_query:
            posts = self.feed_service.search_posts(self.search_query)
        elif self.current_filter == "trending":
            posts = self.feed_service.get_trending_posts()
        elif self.current_filter == "popular":
            posts = self.feed_service.sort_feed_by_likes(self.user.user_id)
        else:
            posts = self.feed_service.get_feed(self.user.user_id)
        
        if not posts:
            no_posts = ctk.CTkLabel(self.posts_frame, text="No posts to display",
                                   font=(Theme.FONT_FAMILY, 16), text_color="gray")
            no_posts.pack(pady=50)
        else:
            for post in posts:
                self.create_post_widget(post)
    
    def create_post_widget(self, post):
        post_frame = ctk.CTkFrame(self.posts_frame)
        post_frame.pack(fill="x", pady=10, padx=10)
        
        author = self.user_service.get_user_by_id(post.user_id)
        author_name = author.username if author else "Unknown"
        
        header = ctk.CTkFrame(post_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=5)
        
        author_label = ctk.CTkLabel(header, text=f"@{author_name}",
                                   font=(Theme.FONT_FAMILY, 14, "bold"))
        author_label.pack(side="left", padx=5)
        
        date_str = datetime.datetime.fromtimestamp(post.created_at).strftime("%b %d, %I:%M %p")
        date_label = ctk.CTkLabel(header, text=date_str,
                                 font=(Theme.FONT_FAMILY, 10), text_color="gray")
        date_label.pack(side="left", padx=5)
        
        if post.edited_at:
            edited_label = ctk.CTkLabel(header, text="(edited)",
                                       font=(Theme.FONT_FAMILY, 9), text_color="gray")
            edited_label.pack(side="left", padx=2)
        
        content = ctk.CTkLabel(post_frame, text=post.content,
                              font=(Theme.FONT_FAMILY, 14), wraplength=900, anchor="w")
        content.pack(anchor="w", padx=10, pady=10, fill="x")
        
        action_frame = ctk.CTkFrame(post_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=10)
        
        is_liked = self.user.user_id in post.liked_by
        like_text = "❤️ Unlike" if is_liked else "🤍 Like"
        like_color = Theme.DANGER if is_liked else Theme.PRIMARY
        
        like_btn = ctk.CTkButton(action_frame, text=like_text, width=100, height=30,
                                fg_color=like_color,
                                command=lambda: self.toggle_like(post))
        like_btn.pack(side="left", padx=5)
        
        comment_btn = ctk.CTkButton(action_frame, text="💬 Comment", width=100, height=30,
                                   command=lambda: self.show_comment_dialog(post))
        comment_btn.pack(side="left", padx=5)
        
        likes_label = ctk.CTkLabel(action_frame, text=f"{post.likes} likes",
                                  font=(Theme.FONT_FAMILY, 12))
        likes_label.pack(side="left", padx=15)
        
        comments_label = ctk.CTkLabel(action_frame, text=f"{len(post.comments)} comments",
                                     font=(Theme.FONT_FAMILY, 12))
        comments_label.pack(side="left", padx=5)
        
        if post.comments:
            view_comments_btn = ctk.CTkButton(action_frame, text="View Comments", 
                                             width=120, height=30,
                                             command=lambda: self.show_comments(post))
            view_comments_btn.pack(side="right", padx=5)
    
    def toggle_like(self, post):
        if self.user.user_id in post.liked_by:
            self.post_service.unlike_post(post.post_id, self.user.user_id)
            self.history_service.add_action("unlike", {
                "post_id": post.post_id,
                "user_id": self.user.user_id
            })
        else:
            self.post_service.like_post(post.post_id, self.user.user_id)
            self.history_service.add_action("like", {
                "post_id": post.post_id,
                "user_id": self.user.user_id
            })
        
        self.load_feed()
    
    def show_comment_dialog(self, post):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Add Comment")
        dialog.geometry("500x250")
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text="Write your comment:",
                            font=(Theme.FONT_FAMILY, 16))
        label.pack(pady=20)
        
        textbox = ctk.CTkTextbox(dialog, height=100)
        textbox.pack(fill="both", padx=20, pady=10)
        
        def post_comment():
            comment = textbox.get("1.0", "end").strip()
            if comment:
                self.post_service.add_comment(post.post_id, self.user.user_id, comment)
                self.load_feed()
                dialog.destroy()
        
        post_btn = ctk.CTkButton(dialog, text="Post Comment", width=150,
                                command=post_comment)
        post_btn.pack(pady=10)
    
    def show_comments(self, post):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Comments")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text=f"Comments ({len(post.comments)})",
                            font=(Theme.FONT_FAMILY, 20, "bold"))
        title.pack(pady=20)
        
        comments_frame = ctk.CTkScrollableFrame(dialog)
        comments_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        for comment in post.comments:
            comment_widget = ctk.CTkFrame(comments_frame)
            comment_widget.pack(fill="x", pady=5, padx=10)
            
            author = self.user_service.get_user_by_id(comment['user_id'])
            author_name = author.username if author else "Unknown"
            
            author_label = ctk.CTkLabel(comment_widget, text=f"@{author_name}",
                                       font=(Theme.FONT_FAMILY, 12, "bold"))
            author_label.pack(anchor="w", padx=10, pady=5)
            
            comment_text = ctk.CTkLabel(comment_widget, text=comment['comment'],
                                       font=(Theme.FONT_FAMILY, 12), wraplength=500)
            comment_text.pack(anchor="w", padx=10, pady=5)
            
            date_str = datetime.datetime.fromtimestamp(comment['created_at']).strftime("%b %d, %I:%M %p")
            date_label = ctk.CTkLabel(comment_widget, text=date_str,
                                     font=(Theme.FONT_FAMILY, 9), text_color="gray")
            date_label.pack(anchor="w", padx=10, pady=2)
    
    def search_posts(self):
        self.search_query = self.search_entry.get().strip()
        self.load_feed()
    
    def apply_filter(self, filter_type):
        self.current_filter = filter_type
        self.search_query = ""
        self.search_entry.delete(0, "end")
        self.load_feed()
    
    def undo_action(self):
        action = self.history_service.undo_last_action()
        if action:
            if action['type'] == "like":
                self.post_service.unlike_post(action['data']['post_id'], 
                                             action['data']['user_id'])
            elif action['type'] == "unlike":
                self.post_service.like_post(action['data']['post_id'], 
                                           action['data']['user_id'])
            self.load_feed()