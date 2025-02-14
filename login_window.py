import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, db, on_successful_login):
        self.db = db
        self.on_successful_login = on_successful_login
        
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("300x250")
        
        # Username
        tk.Label(self.root, text="Username").pack(pady=(20,5))
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()
        
        # Password
        tk.Label(self.root, text="Password").pack(pady=(10,5))
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack()
        
        # Login Button
        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)
        
        self.root.mainloop()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.db.authenticate_user(username, password):
            messagebox.showinfo("Success", "Login Successful")
            self.root.destroy()
            self.on_successful_login()
        else:
            messagebox.showerror("Error", "Invalid Credentials")