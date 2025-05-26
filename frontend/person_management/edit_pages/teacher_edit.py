"""Teacher edit page implementation.

This module provides the user interface for editing existing teacher records,
including personal information, academic details, and contact details.
"""
import customtkinter as ctk
from tkinter import messagebox
from backend.database import update_teacher_by_id
from typing import Callable, Dict, Any
import tkinter as tk
from ..constants import ACADEMIC_LEVELS, GENDER_OPTIONS

class EditTeacherPage(ctk.CTkFrame):
    """UI for editing existing teacher details.
    
    This class provides a form interface for modifying teacher information,
    including personal details, academic level, and contact information.
    """

    def __init__(self, master, teacher_data: Dict[str, Any], on_back: Callable = None):
        """Initialize the edit teacher page.

        Args:
            master: The parent widget.
            teacher_data: Dictionary containing the teacher's current data.
            on_back: Callback function to return to the previous page.
        """
        super().__init__(master)
        self.master = master
        self.on_back = on_back
        self.teacher_data = teacher_data
        self.setup_ui()
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def arabic(self, text: str) -> str:
        """Handle Arabic text display.
        
        Args:
            text: The text to be displayed in Arabic.
            
        Returns:
            The processed Arabic text.
        """
        return text

    def setup_ui(self):
        """Set up the UI components for the edit teacher page.
        
        Creates and arranges all form elements including:
        - Back button
        - Page title
        - Teacher information fields
        - Save button
        """
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        # Match background color with parent window
        self.configure(fg_color=self.master.cget('fg_color'))

        # Add back button if callback provided
        if self.on_back:
            back_icon = ctk.CTkButton(
                self,
                text="←",
                font=("Arial", 18, "bold"),
                width=40,
                height=40,
                fg_color="#ff3333",
                text_color="#000000",
                hover_color="#b71c1c",
                corner_radius=20,
                command=self.go_back
            )
            back_icon.grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=(0, 10))

        # Page title
        title_label = ctk.CTkLabel(
            self,
            text=self.arabic("تعديل بيانات المعلمة"),
            font=("Arial", 22, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 20))

        # Teacher information sections
        self._setup_personal_info()
        self._setup_academic_info()
        self._setup_contact_info()

        # Save Button
        self.save_button = ctk.CTkButton(
            self,
            text=self.arabic("حفظ التعديلات"),
            font=("Arial", 18),
            height=40,
            width=200,
            command=self.update_teacher
        )
        self.save_button.grid(row=11, column=0, columnspan=2, pady=(20, 10), sticky="ew")

    def _setup_personal_info(self):
        """Set up personal information fields (name and national ID)."""
        # Teacher Name
        ctk.CTkLabel(self, text=self.arabic(":اسم المعلمة"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=1, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.name_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.name_entry.insert(0, self.teacher_data.get("name", ""))
        self.name_entry.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        # National ID
        ctk.CTkLabel(self, text=self.arabic(":الرقم القومي"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=3, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.nid_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.nid_entry.insert(0, self.teacher_data.get("nid", ""))
        self.nid_entry.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

    def _setup_academic_info(self):
        """Set up academic information fields (level and gender)."""
        # Academic level and gender labels
        ctk.CTkLabel(self, text=self.arabic(":الفصل الدراسي"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=5, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        ctk.CTkLabel(self, text=self.arabic(":الجنس"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=5, column=0, sticky="e", pady=(10, 2), padx=(0, 10))

        # Academic level dropdown
        levels = [self.arabic(level) for level in ACADEMIC_LEVELS if level != "الجميع"]
        self.term_var = tk.StringVar(value=self.teacher_data.get("term", levels[0] if levels else ""))
        self.term_menu = ctk.CTkOptionMenu(self, values=levels, variable=self.term_var)
        self.term_menu.grid(row=6, column=1, sticky="ew", pady=5, padx=(0, 10))

        # Gender dropdown
        genders = [self.arabic(GENDER_OPTIONS["male"]), self.arabic(GENDER_OPTIONS["female"])]
        self.gender_var = tk.StringVar(value=self.teacher_data.get("gender", genders[0] if genders else ""))
        self.gender_menu = ctk.CTkOptionMenu(self, values=genders, variable=self.gender_var)
        self.gender_menu.grid(row=6, column=0, sticky="ew", pady=5, padx=(0, 10))

    def _setup_contact_info(self):
        """Set up contact information fields (phone numbers)."""
        # Primary phone
        ctk.CTkLabel(self, text=self.arabic(":هاتف"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=7, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.phone1_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.phone1_entry.insert(0, self.teacher_data.get("phone1", ""))
        self.phone1_entry.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

        # Secondary phone (optional)
        ctk.CTkLabel(self, text=self.arabic(":هاتف آخر"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=9, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.phone2_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.phone2_entry.insert(0, self.teacher_data.get("phone2", ""))
        self.phone2_entry.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew")

    def update_teacher(self):
        """Update teacher information in the database.
        
        Collects form data, validates required fields, and updates the teacher record.
        Shows success/error messages and returns to previous page on success.
        """
        # Get teacher ID
        teacher_id = self.teacher_data.get("id")
        
        # Collect form data
        name = self.name_entry.get().strip()
        nid = self.nid_entry.get().strip()
        term = self.term_var.get().strip()
        gender = self.gender_var.get().strip()
        phone1 = self.phone1_entry.get().strip()
        phone2 = self.phone2_entry.get().strip()

        # Validate required fields
        if not all([name, nid, term, gender, phone1]):
            messagebox.showerror(
                self.arabic("خطأ"), 
                self.arabic("من فضلك املأ الحقول المطلوبة على الأقل (الاسم، الرقم القومي، الفصل، الجنس، هاتف)")
            )
            return

        # Update teacher record by ID
        update_teacher_by_id(teacher_id, name, nid, term, gender, phone1, phone2)

        # Show success message
        messagebox.showinfo(self.arabic("تم"), self.arabic("تم تحديث بيانات المعلمة بنجاح"))

        # Return to previous page
        self.go_back()

    def go_back(self):
        """Return to the previous page.
        
        Clears the current frame and calls the back callback if provided.
        """
        if self.on_back:
            self.on_back() 