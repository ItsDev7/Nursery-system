"""
Popup window to display student details.
"""
import customtkinter as ctk
from typing import Callable, Dict, Any, Optional

class StudentDetailsPopup:
    """A toplevel window to show detailed information about a student."""

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
        self.details_window = None
        self.show()

    def arabic(self, text: str) -> str:
        # Assuming Arabic reshaping/bidi handling is done elsewhere or not needed here
        return text

    def show(self):
        """Creates and displays the student details popup window."""
        # Prevent opening multiple popups
        if self.details_window is not None and self.details_window.winfo_exists():
            self.details_window.focus_force()
            return

        self.details_window = ctk.CTkToplevel(self.main)
        self.details_window.title(self.arabic(f"تفاصيل الطالب - {self.student.get('name', '')}"))
        self.details_window.geometry("400x470")
        self.details_window.resizable(False, False)
        self.details_window.transient(self.main)  # Make the popup appear on top of the main window
        self.details_window.grab_set()  # Make the popup modal

        # Set a minimum width to ensure the title is visible
        self.details_window.minsize(width=400, height=150)

        # Calculate position to center above the main window
        self.details_window.update_idletasks() # Update to get correct window size
        main_x = self.main.winfo_x()
        main_y = self.main.winfo_y()
        main_width = self.main.winfo_width()
        main_height = self.main.winfo_height()
        
        # Position the popup centered on the screen based on main window position
        popup_width = self.details_window.winfo_width()
        popup_height = self.details_window.winfo_height()
        x = main_x + (main_width - popup_width) // 2
        y = main_y + (main_height - popup_height) // 2 # Removed upward offset
        
        self.details_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}") # Set geometry with calculated position

        # Frame to hold all content in the popup
        frame = ctk.CTkFrame(self.details_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title label for the popup
        title_label = ctk.CTkLabel(
            frame,
            text=self.arabic("معلومات الطالب"),
            font=("Arial", 20, "bold"),
            text_color="#2D8CFF"
        )
        title_label.pack(pady=(0, 15))

        # Student basic information
        info = [
            ("👤", f"الاسم: {self.student.get('name', '')}"),
            ("🧾", f"الرقم القومي: {self.student.get('nid', '')}"),
            ("🏫", f"المستوى الدراسي: {self.student.get('term', '')}"),
            ("⚧", f"الجنس: {self.student.get('gender', '')}"),
            ("📞", f"هاتف ولي الأمر: {self.student.get('phone1', '')}"),
            ("📞", f"هاتف ولي أمر آخر: {self.student.get('phone2', '')}")
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
                text=self.arabic(text),
                font=("Arial", 16),
                anchor="e",
                justify="right"
            ).pack(side="right", fill="x", expand=True)

        # Fees section title
        fees_title = ctk.CTkLabel(
            frame,
            text=self.arabic("الرسوم الدراسية"),
            font=("Arial", 18, "bold"),
            text_color="#4CAF50"
        )
        fees_title.pack(pady=(15, 10))

        # Fee details
        fee_names = [
            "القسط الأول",
            "القسط الثاني",
            "القسط الثالث",
            "الملابس أو القسط الرابع*"
        ]
        fees = [self.student.get(f"fee{i+1}", "") for i in range(4)]
        fee_dates = [self.student.get(f"fee{i+1}_date", "") for i in range(4)]

        # Display fee information
        for i in range(4):
            row_fee = ctk.CTkFrame(frame, fg_color="transparent")
            row_fee.pack(fill="x", pady=2)
            ctk.CTkLabel(
                row_fee,
                text=self.arabic(f"{fee_names[i]}:"),
                font=("Arial", 15, "bold"),
                width=120,
                anchor="e"
            ).pack(side="right")
            ctk.CTkLabel(
                row_fee,
                text=self.arabic(f"{fees[i]}"),
                font=("Arial", 15),
                width=60,
                anchor="e",
                text_color="#2D8CFF"
            ).pack(side="right", padx=(0, 10))
            ctk.CTkLabel(
                row_fee,
                text=self.arabic(f"تاريخ الدفع: {fee_dates[i]}"),
                font=("Arial", 14),
                anchor="e",
                text_color="#666666"
            ).pack(side="right", padx=(0, 10))

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