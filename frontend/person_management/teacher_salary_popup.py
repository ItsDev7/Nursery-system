import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, Callable
from backend.database import get_teacher_salaries, add_teacher_salary, update_teacher_salary
from datetime import datetime
from .utils import DateEntry

class EditSalaryPopup(ctk.CTkToplevel):
    """Popup window for editing a salary entry."""
    
    def __init__(self, master, salary_id: int, current_amount: float, current_date: str, 
                 arabic_handler: Callable, on_save: Callable):
        super().__init__(master)
        self.salary_id = salary_id
        self.arabic_handler = arabic_handler
        self.on_save = on_save
        
        self.title(self.arabic_handler("تعديل المرتب"))
        self.geometry("300x250")
        self.transient(master)
        self.grab_set()
        
        # Position the popup above the parent window
        x = master.winfo_x() + (master.winfo_width() - 300) // 2
        y = master.winfo_y() + (master.winfo_height() - 200) // 2 - 50
        self.geometry(f"+{x}+{y}")
        
        # Create the form
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Amount entry
        ctk.CTkLabel(frame, text=self.arabic_handler("المبلغ:"), font=("Arial", 14)).pack(pady=(0, 5))
        self.amount_entry = ctk.CTkEntry(frame, justify="right")
        self.amount_entry.pack(fill="x", pady=(0, 10))
        self.amount_entry.insert(0, str(current_amount))
        
        # Date entry
        ctk.CTkLabel(frame, text=self.arabic_handler("التاريخ:"), font=("Arial", 14)).pack(pady=(0, 5))
        self.date_entry = DateEntry(frame, self.arabic_handler)
        self.date_entry.pack(fill="x", pady=(0, 10))
        self.date_entry.set_date(current_date)
        
        # Save button
        ctk.CTkButton(
            frame,
            text=self.arabic_handler("حفظ"),
            command=self.save_changes,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(pady=10)
        
        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
    def save_changes(self):
        """Save the changes to the salary entry."""
        amount_str = self.amount_entry.get().strip()
        date_str = self.date_entry.get_date()
        
        if not amount_str or not date_str:
            messagebox.showwarning(
                self.arabic_handler("تحذير"),
                self.arabic_handler("الرجاء إدخال المبلغ والتاريخ.")
            )
            return
            
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning(
                self.arabic_handler("تحذير"),
                self.arabic_handler("الرجاء إدخال مبلغ صحيح.")
            )
            return
            
        update_teacher_salary(self.salary_id, amount, date_str)
        messagebox.showinfo(
            self.arabic_handler("تم"),
            self.arabic_handler("تم تحديث المرتب بنجاح.")
        )
        self.on_save()
        self.destroy()

class TeacherSalaryPopup(ctk.CTkToplevel):
    """Popup window to manage teacher salaries."""

    def __init__(self, master, teacher: Dict[str, Any], arabic_handler: Callable, on_close: Callable = None):
        """
        Initialize the teacher salary popup.

        Args:
            master: The parent widget.
            teacher: Dictionary containing teacher details.
            arabic_handler: The function to use for Arabic text handling.
            on_close: Callback function to run when the popup is closed.
        """
        super().__init__(master)
        self.master = master
        self.teacher = teacher
        self.arabic_handler = arabic_handler
        self.on_close = on_close

        self.title(self.arabic_handler(f"إدارة مرتبات المعلمة: {teacher.get('name', '')}"))
        self.geometry("500x400")
        self.transient(master)  # Make the popup appear on top of the main window
        self.grab_set()  # Make the popup modal

        # Calculate position to center above the main window
        main_x = master.winfo_x()
        main_y = master.winfo_y()
        main_width = master.winfo_width()
        main_height = master.winfo_height()
        
        # Position the popup above the center of the main window
        popup_width = 500
        popup_height = 400
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2 - 50  # Offset by 50 pixels upward
        
        self.geometry(f"+{x}+{y}")

        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.close_popup)  # Handle window closing

    def setup_ui(self):
        """Set up the UI components for the popup."""
        # Configure grid for the main frame (self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Make the salaries list expandable

        # --- Add Salary Section ---
        add_frame = ctk.CTkFrame(self)
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        add_frame.grid_columnconfigure(0, weight=1)  # Date entry
        add_frame.grid_columnconfigure(1, weight=1)  # Amount entry
        add_frame.grid_columnconfigure(2, weight=0)  # Add button

        # Amount Entry (RTL)
        self.amount_entry = ctk.CTkEntry(add_frame, placeholder_text=self.arabic_handler("مبلغ المرتب"), justify="right")
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Date Entry (RTL)
        self.date_entry = DateEntry(add_frame, self.arabic_handler)
        self.date_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Add Button (RTL)
        add_button = ctk.CTkButton(add_frame, text=self.arabic_handler("إضافة مرتب"), command=self.add_salary)
        add_button.grid(row=0, column=2, padx=5, pady=5)

        # --- Salaries List Section ---
        salaries_label = ctk.CTkLabel(self, text=self.arabic_handler("المرتبات المسجلة:"), font=("Arial", 14, "bold"))
        salaries_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.salaries_scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#f5f5f5")
        self.salaries_scroll_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.salaries_scroll_frame.grid_columnconfigure(0, weight=1)

        self.load_salaries()

    def add_salary(self):
        """Adds a new salary entry."""
        amount_str = self.amount_entry.get().strip()
        date_str = self.date_entry.get_date()

        if not amount_str or not date_str:
            messagebox.showwarning(self.arabic_handler("تحذير"), self.arabic_handler("الرجاء إدخال المبلغ والتاريخ."))
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning(self.arabic_handler("تحذير"), self.arabic_handler("الرجاء إدخال مبلغ صحيح."))
            return

        teacher_id = self.teacher.get('id')
        if teacher_id is None:
             messagebox.showerror(self.arabic_handler("خطأ"), self.arabic_handler("لا يمكن إضافة المرتب. معرف المعلمة مفقود."))
             return

        add_teacher_salary(teacher_id, amount, date_str)
        messagebox.showinfo(self.arabic_handler("تم"), self.arabic_handler("تم إضافة المرتب بنجاح."))
        self.amount_entry.delete(0, ctk.END)
        self.date_entry.set_date("")  # Clear date
        self.load_salaries()  # Refresh the list

    def load_salaries(self):
        """Loads and displays existing salaries for the teacher."""
        # Clear existing entries
        for widget in self.salaries_scroll_frame.winfo_children():
            widget.destroy()

        teacher_id = self.teacher.get('id')
        if teacher_id is None:
            ctk.CTkLabel(self.salaries_scroll_frame, text=self.arabic_handler("لا يمكن عرض المرتبات. معرف المعلمة مفقود.")).pack()
            return

        salaries = get_teacher_salaries(teacher_id)

        if salaries:
            # Add headers for the list
            header_frame = ctk.CTkFrame(self.salaries_scroll_frame)
            header_frame.pack(fill="x", pady=(0, 5))
            header_frame.grid_columnconfigure(0, weight=1)
            header_frame.grid_columnconfigure(1, weight=1)
            header_frame.grid_columnconfigure(2, weight=0)  # For edit button

            ctk.CTkLabel(header_frame, text=self.arabic_handler("المبلغ"), font=("Arial", 13, "bold")).grid(row=0, column=1, padx=5, sticky="e")
            ctk.CTkLabel(header_frame, text=self.arabic_handler("التاريخ"), font=("Arial", 13, "bold")).grid(row=0, column=0, padx=5, sticky="w")
            ctk.CTkLabel(header_frame, text=self.arabic_handler("تعديل"), font=("Arial", 13, "bold")).grid(row=0, column=2, padx=5)

            # Display each salary entry
            for salary_id, amount, date in salaries:
                row_frame = ctk.CTkFrame(self.salaries_scroll_frame)
                row_frame.pack(fill="x", pady=2)
                row_frame.grid_columnconfigure(0, weight=1)
                row_frame.grid_columnconfigure(1, weight=1)
                row_frame.grid_columnconfigure(2, weight=0)  # For edit button

                ctk.CTkLabel(row_frame, text=str(amount), font=("Arial", 13)).grid(row=0, column=1, padx=5, sticky="e")
                ctk.CTkLabel(row_frame, text=date, font=("Arial", 13)).grid(row=0, column=0, padx=5, sticky="w")
                
                # Edit button
                edit_button = ctk.CTkButton(
                    row_frame,
                    text=self.arabic_handler("تعديل"),
                    width=60,
                    command=lambda sid=salary_id, amt=amount, dt=date: self.edit_salary(sid, amt, dt)
                )
                edit_button.grid(row=0, column=2, padx=5)
        else:
            ctk.CTkLabel(self.salaries_scroll_frame, text=self.arabic_handler("لا توجد مرتبات مسجلة لهذه المعلمة.")).pack(pady=10)

    def edit_salary(self, salary_id: int, current_amount: float, current_date: str):
        """Open the edit salary popup."""
        EditSalaryPopup(
            self,
            salary_id,
            current_amount,
            current_date,
            self.arabic_handler,
            self.load_salaries
        )

    def close_popup(self):
        """Closes the popup window."""
        if self.on_close:
            self.on_close()
        self.destroy()
        self.master.focus_force()  # Return focus to main window 