"""Student details popup window implementation.

This module provides a toplevel window to display detailed information
about a specific student, including personal details and fee payments.
"""
import customtkinter as ctk
from typing import Callable, Dict, Any, Optional

class StudentDetailsPopup:
    """A toplevel window to show detailed information about a student.
    
    Displays the student's personal details, academic information, contact
    information, and fee payment details in a modal popup window.
    """

    def __init__(self, master, student: Dict[str, Any], on_close: Optional[Callable] = None):
        """
        Initializes the StudentDetailsPopup.

        Args:
            master: The parent widget (usually the main application window).
            student: A dictionary containing the student's data.
            on_close: An optional callback function to run when the popup is closed.
        """
        self.main = master
        self.student = student
        self.on_close = on_close
        self.details_window = None # Initialize window attribute
        self.show()

    def arabic(self, text: str) -> str:
        """Handles potential Arabic text display issues.
        
        Args:
            text: The input string which may contain Arabic characters.
            
        Returns:
            The processed string for display (identity function if no processing needed).
        """
        # Assuming Arabic reshaping/bidi handling is done elsewhere or not needed here
        return text

    def show(self):
        """Creates and displays the student details popup window.
        
        Prevents multiple popups and centers the window over the parent.
        Sets up the layout and populates it with student information.
        """
        # Prevent opening multiple popups
        if self.details_window is not None and self.details_window.winfo_exists():
            self.details_window.focus_force() # Bring existing popup to front
            return

        # Create the toplevel window
        self.details_window = ctk.CTkToplevel(self.main)
        self.details_window.title(self.arabic(f"تفاصيل الطالب - {self.student.get('name', '')}")) # Set window title
        self.details_window.geometry("400x470") # Set initial size
        self.details_window.resizable(False, False) # Prevent resizing
        self.details_window.transient(self.main)  # Make the popup appear on top of the main window
        self.details_window.grab_set()  # Make the popup modal (block interaction with main window)

        # Set a minimum width to ensure content visibility
        self.details_window.minsize(width=400, height=150)

        # Calculate position to center over the main window
        self.details_window.update_idletasks() # Update geometry to get correct window size
        main_x = self.main.winfo_x()
        main_y = self.main.winfo_y()
        main_width = self.main.winfo_width()
        main_height = self.main.winfo_height()
        
        # Calculate center position
        popup_width = self.details_window.winfo_width()
        popup_height = self.details_window.winfo_height()
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2
        
        # Set the window position
        self.details_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        # Frame to hold all content within the popup
        frame = ctk.CTkFrame(self.details_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Student Basic Information Section ---
        # Title label for the basic info section
        title_label = ctk.CTkLabel(
            frame,
            text=self.arabic("معلومات الطالب"), # "Student Information"
            font=("Arial", 20, "bold"),
            text_color="#2D8CFF"
        )
        title_label.pack(pady=(0, 15))

        # List of basic information fields and their corresponding icons
        info_fields = [
            ("👤", f"الاسم: {self.student.get('name', '')}"), # Name
            ("🧾", f"الرقم القومي: {self.student.get('nid', '')}"), # National ID
            ("🏫", f"المستوى الدراسي: {self.student.get('term', '')}"), # Academic Level
            ("⚧", f"الجنس: {self.student.get('gender', '')}"), # Gender
            ("📞", f"هاتف ولي الأمر: {self.student.get('phone1', '')}"), # Primary Guardian Phone
            ("📞", f"هاتف ولي أمر آخر: {self.student.get('phone2', '')}") # Secondary Guardian Phone
        ]
        
        # Display basic info with icons in separate frames for RTL alignment
        for icon, text in info_fields:
            row_frame = ctk.CTkFrame(frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=3)
            # Icon on the right for RTL
            ctk.CTkLabel(
                row_frame,
                text=icon,
                font=("Arial", 20),
                width=30,
                anchor="e" # Anchor to the right
            ).pack(side="right")
            # Text label on the right, expanding to fill space
            ctk.CTkLabel(
                row_frame,
                text=self.arabic(text),
                font=("Arial", 16),
                anchor="e", # Anchor text to the right
                justify="right" # Justify text to the right
            ).pack(side="right", fill="x", expand=True)

        # --- Fees Information Section ---
        # Title label for the fees section
        fees_title = ctk.CTkLabel(
            frame,
            text=self.arabic("الرسوم الدراسية"), # "Tuition Fees"
            font=("Arial", 18, "bold"),
            text_color="#4CAF50"
        )
        fees_title.pack(pady=(15, 10))

        # List of fee names
        fee_names = [
            "القسط الأول", # First Installment
            "القسط الثاني", # Second Installment
            "القسط الثالث", # Third Installment
            "الملابس أو القسط الرابع*" # Clothing or Fourth Installment*
        ]
        # Retrieve fee amounts and dates from student data
        fees = [self.student.get(f"fee{i+1}", "") for i in range(4)]
        fee_dates = [self.student.get(f"fee{i+1}_date", "") for i in range(4)]

        # Display fee information for each installment
        for i in range(4):
            row_fee = ctk.CTkFrame(frame, fg_color="transparent")
            row_fee.pack(fill="x", pady=2)
            # Fee name label on the right
            ctk.CTkLabel(
                row_fee,
                text=self.arabic(f"{fee_names[i]}:"),
                font=("Arial", 15, "bold"),
                width=120,
                anchor="e" # Anchor to the right
            ).pack(side="right")
            # Fee amount label in the middle
            ctk.CTkLabel(
                row_fee,
                text=self.arabic(f"{fees[i]}"),
                font=("Arial", 15),
                width=60,
                anchor="e", # Anchor to the right
                text_color="#2D8CFF"
            ).pack(side="right", padx=(0, 10))
            # Fee date label on the left
            ctk.CTkLabel(
                row_fee,
                text=self.arabic(f"تاريخ الدفع: {fee_dates[i]}"), # "Payment Date"
                font=("Arial", 14),
                anchor="e", # Anchor to the right
                text_color="#666666"
            ).pack(side="right", padx=(0, 10))

        def close_window():
            """Handles closing the popup window and triggering the on_close callback."""
            self.details_window.destroy() # Destroy the window
            self.details_window = None # Reset window attribute
            if self.on_close:
                self.on_close() # Execute the callback function
            self.main.focus_force() # Return focus to the main window

        # Bind the close window protocol to the custom close function
        self.details_window.protocol("WM_DELETE_WINDOW", close_window)

        # --- Final Window Setup ---
        # Lift window to the top, make it modal, and set focus
        self.details_window.lift()
        self.details_window.grab_set()
        self.details_window.focus_force() 