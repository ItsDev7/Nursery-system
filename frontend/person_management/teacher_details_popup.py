"""Teacher details popup window implementation.

This module provides a toplevel window to display detailed information
about a specific teacher, including personal details and contact information.
"""
import customtkinter as ctk
from typing import Callable, Dict, Any, Optional

class TeacherDetailsPopup:
    """A toplevel window to show detailed information about a teacher.
    
    Displays the teacher's personal details, academic information, and contact
    information in a modal popup window.
    """

    def __init__(self, master, teacher: Dict[str, Any], arabic_handler: Optional[Callable[[str], str]] = None, on_close: Optional[Callable] = None):
        """
        Initializes the TeacherDetailsPopup.

        Args:
            master: The parent widget (usually the main application window).
            teacher: A dictionary containing the teacher's data.
            arabic_handler: An optional function to handle Arabic text formatting.
                            Defaults to an identity function if not provided.
            on_close: An optional callback function to run when the popup is closed.
        """
        self.main = master
        self.teacher = teacher
        self.arabic = arabic_handler or (lambda x: x)  # Use provided handler or identity function
        self.on_close = on_close
        self.details_window = None # Initialize window attribute
        self.show()

    def show(self):
        """Creates and displays the teacher details popup window.
        
        Prevents multiple popups and centers the window over the parent.
        Sets up the layout and populates it with teacher information.
        """
        # Prevent opening multiple popups
        if self.details_window is not None and self.details_window.winfo_exists():
            self.details_window.focus_force() # Bring existing popup to front
            return

        # Create the toplevel window
        self.details_window = ctk.CTkToplevel(self.main)
        self.details_window.title(self.arabic(f"تفاصيل المعلمة - {self.teacher.get('name', '')}")) # Set window title
        self.details_window.geometry("420x320")  # Set initial size (adjusted height)
        self.details_window.resizable(False, False) # Prevent resizing
        self.details_window.transient(self.main)  # Make the popup appear on top of the main window
        self.details_window.grab_set()  # Make the popup modal (block interaction with main window)

        # Set a minimum width to ensure content visibility
        self.details_window.minsize(width=450, height=150)

        # Calculate position to center over the main window
        # Update idletasks to get accurate main window dimensions
        self.main.update_idletasks()
        main_x = self.main.winfo_x()
        main_y = self.main.winfo_y()
        main_width = self.main.winfo_width()
        main_height = self.main.winfo_height()
        
        # Calculate center position
        popup_width = 420 # Use fixed width for calculation
        popup_height = 320 # Use fixed height for calculation
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2 - 50  # Offset by 50 pixels upward for better visibility
        
        # Set the window position
        self.details_window.geometry(f"+{x}+{y}") # Use +x+y format to set position without size

        # Frame to hold all content within the popup
        frame = ctk.CTkFrame(self.details_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Teacher Basic Information Section ---
        # Title label for the basic info section
        title_label = ctk.CTkLabel(
            frame,
            text=self.arabic("معلومات المعلمة"), # "Teacher Information"
            font=("Arial", 20, "bold"),
            text_color="#E91E63" # Color associated with teachers
        )
        title_label.pack(pady=(0, 15))

        # List of basic information fields and their corresponding icons
        info_fields = [
            ("👤", f"الاسم: {self.teacher.get('name', '')}"), # Name
            ("🧾", f"الرقم القومي: {self.teacher.get('nid', '')}"), # National ID
            ("🏫", f"المستوى الدراسي: {self.teacher.get('term', '')}"), # Academic Level
            ("⚧", f"الجنس: {self.teacher.get('gender', '')}"), # Gender
            ("📞", f"رقم الهاتف: {self.teacher.get('phone1', '')}"), # Primary Phone
            ("📞", f"رقم هاتف آخر: {self.teacher.get('phone2', '')}") # Secondary Phone
        ]
        
        # Display basic info with icons in separate frames for RTL alignment
        for icon, text in info_fields:
            row_frame = ctk.CTkFrame(frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=3)
            # Icon on the right for RTL layout
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
                text=self.arabic(text),  # Apply arabic shaping to text
                font=("Arial", 16),
                anchor="e", # Anchor text to the right
                justify="right" # Justify text to the right
            ).pack(side="right", fill="x", expand=True)

        def close_window():
            """Handles closing the popup window and triggering the on_close callback."""
            self.details_window.destroy() # Destroy the window widget
            self.details_window = None # Reset the window attribute
            if self.on_close:
                self.on_close() # Execute the callback function
            self.main.focus_force()  # Return focus to main window

        # Bind the close window protocol (clicking the X button) to the custom close function
        self.details_window.protocol("WM_DELETE_WINDOW", close_window)

        # --- Final Window Setup ---
        # Lift window to the top, make it modal, and set focus
        self.details_window.lift()
        self.details_window.grab_set()
        self.details_window.focus_force() 