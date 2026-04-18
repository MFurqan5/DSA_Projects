import customtkinter as ctk
from ui.theme import Theme
import datetime

class ProfileUI:
    def __init__(self, parent, user_service, post_service):
        self.parent = parent
        self.user_service = user_service
        self.post_service = post_service
        self.user = user_service.current_user
        
        self.setup_ui()
    
    def setup_ui(self):
        scrollable_frame = ctk.CTkScrollableFrame(self.parent)
        scrollable_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        header = ctk.CTkFrame(scrollable_frame)
        header.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(header, text="My Profile", 
                            font=(Theme.FONT_FAMILY, 28, "bold"))
        title.pack(pady=10)
        
        info_frame = ctk.CTkFrame(scrollable_frame)
        info_frame.pack(fill="x", pady=20, padx=20)
        
        username_label = ctk.CTkLabel(info_frame, text=f"Username: {self.user.username}",
                                     font=(Theme.FONT_FAMILY, 16))
        username_label.pack(pady=5, anchor="w", padx=20)
        
        email_label = ctk.CTkLabel(info_frame, text=f"Email: {self.user.email}",
                                   font=(Theme.FONT_FAMILY, 14))
        email_label.pack(pady=5, anchor="w", padx=20)
        
        bio_label = ctk.CTkLabel(info_frame, text=f"Bio: {self.user.bio or 'No bio yet'}",
                                font=(Theme.FONT_FAMILY, 14))
        bio_label.pack(pady=5, anchor="w", padx=20)
        
        created_date = datetime.datetime.fromtimestamp(self.user.created_at).strftime("%B %d, %Y")
        joined_label = ctk.CTkLabel(info_frame, text=f"Joined: {created_date}",
                                   font=(Theme.FONT_FAMILY, 12), text_color="gray")
        joined_label.pack(pady=5, anchor="w", padx=20)
        
        edit_btn = ctk.CTkButton(info_frame, text="Edit Profile", width=150, height=35,
                                command=self.show_edit_dialog)
        edit_btn.pack(pady=15)
        
        posts_header = ctk.CTkLabel(scrollable_frame, text="My Posts",
                                   font=(Theme.FONT_FAMILY, 24, "bold"))
        posts_header.pack(pady=20)
        
        create_post_frame = ctk.CTkFrame(scrollable_frame)
        create_post_frame.pack(fill="x", pady=10, padx=20)
        
        post_label = ctk.CTkLabel(create_post_frame, text="Create New Post:")
        post_label.pack(pady=5, anchor="w", padx=10)
        
        post_textbox = ctk.CTkTextbox(create_post_frame, height=100)
        post_textbox.pack(fill="x", padx=10, pady=5)
        
        def create_post():
            content = post_textbox.get("1.0", "end").strip()
            if content:
                self.post_service.create_post(self.user.user_id, content)
                post_textbox.delete("1.0", "end")
                self.refresh_posts(scrollable_frame)
            else:
                error_label.configure(text="Post cannot be empty!")
        
        post_btn = ctk.CTkButton(create_post_frame, text="Post", width=120, height=35,
                                command=create_post)
        post_btn.pack(pady=10)
        
        error_label = ctk.CTkLabel(create_post_frame, text="", text_color="red")
        error_label.pack()
        
        self.posts_container = ctk.CTkFrame(scrollable_frame)
        self.posts_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.refresh_posts(scrollable_frame)
    
    def refresh_posts(self, parent):
        for widget in self.posts_container.winfo_children():
            widget.destroy()
        
        user_posts = self.post_service.get_user_posts(self.user.user_id)
        user_posts.sort(key=lambda x: x.created_at, reverse=True)
        
        if not user_posts:
            no_posts = ctk.CTkLabel(self.posts_container, text="No posts yet",
                                   font=(Theme.FONT_FAMILY, 14), text_color="gray")
            no_posts.pack(pady=20)
        else:
            for post in user_posts:
                self.create_post_widget(post)
    
    def create_post_widget(self, post):
        post_frame = ctk.CTkFrame(self.posts_container)
        post_frame.pack(fill="x", pady=10, padx=10)
        
        date_str = datetime.datetime.fromtimestamp(post.created_at).strftime("%b %d, %Y %I:%M %p")
        header = ctk.CTkLabel(post_frame, text=date_str, 
                             font=(Theme.FONT_FAMILY, 10), text_color="gray")
        header.pack(anchor="w", padx=10, pady=5)
        
        content = ctk.CTkLabel(post_frame, text=post.content, 
                              font=(Theme.FONT_FAMILY, 14), wraplength=700, anchor="w")
        content.pack(anchor="w", padx=10, pady=10, fill="x")
        
        stats_frame = ctk.CTkFrame(post_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        likes_label = ctk.CTkLabel(stats_frame, text=f"❤️ {post.likes} likes",
                                  font=(Theme.FONT_FAMILY, 12))
        likes_label.pack(side="left", padx=5)
        
        comments_label = ctk.CTkLabel(stats_frame, text=f"💬 {len(post.comments)} comments",
                                     font=(Theme.FONT_FAMILY, 12))
        comments_label.pack(side="left", padx=5)
        
        button_frame = ctk.CTkFrame(post_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)
        
        edit_btn = ctk.CTkButton(button_frame, text="Edit", width=80, height=30,
                                command=lambda: self.edit_post(post))
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(button_frame, text="Delete", width=80, height=30,
                                  fg_color=Theme.DANGER,
                                  command=lambda: self.delete_post(post))
        delete_btn.pack(side="left", padx=5)
    
    def edit_post(self, post):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Edit Post")
        dialog.geometry("500x300")
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text="Edit Post Content:", 
                            font=(Theme.FONT_FAMILY, 16))
        label.pack(pady=20)
        
        textbox = ctk.CTkTextbox(dialog, height=150)
        textbox.pack(fill="both", padx=20, pady=10)
        textbox.insert("1.0", post.content)
        
        def save():
            new_content = textbox.get("1.0", "end").strip()
            if new_content:
                self.post_service.update_post(post.post_id, new_content)
                self.refresh_posts(self.parent)
                dialog.destroy()
        
        save_btn = ctk.CTkButton(dialog, text="Save", width=120, command=save)
        save_btn.pack(pady=10)
    
    def delete_post(self, post):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Confirm Delete")
        dialog.geometry("400x200")
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text="Are you sure you want to delete this post?",
                            font=(Theme.FONT_FAMILY, 14))
        label.pack(pady=30)
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def confirm():
            self.post_service.delete_post(post.post_id)
            self.refresh_posts(self.parent)
            dialog.destroy()
        
        yes_btn = ctk.CTkButton(button_frame, text="Yes", width=100, 
                               fg_color=Theme.DANGER, command=confirm)
        yes_btn.pack(side="left", padx=10)
        
        no_btn = ctk.CTkButton(button_frame, text="No", width=100,
                              command=dialog.destroy)
        no_btn.pack(side="left", padx=10)
    
    def show_edit_dialog(self):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Edit Profile")
        dialog.geometry("500x400")
        dialog.grab_set()
        
        title = ctk.CTkLabel(dialog, text="Edit Profile", 
                            font=(Theme.FONT_FAMILY, 20, "bold"))
        title.pack(pady=20)
        
        username_label = ctk.CTkLabel(dialog, text="Username:")
        username_label.pack(pady=5)
        
        username_entry = ctk.CTkEntry(dialog, width=300)
        username_entry.insert(0, self.user.username)
        username_entry.pack(pady=5)
        
        email_label = ctk.CTkLabel(dialog, text="Email:")
        email_label.pack(pady=5)
        
        email_entry = ctk.CTkEntry(dialog, width=300)
        email_entry.insert(0, self.user.email)
        email_entry.pack(pady=5)
        
        bio_label = ctk.CTkLabel(dialog, text="Bio:")
        bio_label.pack(pady=5)
        
        bio_textbox = ctk.CTkTextbox(dialog, width=300, height=100)
        bio_textbox.insert("1.0", self.user.bio)
        bio_textbox.pack(pady=5)
        
        def save():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            bio = bio_textbox.get("1.0", "end").strip()
            
            if username and email:
                self.user_service.update_user(self.user.user_id, username, email, bio)
                self.user = self.user_service.current_user
                dialog.destroy()
                self.setup_ui()
        
        save_btn = ctk.CTkButton(dialog, text="Save Changes", width=150, command=save)
        save_btn.pack(pady=20)