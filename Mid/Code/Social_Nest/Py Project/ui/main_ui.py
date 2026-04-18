# ui/main_ui.py
import customtkinter as ctk
from ui.theme import Theme
from ui.profile_ui import ProfileUI
from ui.feed_ui import FeedUI
from ui.friends_ui import FriendsUI

class MainUI:
    def __init__(self, user_service, post_service, feed_service, friend_service, history_service):
        self.user_service = user_service
        self.post_service = post_service
        self.feed_service = feed_service
        self.friend_service = friend_service
        self.history_service = history_service
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("Welcome to Social Nest")
        self.root.geometry("1200x700")
        
        self.current_view = None
        
        self.setup_ui()
    
    def setup_ui(self):
        if self.user_service.current_user:
            self.show_main_interface()
        else:
            self.show_login_screen()
    
    def show_login_screen(self):
        self.clear_window()
        
        login_frame = ctk.CTkFrame(self.root)
        login_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        title = ctk.CTkLabel(login_frame, text="Social Nest", 
                            font=(Theme.FONT_FAMILY, 32, "bold"))
        title.pack(pady=30)
        
        subtitle = ctk.CTkLabel(login_frame, text="Login or Create Account", 
                               font=(Theme.FONT_FAMILY, 16))
        subtitle.pack(pady=10)
        
        username_label = ctk.CTkLabel(login_frame, text="Username:")
        username_label.pack(pady=5)
        
        username_entry = ctk.CTkEntry(login_frame, width=300, height=40)
        username_entry.pack(pady=5)
        
        # ← ADDED PASSWORD
        password_label = ctk.CTkLabel(login_frame, text="Password:")
        password_label.pack(pady=5)
        password_entry = ctk.CTkEntry(login_frame, width=300, height=40, show="*")
        password_entry.pack(pady=5)
        
        # ← ADDED NAME
        name_label = ctk.CTkLabel(login_frame, text="Full Name (optional):")
        name_label.pack(pady=5)
        name_entry = ctk.CTkEntry(login_frame, width=300, height=40)
        name_entry.pack(pady=5)
        
        email_label = ctk.CTkLabel(login_frame, text="Email (for registration):")
        email_label.pack(pady=5)
        
        email_entry = ctk.CTkEntry(login_frame, width=300, height=40)
        email_entry.pack(pady=5)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get()
            if username:
                user = self.user_service.login(username, password)  # ← now with password
                if user:
                    self.show_main_interface()
                else:
                    error_label.configure(text="Wrong username or password!")
            else:
                error_label.configure(text="Please enter username!")
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            email = email_entry.get().strip()
            name = name_entry.get().strip()
            if username and email:
                user = self.user_service.create_user(username, email, password, name)  # ← pass password + name
                if user:
                    self.user_service.login(username, password)
                    self.show_main_interface()
                else:
                    error_label.configure(text="Username already exists!")
            else:
                error_label.configure(text="Please enter username and email!")
        
        button_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        login_btn = ctk.CTkButton(button_frame, text="Login", width=140, height=40, 
                                 command=login)
        login_btn.pack(side="left", padx=10)
        
        register_btn = ctk.CTkButton(button_frame, text="Register", width=140, height=40,
                                    command=register)
        register_btn.pack(side="left", padx=10)
        
        error_label = ctk.CTkLabel(login_frame, text="", text_color="red")
        error_label.pack(pady=10)
    
    # ← Everything below is 100% your original code — no change
    def show_main_interface(self):
        self.clear_window()
        
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(expand=True, fill="both")
        
        sidebar = ctk.CTkFrame(main_container, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(side="right", expand=True, fill="both")
        
        user_label = ctk.CTkLabel(sidebar, 
                                 text=f"@{self.user_service.current_user.username}",
                                 font=(Theme.FONT_FAMILY, 16, "bold"))
        user_label.pack(pady=20)
        
        def show_feed():
            self.clear_content(content_frame)
            FeedUI(content_frame, self.user_service, self.post_service, 
                  self.feed_service, self.friend_service, self.history_service)
        
        def show_profile():
            self.clear_content(content_frame)
            ProfileUI(content_frame, self.user_service, self.post_service)
        
        def show_friends():
            self.clear_content(content_frame)
            FriendsUI(content_frame, self.user_service, self.friend_service)
        
        def logout():
            self.user_service.logout()
            self.show_login_screen()
        
        feed_btn = ctk.CTkButton(sidebar, text="Feed", width=180, height=40,
                                command=show_feed)
        feed_btn.pack(pady=10, padx=10)
        
        profile_btn = ctk.CTkButton(sidebar, text="Profile", width=180, height=40,
                                   command=show_profile)
        profile_btn.pack(pady=10, padx=10)
        
        friends_btn = ctk.CTkButton(sidebar, text="Friends", width=180, height=40,
                                   command=show_friends)
        friends_btn.pack(pady=10, padx=10)
        
        logout_btn = ctk.CTkButton(sidebar, text="Logout", width=180, height=40,
                                  command=logout, fg_color=Theme.DANGER)
        logout_btn.pack(side="bottom", pady=20, padx=10)
        
        show_feed()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_content(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def run(self):
        self.root.mainloop()