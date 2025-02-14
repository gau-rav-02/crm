import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk  # Add this import
from tkcalendar import DateEntry
from datetime import datetime
from login_window import LoginWindow

from database_connection import DatabaseConnection
from add_user_section import AddUserSection
from show_user_details import ShowUserDetails

class NPTechCRMApp:
    def __init__(self):
        # Database Initialization
        self.db = DatabaseConnection()

        # Create root window but don't show it yet
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window

        # Show Login Window
        # LoginWindow(self.db, self.create_main_window)
        self.create_main_window()
    
    def create_main_window(self):
        # Show and configure main window
        self.root.deiconify()  # Show the main window
        self.root.title("NPTECH CRM Software")
        self.root.geometry("1200x800")
        self.root.configure(bg="#b5eeff")

        # Create UI Components
        self.create_menu_frame()
        self.create_content_frame()

        # Default to Add User Section
        self.show_add_user()

    def create_menu_frame(self):
        self.menu_frame = tk.Frame(self.root, width=200, bg="#BCCCDC")
        self.menu_frame.pack(side="left", fill="y")
        
        # Add logo
        try:
            # Load and resize the logo image
            logo_image = Image.open("assets/npl.png")  # Replace with your logo file path
            # Resize image to fit menu frame (adjust size as needed)
            logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Create label for logo
            logo_label = tk.Label(self.menu_frame, image=self.logo_photo, bg="#BCCCDC")
            logo_label.pack(pady=(20, 10))
        except Exception as e:
            print(f"Error loading logo: {e}")

        # menu_label = tk.Label(self.menu_frame, text="NPTECH CRM", 
        #                        font=("Arial", 16, "bold"), 
        #                        bg="#BCCCDC", fg="#000000")
        # menu_label.pack(pady=20)

        self.add_user_btn = tk.Button(self.menu_frame, text="Add Student Data", 
                                 command=self.show_add_user, 
                                #  bg="#BCCCDC", fg="white",
                                 font=("Arial", 12), width=20, pady=10)
        self.add_user_btn.pack(pady=10, padx=(20, 20))

        self.show_details_btn = tk.Button(self.menu_frame, text="Show Student Details", 
                                     command=self.show_user_details, 
                                    #  bg="#BCCCDC", fg="white", 
                                     font=("Arial", 12), width=20, pady=10)
        self.show_details_btn.pack(pady=10, padx=(20, 20))

    def create_content_frame(self):
        self.content_frame = tk.Frame(self.root, bg="#ffffff")
        self.content_frame.pack(side="right", fill="both", expand=True)
        
    def update_button_state(self, active_button):
        # Reset all button styles
        self.add_user_btn.config(bg="#BCCCDC", fg="black")
        self.show_details_btn.config(bg="#BCCCDC", fg="black")

        # Highlight the active button
        if active_button == "add_user":
            self.add_user_btn.config(bg="white", fg="#0b4bd1")
        elif active_button == "show_details":
            self.show_details_btn.config(bg="white", fg="#0b4bd1")

    def show_add_user(self):
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.update_button_state("add_user")

        # Create Add User Section
        AddUserSection(self.content_frame, self.db)

    def show_user_details(self):
        #Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.update_button_state("show_details")

        # Create Show User Details Section
        ShowUserDetails(self.content_frame, self.db)
        

def main():
    app = NPTechCRMApp()
    tk.mainloop()

if __name__ == "__main__":
    main()