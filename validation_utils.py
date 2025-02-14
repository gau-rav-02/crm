import os
import mimetypes
import tkinter as tk
from tkinter import messagebox

def validate_age(value):
    if value == "":
        return True
    if value.isdigit() and len(value) <= 2:
        if len(value) == 1 or (len(value) == 2 and 10 <= int(value) <= 99):
            return True
    return False

def validate_float(value):
    if value == "":
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_pdf(file_path):
    MAX_FILE_SIZE_MB = 5
    PDF_MIME_TYPE = 'application/pdf'

    if not file_path:
        return False

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

def register_validation(entry, validator):
    """
    Register validation for an entry widget
    :param entry: Tkinter Entry widget
    :param validator: Validation function
    """
    def validate_wrapper(value):
        return validator(value)
    
    vcmd = entry.register(validate_wrapper)
    entry.configure(validate="key", validatecommand=(vcmd, '%P'))