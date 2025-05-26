"""Teacher salary management popup windows implementation.

This module provides popup windows for viewing, adding, and editing
teacher salary entries.
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, Any, Callable, Optional
from backend.database import get_teacher_salaries, add_teacher_salary, update_teacher_salary
from .utils import DateEntry

class EditSalaryPopup(ctk.CTkToplevel):
    """Popup window for editing an existing salary entry.
    
    Provides a form to modify the amount and date of a specific salary record.
    """
    
    def __init__(self, master, salary_id: int, current_amount: float, current_date: str, 
                 arabic_handler: Callable, on_save: Callable):
        """Initialize the EditSalaryPopup.
        
        Args:
            master: The parent widget.
            salary_id: The ID of the salary entry to edit.
            current_amount: The current amount of the salary.
            current_date: The current date of the salary (YYYY-MM-DD format).
            arabic_handler: The function to use for Arabic text handling.
            on_save: Callback function to run after saving changes.
        """
        super().__init__(master)
        self.salary_id = salary_id
        self.arabic_handler = arabic_handler
        self.on_save = on_save
        
        # Set window title and basic properties
        self.title(self.arabic_handler("تعديل المرتب")) # "Edit Salary"
        self.geometry("300x250") # Set initial size
        self.transient(master) # Make popup appear on top of master
        self.grab_set() # Make popup modal
        
        # Calculate position to center above the parent window
        master.update_idletasks() # Ensure master geometry is up-to-date
        x = master.winfo_x() + (master.winfo_width() - 300) // 2 # Center horizontally
        y = master.winfo_y() + (master.winfo_height() - 250) // 2 - 50 # Center vertically with upward offset
        self.geometry(f"+{x}+{y}") # Set window position
        
        # Create the main frame for form elements
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- Form Fields ---
        # Amount entry field
        ctk.CTkLabel(frame, text=self.arabic_handler("المبلغ:"), font=("Arial", 14)).pack(pady=(0, 5)) # "Amount:"
        self.amount_entry = ctk.CTkEntry(frame, justify="right")
        self.amount_entry.pack(fill="x", pady=(0, 10))
        self.amount_entry.insert(0, str(current_amount)) # Populate with current amount
        
        # Date entry field using DateEntry widget
        ctk.CTkLabel(frame, text=self.arabic_handler("التاريخ:"), font=("Arial", 14)).pack(pady=(0, 5)) # "Date:"
        self.date_entry = DateEntry(frame, self.arabic_handler)
        self.date_entry.pack(fill="x", pady=(0, 10))
        self.date_entry.set_date(current_date) # Populate with current date
        
        # Save button
        ctk.CTkButton(
            frame,
            text=self.arabic_handler("حفظ"), # "Save"
            command=self.save_changes,
            fg_color="#4CAF50", # Green color
            hover_color="#45a049"
        ).pack(pady=10)
        
        # Bind the window closing protocol (X button) to destroy the window
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
    def save_changes(self):
        """Save the changes to the salary entry.
        
        Validates input, updates the database, shows messages, and closes the popup.
        """
        amount_str = self.amount_entry.get().strip()
        date_str = self.date_entry.get_date()
        
        # Input validation
        if not amount_str or not date_str:
            messagebox.showwarning(
                self.arabic_handler("تحذير"), # "Warning"
                self.arabic_handler("الرجاء إدخال المبلغ والتاريخ.") # "Please enter amount and date."
            )
            return
            
        # Validate amount is a number
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning(
                self.arabic_handler("تحذير"), # "Warning"
                self.arabic_handler("الرجاء إدخال مبلغ صحيح.") # "Please enter a valid amount."
            )
            return
            
        # Update the salary in the database
        update_teacher_salary(self.salary_id, amount, date_str)
        
        # Show success message
        messagebox.showinfo(
            self.arabic_handler("تم"), # "Done"
            self.arabic_handler("تم تحديث المرتب بنجاح.") # "Salary updated successfully."
        )
        
        # Trigger the on_save callback (e.g., to refresh the list in the main salary popup)
        self.on_save()
        
        # Close the popup
        self.destroy()

class TeacherSalaryPopup(ctk.CTkToplevel):
    """Popup window to manage teacher salaries.
    
    Displays a list of salary entries for a specific teacher,
    allows adding new entries and editing existing ones.
    """

    def __init__(self, master, teacher: Dict[str, Any], arabic_handler: Callable, on_close: Optional[Callable] = None):
        """Initialize the teacher salary popup.

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

        # Set window title based on teacher's name
        self.title(self.arabic_handler(f"إدارة مرتبات المعلمة: {teacher.get('name', '')}")) # "Manage Teacher Salaries: [Teacher Name]"
        self.geometry("500x400") # Set initial size
        self.transient(master)  # Make the popup appear on top of the main window
        self.grab_set()  # Make the popup modal

        # Calculate position to center over the main window
        master.update_idletasks() # Ensure master geometry is up-to-date
        main_x = master.winfo_x()
        main_y = master.winfo_y()
        main_width = master.winfo_width()
        main_height = master.winfo_height()
        
        # Calculate center position with upward offset
        popup_width = 500 # Use fixed width for calculation
        popup_height = 400 # Use fixed height for calculation
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2 - 50  # Offset by 50 pixels upward
        
        # Set the window position
        self.geometry(f"+{x}+{y}") # Use +x+y format to set position without size

        self.setup_ui()
        # Bind the window closing protocol (X button) to the custom close function
        self.protocol("WM_DELETE_WINDOW", self.close_popup)  # Handle window closing

    def setup_ui(self):
        """Sets up the UI components for the main salary management popup.
        
        Includes sections for adding new salaries and displaying the list of existing salaries.
        """
        # Configure grid for the main popup frame (self)
        self.grid_columnconfigure(0, weight=1) # Allow the main column to expand horizontally
        self.grid_rowconfigure(1, weight=0) # Add salary section row (fixed height)
        self.grid_rowconfigure(3, weight=1)  # Salaries list scrollable frame row (expands vertically)
        

        # --- Add Salary Section ---
        add_frame = ctk.CTkFrame(self) # Frame to hold add salary controls
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew") # Place at top, expand horizontally
        # Configure columns within the add_frame for RTL layout: [Date Entry] [Amount Entry] [Add Button]
        add_frame.grid_columnconfigure(0, weight=1)  # Date entry column (expands)
        add_frame.grid_columnconfigure(1, weight=1)  # Amount entry column (expands)
        add_frame.grid_columnconfigure(2, weight=0)  # Add button column (fixed size)

        # Amount Entry (RTL: Placed to the left of Date Entry usually, but grid handles order)
        self.amount_entry = ctk.CTkEntry(add_frame, placeholder_text=self.arabic_handler("مبلغ المرتب"), justify="right") # "Salary Amount"
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew") # Place in column 1

        # Date Entry (RTL: Placed to the right of Amount Entry usually)
        self.date_entry = DateEntry(add_frame, self.arabic_handler)
        self.date_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew") # Place in column 0

        # Add Button (RTL: Placed on the far right)
        add_button = ctk.CTkButton(add_frame, text=self.arabic_handler("إضافة مرتب"), command=self.add_salary) # "Add Salary"
        add_button.grid(row=0, column=2, padx=5, pady=5) # Place in column 2

        # --- Salaries List Section ---
        # Label for the salaries list
        salaries_label = ctk.CTkLabel(self, text=self.arabic_handler("المرتبات المسجلة:"), font=("Arial", 14, "bold")) # "Recorded Salaries:"
        salaries_label.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="ew") # Place below add frame

        # Scrollable frame to display the list of salaries
        self.salaries_scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#f5f5f5") # Light gray background
        self.salaries_scroll_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew") # Place below label, expands
        # Configure the inner frame within the scrollable frame to expand horizontally
        self.salaries_scroll_frame.grid_columnconfigure(0, weight=1)

        # Load and display the initial list of salaries
        self.load_salaries()

    def add_salary(self):
        """Adds a new salary entry to the database.
        
        Validates input, calls the backend function, shows messages, and refreshes the list.
        """
        amount_str = self.amount_entry.get().strip()
        date_str = self.date_entry.get_date()

        # Input validation
        if not amount_str or not date_str:
            messagebox.showwarning(self.arabic_handler("تحذير"), self.arabic_handler("الرجاء إدخال المبلغ والتاريخ.")) # "Warning", "Please enter amount and date."
            return

        # Validate amount is a number
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning(self.arabic_handler("تحذير"), self.arabic_handler("الرجاء إدخال مبلغ صحيح.")) # "Warning", "Please enter a valid amount."
            return

        # Get teacher ID (should be available from __init__)
        teacher_id = self.teacher.get('id')
        if teacher_id is None:
             messagebox.showerror(self.arabic_handler("خطأ"), self.arabic_handler("لا يمكن إضافة المرتب. معرف المعلمة مفقود.")) # "Error", "Cannot add salary. Teacher ID is missing."
             return # Prevent adding if ID is missing

        # Add salary to database
        add_teacher_salary(teacher_id, amount, date_str)
        
        # Show success message
        messagebox.showinfo(self.arabic_handler("تم"), self.arabic_handler("تم إضافة المرتب بنجاح.")) # "Done", "Salary added successfully."
        
        # Clear input fields
        self.amount_entry.delete(0, ctk.END)
        self.date_entry.set_date("")  # Clear date entry
        
        # Refresh the displayed list of salaries
        self.load_salaries()  

    def load_salaries(self):
        """Loads and displays existing salaries for the teacher from the database.
        
        Clears the current list and populates it with updated data.
        """
        # Clear existing entries in the scrollable frame
        for widget in self.salaries_scroll_frame.winfo_children():
            widget.destroy()

        # Get teacher ID (should be available)
        teacher_id = self.teacher.get('id')
        if teacher_id is None:
            # Display error message if teacher ID is missing
            ctk.CTkLabel(self.salaries_scroll_frame, text=self.arabic_handler("لا يمكن عرض المرتبات. معرف المعلمة مفقود.")).pack(pady=10) # "Cannot display salaries. Teacher ID is missing."
            return

        # Retrieve salaries from the database
        salaries = get_teacher_salaries(teacher_id)

        if salaries:
            # --- Create Table Headers for Salaries List ---
            header_frame = ctk.CTkFrame(self.salaries_scroll_frame) # Frame for headers
            header_frame.pack(fill="x", pady=(0, 5)) # Pack above salary entries
            # Configure header column weights to match salary entry rows
            header_frame.grid_columnconfigure(0, weight=1) # Date column
            header_frame.grid_columnconfigure(1, weight=1) # Amount column
            header_frame.grid_columnconfigure(2, weight=0)  # Edit button column (fixed size)

            # Place headers (RTL: Edit | Amount | Date)
            ctk.CTkLabel(header_frame, text=self.arabic_handler("المبلغ"), font=("Arial", 13, "bold")).grid(row=0, column=1, padx=5, sticky="e") # "Amount"
            ctk.CTkLabel(header_frame, text=self.arabic_handler("التاريخ"), font=("Arial", 13, "bold")).grid(row=0, column=0, padx=5, sticky="w") # "Date"
            ctk.CTkLabel(header_frame, text=self.arabic_handler("تعديل"), font=("Arial", 13, "bold")).grid(row=0, column=2, padx=5) # "Edit"

            # --- Display Each Salary Entry ---
            for salary_id, amount, date in salaries:
                row_frame = ctk.CTkFrame(self.salaries_scroll_frame) # Frame for each salary row
                row_frame.pack(fill="x", pady=2)
                # Configure row column weights to match headers
                row_frame.grid_columnconfigure(0, weight=1)
                row_frame.grid_columnconfigure(1, weight=1)
                row_frame.grid_columnconfigure(2, weight=0)

                # Display amount and date (RTL: Edit | Amount | Date)
                ctk.CTkLabel(row_frame, text=str(amount), font=("Arial", 13)).grid(row=0, column=1, padx=5, sticky="e")
                ctk.CTkLabel(row_frame, text=date, font=("Arial", 13)).grid(row=0, column=0, padx=5, sticky="w")
                
                # Edit button for the salary entry
                edit_button = ctk.CTkButton(
                    row_frame,
                    text=self.arabic_handler("تعديل"), # "Edit"
                    width=60,
                    command=lambda sid=salary_id, amt=amount, dt=date: self.edit_salary(sid, amt, dt) # Pass salary details to edit method
                )
                edit_button.grid(row=0, column=2, padx=5)
        else: # Message if no salaries are recorded
            ctk.CTkLabel(self.salaries_scroll_frame, text=self.arabic_handler("لا توجد مرتبات مسجلة لهذه المعلمة.")).pack(pady=10) # "No salaries recorded for this teacher."

    def edit_salary(self, salary_id: int, current_amount: float, current_date: str):
        """Opens the EditSalaryPopup window to modify a specific salary entry.
        
        Args:
            salary_id: The ID of the salary entry to edit.
            current_amount: The current amount of the salary.
            current_date: The current date of the salary.
        """
        # Create and show the EditSalaryPopup
        EditSalaryPopup(
            self, # Pass the main salary popup as master
            salary_id,
            current_amount,
            current_date,
            self.arabic_handler, # Pass the arabic handler
            self.load_salaries # Pass load_salaries as the on_save callback
        )

    def close_popup(self):
        """Closes the main teacher salary popup window.
        
        Executes the on_close callback if provided and returns focus to the master window.
        """
        # Execute the on_close callback if available
        if self.on_close:
            self.on_close() # For example, refresh the search page
            
        self.destroy() # Destroy the popup window widget
        self.master.focus_force()  # Ensure focus returns to the main application window 