import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import os
import mimetypes
import base64
from bson.objectid import ObjectId
from PIL import Image, ImageTk

from validation_utils import validate_age, validate_float, validate_pdf, register_validation

class AddUserSection:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.init_variables()
        self.create_ui()

    def init_variables(self):
        # Personal Information Variables
        self.first_name_var = tk.StringVar()
        self.middle_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Male")
        self.contact_no_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        # Education Variables
        self.ssc_var = tk.StringVar()
        self.education_type_var = tk.StringVar(value="HSC")
        self.hsc_diploma_var = tk.StringVar()
        self.diploma_stream_var = tk.StringVar()
        self.degree_type_var = tk.StringVar(value="B.Tech")
        self.degree_stream_var = tk.StringVar()
        self.degree_percent_var = tk.StringVar()
        self.current_year_var = tk.StringVar(value="1st Year")
        self.completion_year_var = tk.StringVar(value=str(datetime.now().year))
        self.degree_status_var = tk.StringVar(value="Pursuing")
        self.skills_var = tk.StringVar()
        self.resume_path_var = tk.StringVar()

        # Internship Variables
        self.role_var = tk.StringVar()
        self.duration_var = tk.StringVar(value="select")
        self.joining_date_var = tk.StringVar()
        self.ending_date_var = tk.StringVar()
        self.payment_type_var = tk.StringVar(value="Unpaid")
        self.stipend_amount_var = tk.StringVar()
        self.stipend_frequency_var = tk.StringVar(value="per month")

    def create_ui(self):
        main_container = tk.Frame(self.master, bg="#ffffff")
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Create a main frame to hold form and image
        # content_frame = tk.Frame(main_container, bg="#ffffff")
        # content_frame.pack(fill='both', expand=True)
        
        content_frame = tk.Canvas(main_container, bg="#ffffff", highlightthickness=0)
        content_frame.pack(fill='both', expand=True)
        
        def setup_background():
            content_frame.update()
            try:
                bg_image = Image.open("assets/bg.jpg")
                width = main_container.winfo_width()
                height = main_container.winfo_height()
                
                bg_image = bg_image.resize((width, height), Image.LANCZOS)
                self.bg_image_tk = ImageTk.PhotoImage(bg_image)
                content_frame.create_image(0, 0, image=self.bg_image_tk, anchor="nw")
            except Exception as e:
                print(f"Error: {e}")

        def update_background(event):
            setup_background()

        setup_background()
        content_frame.bind('<Configure>', update_background)

        # Add scrollbar on the far right
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        content_frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int(e.delta/120), "units"))

        # Create form frame on the left
        form_frame = tk.Frame(content_frame, bg="#ffffff")
        form_frame.pack(side='left', fill='both', expand=True, padx=(40, 0))  

        canvas = tk.Canvas(form_frame, bg="#ffffff", yscrollcommand=scrollbar.set, highlightthickness=0)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=canvas.yview)

        image_frame = tk.Frame(content_frame, bg="#ffffff", width=400)  
        image_frame.pack(side='right', fill='y', padx=(0, 40))  

        try:
            image_path = "assets/data.jpg"  
            original_image = Image.open(image_path)

            image_frame.update()
            image_width = int(image_frame.winfo_width() * 1.5)  
            resized_image = original_image.resize(
                (image_width, int(image_width * original_image.height / original_image.width)), Image.LANCZOS
            )

            photo = ImageTk.PhotoImage(resized_image)
            image_label = tk.Label(image_frame, image=photo, bg="#ffffff")
            image_label.image = photo  
            image_label.pack(fill='both', expand=True)
        except Exception as e:
            print(f"Error loading image: {e}")
            error_label = tk.Label(image_frame, text="Image Not Found", bg="#ffffff")
            error_label.pack(expand=True)

        title_label = tk.Label(scrollable_frame, text="Add Student Data", 
                            font=("Arial", 20, "bold"), bg="#ffffff")
        title_label.pack(pady=10)

        self.create_personal_section(scrollable_frame)
        self.create_education_section(scrollable_frame)
        self.create_internship_section(scrollable_frame)

        save_icon = Image.open("assets/save-btn-img.png").resize((100, 50))
        save_img = ImageTk.PhotoImage(save_icon)
        save_btn = tk.Button(scrollable_frame, command=self.save_user, image=save_img, bd=0, highlightthickness=0, borderwidth=0)
        save_btn.image = save_img
        save_btn.pack(pady=20)



    def create_personal_section(self, parent):
        tk.Label(parent, text="Personal Information", 
                 font=("Arial", 16), bg="#ffffff").pack(pady=10)

        fields = [
            ("First Name", self.first_name_var),
            ("Middle Name", self.middle_name_var),
            ("Last Name", self.last_name_var),
            ("Age", self.age_var),
            ("Contact Number", self.contact_no_var),
            ("Email", self.email_var),
            ("Address", self.address_var)
        ]

        for label_text, var in fields:
            frame = tk.Frame(parent, bg="#ffffff")
            frame.pack(fill='x', padx=50, pady=5)
            
            label = tk.Label(frame, text=label_text, width=15, anchor='w', bg="#ffffff")
            label.pack(side='left')
            
            entry = tk.Entry(frame, textvariable=var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK")
            entry.pack(side='left', expand=True, fill='x')

            if label_text == "Age":
                register_validation(entry, validate_age)

        # Gender Selection
        gender_frame = tk.Frame(parent, bg="#ffffff")
        gender_frame.pack(pady=10)
        
        tk.Label(gender_frame, text="Gender", bg="#ffffff").pack(side='left', padx=10)
        
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, 
                       value="Male", bg="#ffffff").pack(side='left', padx=10)
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, 
                       value="Female", bg="#ffffff").pack(side='left')

    def create_education_section(self, parent):
        tk.Label(parent, text="Educational Information", 
             font=("Arial", 16), bg="#ffffff").pack(pady=10)

        def toggle_education_type(*args):
            education_type = self.education_type_var.get()
            
            if education_type == "HSC":
                hsc_percent_frame.pack(fill='x', padx=50, pady=5, after=education_type_frame)
                diploma_stream_frame.pack_forget()
                diploma_percent_frame.pack_forget()
                self.hsc_diploma_var.set("")
                self.diploma_stream_var.set("")
            else:  
                hsc_percent_frame.pack_forget()
                diploma_stream_frame.pack(fill='x', padx=50, pady=5, after=education_type_frame)
                diploma_percent_frame.pack(fill='x', padx=50, pady=5, after=diploma_stream_frame)
                self.hsc_diploma_var.set("")

        def toggle_degree_status(*args):
            degree_status = self.degree_status_var.get()
            
            if degree_status == "Pursuing":
                current_year_frame.pack(fill='x', padx=50, pady=5, after=degree_status_frame)
                completion_year_frame.pack_forget()
            else:  
                current_year_frame.pack_forget()
                completion_year_frame.pack(fill='x', padx=50, pady=5, after=degree_status_frame)

        ssc_frame = tk.Frame(parent, bg="#ffffff")
        ssc_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(ssc_frame, text="SSC Percentage", width=15, anchor='w', bg="#ffffff").pack(side='left')
        ssc_entry = tk.Entry(ssc_frame, textvariable=self.ssc_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK")
        ssc_entry.pack(side='left', expand=True, fill='x')
        register_validation(ssc_entry, validate_float)

        education_type_frame = tk.Frame(parent, bg="#ffffff")
        education_type_frame.pack(pady=10)
        
        tk.Label(education_type_frame, text="Education Type", bg="#ffffff").pack(side='left', padx=10)
        hsc_radio = tk.Radiobutton(education_type_frame, text="HSC", variable=self.education_type_var, 
                    value="HSC", bg="#ffffff", command=toggle_education_type)
        hsc_radio.pack(side='left', padx=10)
        
        diploma_radio = tk.Radiobutton(education_type_frame, text="Diploma", variable=self.education_type_var, 
                        value="Diploma", bg="#ffffff", command=toggle_education_type)
        diploma_radio.pack(side='left')

        hsc_percent_frame = tk.Frame(parent, bg="#ffffff")
        tk.Label(hsc_percent_frame, text="HSC Percentage", width=15, anchor='w', bg="#ffffff").pack(side='left')
        hsc_diploma_entry = tk.Entry(hsc_percent_frame, textvariable=self.hsc_diploma_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK")
        hsc_diploma_entry.pack(side='left', expand=True, fill='x')
        register_validation(hsc_diploma_entry, validate_float)

        diploma_stream_frame = tk.Frame(parent, bg="#ffffff")
        tk.Label(diploma_stream_frame, text="Diploma Stream", width=15, anchor='w', bg="#ffffff").pack(side='left')
        diploma_stream_entry = tk.Entry(diploma_stream_frame, textvariable=self.diploma_stream_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK")
        diploma_stream_entry.pack(side='left', expand=True, fill='x')

        diploma_percent_frame = tk.Frame(parent, bg="#ffffff")
        tk.Label(diploma_percent_frame, text="Diploma Percentage", width=15, anchor='w', bg="#ffffff").pack(side='left')
        diploma_percent_entry = tk.Entry(diploma_percent_frame, textvariable=self.hsc_diploma_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK")
        diploma_percent_entry.pack(side='left', expand=True, fill='x')
        register_validation(diploma_percent_entry, validate_float)

        tk.Label(parent, text="Degree Details", 
                font=("Arial", 14), bg="#ffffff").pack(pady=10)

        degree_status_frame = tk.Frame(parent, bg="#ffffff")
        degree_status_frame.pack(pady=10)
        
        tk.Label(degree_status_frame, text="Degree Status", bg="#ffffff").pack(side='left', padx=10)
        pursuing_radio = tk.Radiobutton(degree_status_frame, text="Pursuing", 
                        variable=self.degree_status_var, 
                        value="Pursuing", bg="#ffffff", command=toggle_degree_status)
        pursuing_radio.pack(side='left', padx=10)
        
        completed_radio = tk.Radiobutton(degree_status_frame, text="Completed", 
                        variable=self.degree_status_var, 
                        value="Completed", bg="#ffffff", command=toggle_degree_status)
        completed_radio.pack(side='left')

        degree_type_frame = tk.Frame(parent, bg="#ffffff")
        degree_type_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(degree_type_frame, text="Degree Type", width=15, anchor='w', bg="#ffffff").pack(side='left')
        combobox_frame = tk.Frame(degree_type_frame, highlightthickness=1, highlightbackground="BLACK")
        combobox_frame.pack(side='left', expand=True, fill='x', padx=5)  
        degree_types = ["B.Tech", "B.E", "B.Com", "BCA", "B.Sc", "B.A"]
        degree_type_dropdown = ttk.Combobox(
            combobox_frame,
            textvariable=self.degree_type_var,
            values=degree_types,
            width=37
        )
        degree_type_dropdown.pack(fill='x')

        current_year_frame = tk.Frame(parent, bg="#ffffff")
        current_years = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        tk.Label(current_year_frame, text="Current Year", width=15, anchor='w', bg="#ffffff").pack(side='left')
        combobox_frame = tk.Frame(current_year_frame, highlightthickness=1, highlightbackground="BLACK")
        combobox_frame.pack(side='left', expand=True, fill='x', padx=5)  
        current_year_dropdown = ttk.Combobox(
            combobox_frame, 
            textvariable=self.current_year_var, 
            values=current_years, 
            width=37
        )
        current_year_dropdown.pack(fill='x')
        current_year_dropdown.current(0)

        completion_year_frame = tk.Frame(parent, bg="#ffffff")
        completion_years = [str(year) for year in range(2025, datetime.now().year-10, -1)]
        tk.Label(completion_year_frame, text="Completion Year", width=15, anchor='w', bg="#ffffff").pack(side='left')
        combobox_frame = tk.Frame(completion_year_frame, highlightthickness=1, highlightbackground="BLACK")
        combobox_frame.pack(side='left', expand=True, fill='x', padx=5) 
        completion_year_dropdown = ttk.Combobox(
            combobox_frame, 
            textvariable=self.completion_year_var, 
            values=completion_years, 
            width=37
        )
        completion_year_dropdown.pack(fill='x')
        completion_year_dropdown.current(0)

        degree_stream_frame = tk.Frame(parent, bg="#ffffff")
        degree_stream_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(degree_stream_frame, text="Degree Stream", width=15, anchor='w', bg="#ffffff").pack(side='left')
        tk.Entry(degree_stream_frame, textvariable=self.degree_stream_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK").pack(side='left', expand=True, fill='x')

        degree_percent_frame = tk.Frame(parent, bg="#ffffff")
        degree_percent_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(degree_percent_frame, text="Degree Percentage", width=15, anchor='w', bg="#ffffff").pack(side='left')
        degree_percent_entry = tk.Entry(degree_percent_frame, textvariable=self.degree_percent_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK")
        degree_percent_entry.pack(side='left', expand=True, fill='x')
        register_validation(degree_percent_entry, validate_float)
        
        skills_frame = tk.Frame(parent, bg="#ffffff")
        skills_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(skills_frame, text="Skills", width=15, anchor='w', bg="#ffffff").pack(side='left')
        tk.Entry(skills_frame, textvariable=self.skills_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK").pack(side='left', expand=True, fill='x')


        resume_frame = tk.Frame(parent, bg="#ffffff")
        resume_frame.pack(fill='x', padx=50, pady=10)
        tk.Label(resume_frame, text="Resume Upload", width=15, anchor='w', bg="#ffffff").pack(side='left')
        resume_icon = Image.open("assets/resume-btn-img.png").resize((90, 40))
        resume_img = ImageTk.PhotoImage(resume_icon)
        resume_btn = tk.Button(resume_frame, image=resume_img, bd=0, highlightthickness=0, borderwidth=0, command=self.upload_resume)
        resume_btn.image = resume_img
        resume_btn.pack(side="left")
        # resume_btn = tk.Button(resume_frame, text="Upload PDF", command=self.upload_resume, bg="#536270", fg="white", bd=0)
        # resume_btn.pack(side='left')
        tk.Label(resume_frame, textvariable=self.resume_path_var, bg="#ffffff").pack(side='left', padx=10)

        self.education_type_var.set("HSC")
        self.degree_status_var.set("Pursuing")
        toggle_education_type()
        toggle_degree_status()

    def upload_resume(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path and self.validate_pdf(file_path):
            self.resume_path_var.set(file_path)

    def validate_pdf(self, file_path):
        MAX_FILE_SIZE_MB = 5
        PDF_MIME_TYPE = 'application/pdf'

        if not file_path.lower().endswith('.pdf'):
            messagebox.showerror("Error", "Please select a PDF file.")
            return False

        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size > MAX_FILE_SIZE_MB:
            messagebox.showerror("Error", "Resume file must be under 5MB.")
            return False

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type != PDF_MIME_TYPE:
            messagebox.showerror("Error", "Selected file is not a valid PDF.")
            return False

        return True

    def create_internship_section(self, parent):
        tk.Label(parent, text="Internship Details", 
             font=("Arial", 16), bg="#ffffff").pack(pady=10)

        def toggle_payment_type():
            payment_type = self.payment_type_var.get()
            
            if payment_type == "Paid":
                stipend_amount_frame.pack(fill='x', padx=50, pady=5, after=payment_frame)
                stipend_frequency_frame.pack(fill='x', padx=50, pady=5, after=stipend_amount_frame)
                self.stipend_amount_var.set("")
            else:  # Unpaid
                stipend_amount_frame.pack_forget()
                stipend_frequency_frame.pack_forget()
                self.stipend_amount_var.set("")

        role_frame = tk.Frame(parent, bg="#ffffff")
        role_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(role_frame, text="Role", width=15, anchor='w', bg="#ffffff").pack(side='left')
        role_dropdown = tk.Entry(role_frame, textvariable=self.role_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK")
        role_dropdown.pack(side='left', expand=True, fill='x')

        duration_frame = tk.Frame(parent, bg="#ffffff")
        duration_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(duration_frame, text="Duration", width=15, anchor='w', bg="#ffffff").pack(side='left')
        combobox_frame = tk.Frame(duration_frame, highlightthickness=1, highlightbackground="BLACK")
        combobox_frame.pack(side='left', expand=True, fill='x', padx=5)  
        durations = ["select", "3 months", "4 months", "5 months", "6 months"]
        duration_dropdown = ttk.Combobox(combobox_frame, textvariable=self.duration_var, values=durations, width=37)
        duration_dropdown.pack(fill='x')

        joining_frame = tk.Frame(parent, bg="#ffffff")
        joining_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(joining_frame, text="Joining Date", width=15, anchor='w', bg="#ffffff").pack(side='left')
        date_frame = tk.Frame(joining_frame, highlightthickness=1, highlightbackground="BLACK")
        date_frame.pack(side='left', expand=True, fill='x', padx=5)  
        joining_date_calendar = DateEntry(
            date_frame, 
            textvariable=self.joining_date_var, 
            date_pattern='yyyy-mm-dd', 
            width=37
        )
        joining_date_calendar.pack(fill='x')

        ending_frame = tk.Frame(parent, bg="#ffffff")
        ending_frame.pack(fill='x', padx=50, pady=5)
        tk.Label(ending_frame, text="Ending Date", width=15, anchor='w', bg="#ffffff").pack(side='left')
        date_frame = tk.Frame(ending_frame, highlightthickness=1, highlightbackground="BLACK")
        date_frame.pack(side='left', expand=True, fill='x', padx=5)  
        ending_date_calendar = DateEntry(
            date_frame, 
            textvariable=self.ending_date_var, 
            date_pattern='yyyy-mm-dd', 
            width=37
        )
        ending_date_calendar.pack(fill='x')

        payment_frame = tk.Frame(parent, bg="#ffffff")
        payment_frame.pack(pady=10)
        tk.Label(payment_frame, text="Payment Type", bg="#ffffff").pack(side='left', padx=10)
        
        paid_radio = tk.Radiobutton(payment_frame, text="Paid", 
                    variable=self.payment_type_var, 
                    value="Paid", bg="#ffffff", command=toggle_payment_type)
        paid_radio.pack(side='left', padx=10)
        
        unpaid_radio = tk.Radiobutton(payment_frame, text="Unpaid", 
                        variable=self.payment_type_var, 
                        value="Unpaid", bg="#ffffff", command=toggle_payment_type)
        unpaid_radio.pack(side='left')

        stipend_amount_frame = tk.Frame(parent, bg="#ffffff")
        tk.Label(stipend_amount_frame, text="Stipend Amount", width=15, anchor='w', bg="#ffffff").pack(side='left')
        stipend_amount_entry = tk.Entry(stipend_amount_frame, textvariable=self.stipend_amount_var, width=40, highlightthickness=1, highlightbackground="BLACK", highlightcolor="BLACK")
        stipend_amount_entry.pack(side='left', expand=True, fill='x')

        stipend_frequency_frame = tk.Frame(parent, bg="#ffffff")
        tk.Label(stipend_frequency_frame, text="Stipend Frequency", width=15, anchor='w', bg="#ffffff").pack(side='left')
        combobox_frame = tk.Frame(stipend_frequency_frame, highlightthickness=1, highlightbackground="BLACK")
        combobox_frame.pack(side='left', expand=True, fill='x', padx=5)  
        frequencies = ["per month", "one-time", "per project"]
        stipend_frequency_dropdown = ttk.Combobox(
            combobox_frame, 
            textvariable=self.stipend_frequency_var, 
            values=frequencies, 
            width=37
        )
        stipend_frequency_dropdown.pack(fill='x')
        stipend_frequency_dropdown.current(0)

        self.payment_type_var.set("Unpaid")
        toggle_payment_type()

    def save_user(self):
        try:
            required_fields = {
                'First Name': self.first_name_var.get().strip(),
                'Last Name': self.last_name_var.get().strip(),
                'Age': self.age_var.get().strip(),
                'Contact Number': self.contact_no_var.get().strip(),
                'Email': self.email_var.get().strip(),
                'Address': self.address_var.get().strip(),
                'SSC Percentage': self.ssc_var.get().strip(),
                'Degree Stream': self.degree_stream_var.get().strip(),
                'Role': self.role_var.get(),
                'Duration': self.duration_var.get(),
                'Joining Date': self.joining_date_var.get(),
                'Ending Date': self.ending_date_var.get()
            }

            for field_name, value in required_fields.items():
                if not value or value == 'select':
                    messagebox.showerror("Validation Error", f"{field_name} is required!")
                    return

            user_data = {
                'first_name': self.first_name_var.get().strip(),
                'middle_name': self.middle_name_var.get().strip(),
                'last_name': self.last_name_var.get().strip(),
                'age': int(self.age_var.get()),
                'gender': self.gender_var.get(),
                'contact_no': self.contact_no_var.get().strip(),
                'email': self.email_var.get().strip(),
                'address': self.address_var.get().strip()
            }

            user_id = self.db.insert_user(user_data)

            resume_data = None
            if self.resume_path_var.get():
                with open(self.resume_path_var.get(), 'rb') as f:
                    resume_data = base64.b64encode(f.read()).decode('utf-8')
                    
            education_data = {
                'user_id': user_id,
                'ssc_percentage': float(self.ssc_var.get()),
                'education_type': self.education_type_var.get(),
                'hsc_diploma_percentage': float(self.hsc_diploma_var.get()) if self.hsc_diploma_var.get() else None,
                'diploma_stream': self.diploma_stream_var.get() if self.education_type_var.get() == "Diploma" else None,
                'degree_status': self.degree_status_var.get(),
                'degree_type': self.degree_type_var.get(),
                'degree_stream': self.degree_stream_var.get(),
                'degree_percentage': float(self.degree_percent_var.get()),
                'skills': self.skills_var.get().strip(),
                'current_year': self.current_year_var.get() if self.degree_status_var.get() == "Pursuing" else None,
                'completion_year': int(self.completion_year_var.get()) if self.degree_status_var.get() == "Completed" else None,
                'resume': resume_data,
            }

            education_id = self.db.insert_education(education_data)

            internship_data = {
                'user_id': user_id,
                'role': self.role_var.get(),
                'duration': self.duration_var.get(),
                'joining_date': datetime.strptime(self.joining_date_var.get(), '%Y-%m-%d'),
                'ending_date': datetime.strptime(self.ending_date_var.get(), '%Y-%m-%d'),
                'internship_type': self.payment_type_var.get(),
                'stipend_amount': float(self.stipend_amount_var.get()) if self.payment_type_var.get() == "Paid" and self.stipend_amount_var.get() else None,
                'stipend_frequency': self.stipend_frequency_var.get() if self.payment_type_var.get() == "Paid" else None
            }

            internship_id = self.db.insert_internship(internship_data)

            messagebox.showinfo("Success", "User data saved successfully!")
            
            self.clear_all_fields()

        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_all_fields(self):
        # Personal Information
        self.first_name_var.set("")
        self.middle_name_var.set("")
        self.last_name_var.set("")
        self.age_var.set("")
        self.gender_var.set("Male")
        self.contact_no_var.set("")
        self.email_var.set("")
        self.address_var.set("")

        # Education Information
        self.ssc_var.set("")
        self.education_type_var.set("HSC")
        self.hsc_diploma_var.set("")
        self.diploma_stream_var.set("")
        self.degree_stream_var.set("")
        self.degree_percent_var.set("")
        self.current_year_var.set("1st Year")
        self.completion_year_var.set(str(datetime.now().year))
        self.degree_status_var.set("Pursuing")
        self.skills_var.set("")
        self.resume_path_var.set("")

        # Internship Information
        self.role_var.set("select")
        self.duration_var.set("select")
        self.joining_date_var.set("")
        self.ending_date_var.set("")
        self.payment_type_var.set("Unpaid")
        self.stipend_amount_var.set("")
        self.stipend_frequency_var.set("per month")