"""
Page for editing teacher details.
"""
import customtkinter as ctk
from tkinter import messagebox
from backend.database import update_teacher_by_id
from typing import Callable, Dict, Any
import tkinter as tk

class EditTeacherPage(ctk.CTkFrame):
    """UI for editing existing teacher details."""

    def __init__(self, master, teacher_data: Dict[str, Any], on_back: Callable = None):
        """
        Initialize the edit teacher page.

        Args:
            master: The parent widget.
            teacher_data: Dictionary containing the teacher's current data.
            on_back: Callback function to return to the previous page.
        """
        super().__init__(master)
        self.master = master # Keep master reference if needed elsewhere
        self.on_back = on_back
        self.teacher_data = teacher_data
        self.setup_ui()

    def arabic(self, text: str) -> str:
        # Assuming Arabic reshaping/bidi handling is done elsewhere or not needed here
        return text

    def setup_ui(self):
        """Set up the UI components for the edit teacher page."""
        # Clear existing widgets in the master frame is handled by the caller (search_student_page.py)

        # The frame is now 'self' because the class inherits from CTkFrame
        self.grid(row=0, column=0, sticky="nsew", padx=80, pady=40)
        # Assuming master is already configured to expand
        # self.master.grid_rowconfigure(0, weight=1)
        # self.master.grid_columnconfigure(0, weight=1)

        # Configure grid for the EditTeacherPage frame itself
        self.grid_rowconfigure(0, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        row = 0

        # Back button (arrow icon)
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

        # Page Title
        title_label = ctk.CTkLabel(
            self,
            text=self.arabic("تعديل بيانات المعلمة"),
            font=("Arial", 22, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 20))

        # Teacher Name
        ctk.CTkLabel(self, text=self.arabic(":اسم المعلمة"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=1, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.name_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.name_entry.insert(0, self.teacher_data.get("name", ""))
        self.name_entry.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        # National ID
        ctk.CTkLabel(self, text=self.arabic(":الرقم القومي"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=3, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.nid_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.nid_entry.insert(0, self.teacher_data.get("nid", ""))
        self.nid_entry.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        # Academic level and gender in one row
        ctk.CTkLabel(self, text=self.arabic(":الفصل الدراسي"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=5, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        ctk.CTkLabel(self, text=self.arabic(":الجنس"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=5, column=0, sticky="e", pady=(10, 2), padx=(0, 10))

        levels = [self.arabic(level) for level in ["التمهيدي", "الاول المستوى", "الثاني المستوى", "الصغار فصل", "يومي اشتراك"]]
        self.term_var = tk.StringVar(value=self.teacher_data.get("term", levels[0] if levels else ""))
        self.term_menu = ctk.CTkOptionMenu(self, values=levels, variable=self.term_var)
        self.term_menu.grid(row=6, column=1, sticky="ew", pady=5, padx=(0, 10))

        genders = [self.arabic("أنثى"), self.arabic("ذكر")] # Assuming female is primary for teachers
        self.gender_var = tk.StringVar(value=self.teacher_data.get("gender", genders[0] if genders else ""))
        self.gender_menu = ctk.CTkOptionMenu(self, values=genders, variable=self.gender_var)
        self.gender_menu.grid(row=6, column=0, sticky="ew", pady=5, padx=(0, 10))

        # Primary Phone
        ctk.CTkLabel(self, text=self.arabic(":هاتف المعلمة"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=7, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.phone1_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.phone1_entry.insert(0, self.teacher_data.get("phone1", ""))
        self.phone1_entry.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

        # Secondary Phone
        ctk.CTkLabel(self, text=self.arabic(":هاتف آخر*"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=9, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        self.phone2_entry = ctk.CTkEntry(self, width=300, justify="right", font=("Arial", 14))
        self.phone2_entry.insert(0, self.teacher_data.get("phone2", ""))
        self.phone2_entry.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew")

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

    def update_teacher(self):
        """Get data from form and update teacher in database."""
        teacher_id = self.teacher_data.get("id")
        name = self.name_entry.get().strip()
        nid = self.nid_entry.get().strip()
        term = self.term_var.get().strip()
        gender = self.gender_var.get().strip()
        phone1 = self.phone1_entry.get().strip()
        phone2 = self.phone2_entry.get().strip()

        if not all([name, nid, term, gender, phone1]) and not phone2:
             messagebox.showerror("خطأ", self.arabic("من فضلك املأ الحقول المطلوبة على الأقل (الاسم، الرقم القومي، الفصل، الجنس، هاتف المعلمة)"))
             return

        update_teacher_by_id(teacher_id, name, nid, term, gender, phone1, phone2)

        messagebox.showinfo("تم", self.arabic("تم تحديث بيانات المعلمة بنجاح"))

        # Go back to search page and refresh
        self.go_back()

    def go_back(self):
        """Clear the current frame and go back to the previous page (search page)."""
        # Clearing is handled by the caller before creating this page
        if self.on_back:
            self.on_back() 