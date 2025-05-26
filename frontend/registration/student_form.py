"""
Student registration form component.
"""
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from backend.database import add_student
from .constants import (
    ACADEMIC_LEVELS,
    GENDER_OPTIONS,
    FEE_TYPES,
    BACK_BUTTON_STYLE,
    REGISTER_BUTTON_STYLE,
    LABEL_STYLE,
    ENTRY_STYLE,
    OPTION_MENU_STYLE
)
from .utils import (
    validate_required_fields,
    clear_entry,
    clear_fee_entries,
    get_fee_dates
)

class StudentRegistrationForm:
    """Form for registering new students."""
    
    def __init__(self, master, on_back=None):
        """
        Initialize the student registration form.
        
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
        # Set frame color to match the master window's background color
        self.frame = ctk.CTkFrame(self.master, fg_color=self.master.cget('fg_color'))
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
            
        # Student name
        ctk.CTkLabel(
            self.frame,
            text=":اسم الطالب",
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
        
        self.gender_var = tk.StringVar(value=GENDER_OPTIONS["male"])
        self.gender_menu = ctk.CTkOptionMenu(
            self.frame,
            values=[GENDER_OPTIONS["male"], GENDER_OPTIONS["female"]],
            variable=self.gender_var,
            **OPTION_MENU_STYLE
        )
        self.gender_menu.grid(row=row, column=0, sticky="ew", pady=5, padx=(0, 10))
        row += 1
        
        # Primary guardian phone
        ctk.CTkLabel(
            self.frame,
            text=":هاتف ولي الأمر",
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
        
        # Secondary guardian phone
        ctk.CTkLabel(
            self.frame,
            text=":هاتف ولي أمر آخر*",
            **LABEL_STYLE
        ).grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        
        self.phone2_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="أدخل رقم الهاتف اخر ان وجد*",
            **ENTRY_STYLE
        )
        self.phone2_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1
        
        # Fees section
        ctk.CTkLabel(
            self.frame,
            text=":الرسوم",
            **LABEL_STYLE
        ).grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        
        self.setup_fees_section(row)
        
    def setup_fees_section(self, start_row):
        """Set up the fees input section."""
        # Fee table header
        fee_header = ctk.CTkFrame(self.frame)
        fee_header.grid(row=start_row, column=0, columnspan=2, sticky="ew", pady=(0, 2))
        for idx in range(5):
            fee_header.grid_columnconfigure(idx, weight=1)
            
        headers = ["يوم", "شهر", "سنة", "المبلغ", "اسم القسط"]
        for idx, txt in enumerate(headers):
            ctk.CTkLabel(
                fee_header,
                text=txt,
                font=("Arial", 13, "bold"),
                anchor="center",
                justify="center"
            ).grid(row=0, column=idx, padx=4, pady=2, sticky="ew")
            
        # Fee entries
        self.fee_entries = []
        self.fee_date_widgets = []
        row = start_row + 1
        
        for i in range(4):
            fee_row_frame = ctk.CTkFrame(self.frame)
            fee_row_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=2)
            for idx in range(5):
                fee_row_frame.grid_columnconfigure(idx, weight=1)
                
            # Date inputs
            day = ctk.CTkEntry(fee_row_frame, width=35, placeholder_text="يوم", justify="center")
            month = ctk.CTkEntry(fee_row_frame, width=35, placeholder_text="شهر", justify="center")
            year = ctk.CTkEntry(fee_row_frame, width=50, placeholder_text="سنة", justify="center")
            
            day.grid(row=0, column=0, padx=4, sticky="ew")
            month.grid(row=0, column=1, padx=4, sticky="ew")
            year.grid(row=0, column=2, padx=4, sticky="ew")
            
            self.fee_date_widgets.append((day, month, year))
            
            # Amount entry
            entry = ctk.CTkEntry(fee_row_frame, width=80, justify="right", font=("Arial", 14))
            entry.grid(row=0, column=3, padx=4, sticky="ew")
            self.fee_entries.append(entry)
            
            # Fee type label
            ctk.CTkLabel(
                fee_row_frame,
                text=FEE_TYPES[i],
                font=("Arial", 13),
                anchor="e",
                justify="right"
            ).grid(row=0, column=4, padx=4, sticky="ew")
            
            row += 1
            
        # Register button
        self.register_button = ctk.CTkButton(
            self.frame,
            text="تسجيل",
            command=self.register_student,
            **REGISTER_BUTTON_STYLE
        )
        self.register_button.grid(row=row, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        
    def register_student(self):
        """Handle student registration."""
        name = self.name_entry.get().strip()
        nid = self.nid_entry.get().strip()
        term = self.term_var.get().strip()
        gender = self.gender_var.get().strip()
        phone1 = self.phone1_entry.get().strip()
        phone2 = self.phone2_entry.get().strip()
        fees = [f.get().strip() for f in self.fee_entries]
        fee_dates = get_fee_dates(self.fee_date_widgets)
        
        if not validate_required_fields(name, nid, phone1, phone2):
            return
            
        # Validate fee amounts are numbers
        for fee in fees:
            if fee:
                try:
                    float(fee)
                except ValueError:
                    messagebox.showerror("خطأ", "يجب أن تكون جميع مبالغ الرسوم أرقامًا صحيحة.", parent=self.master)
                    return
            
        add_student(name, nid, term, gender, phone1, phone2, fees, fee_dates)
        messagebox.showinfo("نجاح", "تم تسجيل الطالب بنجاح")
        
        # Clear form
        clear_entry(self.name_entry, "أدخل الاسم")
        clear_entry(self.nid_entry, "أدخل الرقم القومي")
        clear_entry(self.phone1_entry, "أدخل رقم الهاتف")
        clear_entry(self.phone2_entry, "أدخل رقم الهاتف اخر ان وجد*")
        clear_fee_entries(self.fee_entries, self.fee_date_widgets)
        
    def go_back(self):
        """Handle back button click."""
        for widget in self.master.winfo_children():
            widget.destroy()
        self.on_back() 