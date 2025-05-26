"""Student edit page implementation.

This module provides the user interface for editing existing student records,
including personal information, academic details, and fee management.
"""
import customtkinter as ctk
from tkinter import messagebox
from backend.database import update_student
from typing import Callable, Dict, Any
import tkinter as tk
from ..constants import ACADEMIC_LEVELS, GENDER_OPTIONS, FEE_TYPES
from ..utils import get_fee_dates

class EditStudentPage(ctk.CTkFrame):
    """UI for editing existing student details.
    
    This class provides a form interface for modifying student information,
    including personal details, academic level, and fee payments.
    """

    def __init__(self, master, student_data: Dict[str, Any], on_back: Callable = None):
        """Initialize the edit student page.

        Args:
            master: The parent widget.
            student_data: Dictionary containing the student's current data.
            on_back: Callback function to return to the previous page.
        """
        super().__init__(master)
        self.master = master
        self.on_back = on_back
        self.student_data = student_data
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
        """Set up the UI components for the edit student page.
        
        Creates and arranges all form elements including:
        - Back button
        - Page title
        - Student information fields
        - Fee management section
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
            text=self.arabic("تعديل بيانات الطالب"),
            font=("Arial", 22, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 20))

        # Student information section
        self._setup_personal_info()
        self._setup_academic_info()
        self._setup_contact_info()
        self._setup_fees_section()

        # Save button
        self.save_button = ctk.CTkButton(
            self,
            text=self.arabic("حفظ التعديلات"),
            font=("Arial", 18),
            height=40,
            width=200,
            command=self.update_student
        )
        self.save_button.grid(row=13+len(FEE_TYPES), column=0, columnspan=2, pady=(20, 10), sticky="ew")

    def _setup_personal_info(self):
        """Set up personal information fields (name and national ID)."""
        # Student Name
        ctk.CTkLabel(self, text=self.arabic(":اسم الطالب"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=1, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.name_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.name_entry.insert(0, self.student_data.get("name", ""))
        self.name_entry.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        # National ID
        ctk.CTkLabel(self, text=self.arabic(":الرقم القومي"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=3, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.nid_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.nid_entry.insert(0, self.student_data.get("nid", ""))
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
        self.term_var = tk.StringVar(value=self.student_data.get("term", levels[0] if levels else ""))
        self.term_menu = ctk.CTkOptionMenu(self, values=levels, variable=self.term_var)
        self.term_menu.grid(row=6, column=1, sticky="ew", pady=5, padx=(0, 10))

        # Gender dropdown
        genders = [self.arabic(GENDER_OPTIONS["male"]), self.arabic(GENDER_OPTIONS["female"])]
        self.gender_var = tk.StringVar(value=self.student_data.get("gender", genders[0] if genders else ""))
        self.gender_menu = ctk.CTkOptionMenu(self, values=genders, variable=self.gender_var)
        self.gender_menu.grid(row=6, column=0, sticky="ew", pady=5, padx=(0, 10))

    def _setup_contact_info(self):
        """Set up contact information fields (guardian phone numbers)."""
        # Primary guardian phone
        ctk.CTkLabel(self, text=self.arabic(":هاتف ولي الأمر"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=7, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.phone1_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.phone1_entry.insert(0, self.student_data.get("phone1", ""))
        self.phone1_entry.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

        # Secondary guardian phone (optional)
        ctk.CTkLabel(self, text=self.arabic(":هاتف ولي أمر آخر*"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=9, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.phone2_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.phone2_entry.insert(0, self.student_data.get("phone2", ""))
        self.phone2_entry.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew")

    def _setup_fees_section(self):
        """Set up the fees management section with fee types and dates."""
        # Fees section title
        ctk.CTkLabel(self, text=self.arabic(":الرسوم"), 
                    font=("Arial", 16, "bold"), 
                    anchor="e", justify="right").grid(
                        row=11, column=1, sticky="e", pady=(10, 2), padx=(0, 10))

        # Initialize fee-related lists
        self.fee_entries = []
        self.fee_date_widgets = []
        
        # Get existing fee data
        fees = [self.student_data.get(f"fee{i+1}", "") for i in range(4)]
        fee_dates = [self.student_data.get(f"fee{i+1}_date", "") for i in range(4)]

        # Create fee table header
        fee_header = ctk.CTkFrame(self)
        fee_header.grid(row=12, column=0, columnspan=2, sticky="ew", pady=(0, 2))
        for idx in range(5):
            fee_header.grid_columnconfigure(idx, weight=1)

        # Add column headers
        headers = [self.arabic("يوم"), self.arabic("شهر"), self.arabic("سنة"), 
                  self.arabic("المبلغ"), self.arabic("اسم القسط")]
        for idx, txt in enumerate(headers):
            ctk.CTkLabel(fee_header, text=txt, 
                        font=("Arial", 13, "bold"), 
                        anchor="center", justify="center").grid(
                            row=0, column=idx, padx=4, pady=2, sticky="ew")

        # Create fee rows
        for i in range(4):
            fee_row_frame = ctk.CTkFrame(self)
            fee_row_frame.grid(row=13+i, column=0, columnspan=2, sticky="ew", pady=2)
            for idx in range(5):
                fee_row_frame.grid_columnconfigure(idx, weight=1)

            # Date input fields (day/month/year)
            day_entry = ctk.CTkEntry(fee_row_frame, width=35, justify="center")
            month_entry = ctk.CTkEntry(fee_row_frame, width=35, justify="center")
            year_entry = ctk.CTkEntry(fee_row_frame, width=50, justify="center")

            # Parse and populate existing date values
            if fee_dates[i]:
                try:
                    d, m, y = fee_dates[i].split("/")
                except ValueError:
                    d, m, y = "", "", ""
            else:
                d, m, y = "", "", ""

            day_entry.insert(0, d)
            month_entry.insert(0, m)
            year_entry.insert(0, y)

            # Place date entry fields
            day_entry.grid(row=0, column=0, padx=4, sticky="ew")
            month_entry.grid(row=0, column=1, padx=4, sticky="ew")
            year_entry.grid(row=0, column=2, padx=4, sticky="ew")

            self.fee_date_widgets.append((day_entry, month_entry, year_entry))

            # Fee amount entry
            entry = ctk.CTkEntry(fee_row_frame, width=80, justify="right", font=("Arial", 14))
            entry.insert(0, fees[i])
            self.fee_entries.append(entry)
            entry.grid(row=0, column=3, padx=4, sticky="ew")

            # Fee type label
            ctk.CTkLabel(
                fee_row_frame,
                text=self.arabic(FEE_TYPES[i]),
                font=("Arial", 13)
            ).grid(row=0, column=4, padx=2, sticky="ew")

    def update_student(self):
        """Update student information in the database.
        
        Collects form data, validates required fields, and updates the student record.
        Shows success/error messages and returns to previous page on success.
        """
        # Get original data for reference
        original_name = self.student_data.get("name", "")
        student_id = self.student_data.get("id")

        # Collect form data
        name = self.name_entry.get().strip()
        nid = self.nid_entry.get().strip()
        term = self.term_var.get().strip()
        gender = self.gender_var.get().strip()
        phone1 = self.phone1_entry.get().strip()
        phone2 = self.phone2_entry.get().strip()

        # Get fee data
        fees = [f.get().strip() for f in self.fee_entries]
        fee_dates = get_fee_dates(self.fee_date_widgets)

        # Validate required fields
        if not all([name, nid, term, gender, phone1]) and not phone2:
            messagebox.showerror(
                self.arabic("خطأ"), 
                self.arabic("من فضلك املأ الحقول المطلوبة على الأقل (الاسم، الرقم القومي، الفصل، الجنس، هاتف ولي الأمر)")
            )
            return

        # Update student record
        update_student(original_name, name, nid, term, gender, phone1, phone2, fees, fee_dates)

        # Show success message
        messagebox.showinfo(self.arabic("تم"), self.arabic("تم تحديث بيانات الطالب بنجاح"))

        # Return to previous page
        self.go_back()

    def go_back(self):
        """Return to the previous page.
        
        Clears the current frame and calls the back callback if provided.
        """
        if self.on_back:
            self.on_back() 