"""
Teacher registration form component.
"""
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from backend.database import add_teacher
from .constants import (
    ACADEMIC_LEVELS,
    GENDER_OPTIONS,
    BACK_BUTTON_STYLE,
    REGISTER_BUTTON_STYLE,
    LABEL_STYLE,
    ENTRY_STYLE,
    OPTION_MENU_STYLE
)
from .utils import validate_required_fields, clear_entry

class TeacherRegistrationForm:
    """Form for registering new teachers."""
    
    def __init__(self, master, on_back=None):
        """
        Initialize the teacher registration form.
        
        Args:
            master: Parent window
            on_back: Callback for back button
        """
        self.master = master
        self.on_back = on_back
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the form UI components."""
        # Clear existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()
            
        # Main frame
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=80, pady=40)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        for i in range(2):
            self.frame.grid_columnconfigure(i, weight=1)
            
        row = 0
        
        # Back button
        if self.on_back:
            back_icon = ctk.CTkButton(
                self.frame,
                command=self.go_back,
                **BACK_BUTTON_STYLE
            )
            back_icon.grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=(0, 10))
            
        # Teacher name
        ctk.CTkLabel(
            self.frame,
            text=":اسم المعلمة",
            **LABEL_STYLE
        ).grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        
        self.name_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="أدخل الاسم",
            **ENTRY_STYLE
        )
        self.name_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1
        
        # National ID
        ctk.CTkLabel(
            self.frame,
            text=":الرقم القومي",
            **LABEL_STYLE
        ).grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        
        self.nid_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="أدخل الرقم القومي",
            **ENTRY_STYLE
        )
        self.nid_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1
        
        # Academic level and gender
        ctk.CTkLabel(
            self.frame,
            text=":الفصل الدراسي",
            **LABEL_STYLE
        ).grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        
        ctk.CTkLabel(
            self.frame,
            text=":الجنس",
            **LABEL_STYLE
        ).grid(row=row, column=0, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        
        self.term_var = tk.StringVar(value=ACADEMIC_LEVELS[0])
        self.term_menu = ctk.CTkOptionMenu(
            self.frame,
            values=ACADEMIC_LEVELS,
            variable=self.term_var,
            **OPTION_MENU_STYLE
        )
        self.term_menu.grid(row=row, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        self.gender_var = tk.StringVar(value=GENDER_OPTIONS["female"])
        self.gender_menu = ctk.CTkOptionMenu(
            self.frame,
            values=[GENDER_OPTIONS["female"], GENDER_OPTIONS["male"]],
            variable=self.gender_var,
            **OPTION_MENU_STYLE
        )
        self.gender_menu.grid(row=row, column=0, sticky="ew", pady=5, padx=(0, 10))
        row += 1
        
        # Primary phone
        ctk.CTkLabel(
            self.frame,
            text=":هاتف المعلمة",
            **LABEL_STYLE
        ).grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        
        self.phone1_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="أدخل رقم الهاتف",
            **ENTRY_STYLE
        )
        self.phone1_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1
        
        # Secondary phone
        ctk.CTkLabel(
            self.frame,
            text=":هاتف آخر*",
            **LABEL_STYLE
        ).grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        
        self.phone2_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="أدخل رقم هاتف آخر إن وجد*",
            **ENTRY_STYLE
        )
        self.phone2_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1
        
        # Register button
        self.register_button = ctk.CTkButton(
            self.frame,
            text="تسجيل",
            command=self.register_teacher,
            **REGISTER_BUTTON_STYLE
        )
        self.register_button.grid(row=row, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        
    def register_teacher(self):
        """Handle teacher registration."""
        name = self.name_entry.get().strip()
        nid = self.nid_entry.get().strip()
        term = self.term_var.get().strip()
        gender = self.gender_var.get().strip()
        phone1 = self.phone1_entry.get().strip()
        phone2 = self.phone2_entry.get().strip()
        
        if not validate_required_fields(name, nid, phone1, phone2):
            return
            
        add_teacher(name, nid, term, gender, phone1, phone2)
        messagebox.showinfo("نجاح", "تم تسجيل المعلمة بنجاح")
        
        # Clear form
        clear_entry(self.name_entry, "أدخل الاسم")
        clear_entry(self.nid_entry, "أدخل الرقم القومي")
        clear_entry(self.phone1_entry, "أدخل رقم الهاتف")
        clear_entry(self.phone2_entry, "أدخل رقم هاتف آخر إن وجد*")
        
    def go_back(self):
        """Handle back button click."""
        for widget in self.master.winfo_children():
            widget.destroy()
        self.on_back() 