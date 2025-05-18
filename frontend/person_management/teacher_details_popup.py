"""
Popup window to display teacher details.
"""
import customtkinter as ctk
from typing import Callable, Dict, Any, Optional

class TeacherDetailsPopup:
    """A toplevel window to show detailed information about a teacher."""

    def __init__(self, master, teacher: Dict[str, Any], arabic_handler: Optional[Callable[[str], str]] = None, on_close: Optional[Callable] = None):
        """
        Initializes the TeacherDetailsPopup.

        Args:
            master: The parent widget (usually the main application window).
            teacher: A dictionary containing the teacher's data.
            arabic_handler: An optional function to handle Arabic text formatting.
            on_close: An optional callback function to run when the popup is closed.
        """
        self.main = master
        self.teacher = teacher
        self.arabic = arabic_handler or (lambda x: x)  # Use provided handler or identity function
        self.on_close = on_close
        self.details_window = None
        self.show()

    def show(self):
        """Creates and displays the teacher details popup window."""
        # Prevent opening multiple popups
        if self.details_window is not None and self.details_window.winfo_exists():
            self.details_window.focus_force()
            return

        self.details_window = ctk.CTkToplevel(self.main)
        self.details_window.title(self.arabic(f"تفاصيل المعلمة - {self.teacher.get('name', '')}"))
        self.details_window.geometry("420x320")  # Reduced height since we removed salaries section
        self.details_window.resizable(False, False)
        self.details_window.transient(self.main)  # Make the popup appear on top of the main window
        self.details_window.grab_set()  # Make the popup modal

        # Set a minimum width to ensure the title is visible
        self.details_window.minsize(width=450, height=150)

        # Calculate position to center above the main window
        main_x = self.main.winfo_x()
        main_y = self.main.winfo_y()
        main_width = self.main.winfo_width()
        main_height = self.main.winfo_height()
        
        # Position the popup above the center of the main window
        popup_width = 420
        popup_height = 320
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2 - 50  # Offset by 50 pixels upward
        
        self.details_window.geometry(f"+{x}+{y}")

        # Frame to hold all content in the popup
        frame = ctk.CTkFrame(self.details_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title label for the popup
        title_label = ctk.CTkLabel(
            frame,
            text=self.arabic("معلومات المعلمة"),
            font=("Arial", 20, "bold"),
            text_color="#E91E63"
        )
        title_label.pack(pady=(0, 15))

        # Teacher basic information
        info = [
            ("👤", f"الاسم: {self.teacher.get('name', '')}"),
            ("🧾", f"الرقم القومي: {self.teacher.get('nid', '')}"),
            ("🏫", f"المستوى الدراسي: {self.teacher.get('term', '')}"),
            ("⚧", f"الجنس: {self.teacher.get('gender', '')}"),
            ("📞", f"رقم الهاتف: {self.teacher.get('phone1', '')}"),
            ("📞", f"رقم هاتف آخر: {self.teacher.get('phone2', '')}")
        ]
        # Display basic info with icons
        for icon, text in info:
            row_frame = ctk.CTkFrame(frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=3)
            ctk.CTkLabel(
                row_frame,
                text=icon,
                font=("Arial", 20),
                width=30,
                anchor="e"
            ).pack(side="right")
            ctk.CTkLabel(
                row_frame,
                text=self.arabic(text),  # Apply arabic shaping to text
                font=("Arial", 16),
                anchor="e",
                justify="right"
            ).pack(side="right", fill="x", expand=True)

        def close_window():
            self.details_window.destroy()
            self.details_window = None
            if self.on_close:
                self.on_close()
            self.main.focus_force()  # Return focus to main window

        # Handle window closing by pressing the close button (X)
        self.details_window.protocol("WM_DELETE_WINDOW", close_window)

        # Lift window and set focus
        self.details_window.lift()
        self.details_window.grab_set()  # Make the popup modal
        self.details_window.focus_force() 