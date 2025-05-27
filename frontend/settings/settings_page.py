"""
Settings module for Elnada Kindergarten Management System.
This module handles the settings interface.
"""

# Third-party imports
import customtkinter
from customtkinter import CTkFrame, CTkLabel, CTkButton
import arabic_reshaper
from bidi.algorithm import get_display
import threading
import tkinter.messagebox as messagebox

# Local imports
from .database_backup import DatabaseBackup

class SettingsPage(CTkFrame):
    """
    Handles the application settings interface.

    This class manages the settings page UI.
    """

    def __init__(self, parent_frame, main_window, on_back):
        """
        Initialize the settings interface.

        Args:
            parent_frame: The frame to place the settings UI in.
            main_window: The main application window (CTk object) - kept for potential future use.
            on_back: Callback function to return to the previous page (dashboard).
        """
        super().__init__(parent_frame, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.main_window = main_window # Kept for potential future use
        self.on_back = on_back # Kept in case it's used elsewhere or for context
        self.db_backup = DatabaseBackup(self)
        self.setup_ui()
        
        # Start automatic backup system
        self.db_backup.start_automatic_backup()

    def arabic(self, text: str) -> str:
        """
        Convert and display Arabic text properly.

        Args:
            text (str): The Arabic text to be displayed

        Returns:
            str: Properly formatted Arabic text
        """
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def setup_ui(self):
        """Set up the settings page user interface."""
        # Configure grid for the main page frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Content
        # Removed grid_rowconfigure for Back button

        # Create header frame
        header_frame = CTkFrame(self, fg_color="#1F6BB5", corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)

        # Title label
        title_label = CTkLabel(
            header_frame,
            text=self.arabic("الإعدادات"),
            font=("Arial Black", 32), 
            text_color="white"
        )
        title_label.grid(row=0, column=0, pady=10)

        # Content frame for settings options
        content_frame = CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)
        # Configure rows within content_frame for better spacing
        content_frame.grid_rowconfigure(0, weight=0) # Backup label
        content_frame.grid_rowconfigure(1, weight=0) # Local backup button
        content_frame.grid_rowconfigure(2, weight=0) # Google Drive backup button
        content_frame.grid_rowconfigure(3, weight=1) # Spacer row

        # Database backup section
        backup_label = CTkLabel(
            content_frame,
            text=self.arabic("نسخ احتياطي للبيانات:"),
            font=("Arial", 18, "bold"),
            text_color="#333"
        )
        backup_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="e") # Changed sticky to "e"

        # Local backup button
        local_backup_button = CTkButton(
            content_frame,
            text=self.arabic("حفظ البيانات محلياً"),
            font=("Arial", 16),
            command=self.backup_database
        )
        local_backup_button.grid(row=1, column=0, padx=20, pady=5, sticky="n")

        # Google Drive backup button
        drive_backup_button = CTkButton(
            content_frame,
            text=self.arabic("حفظ البيانات على Google Drive"),
            font=("Arial", 16),
            command=self.backup_to_drive
        )
        drive_backup_button.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="n")
        
        # Removed Back button

    def backup_database(self):
        """Handle database backup process."""
        # Show progress window
        progress_window = self.db_backup.show_backup_progress()
        
        def on_backup_complete(success, message):
            if progress_window and progress_window.winfo_exists():
                 progress_window.destroy()
            if success:
                messagebox.showinfo("نجاح", message)
            else:
                messagebox.showerror("خطأ", message)
        
        # Start backup in a separate thread
        threading.Thread(
            target=self.db_backup.backup_database,
            args=(None, on_backup_complete),
            daemon=True
        ).start()

    def backup_to_drive(self):
        """Handle Google Drive backup."""
        # Show progress window
        progress_window = self.db_backup.show_backup_progress()
        
        # Start backup in a separate thread
        def backup_thread():
            self.db_backup.backup_to_google_drive(
                progress_callback=None,
                completion_callback=lambda success, message: self.show_backup_result(success, message, progress_window)
            )
            
        threading.Thread(target=backup_thread, daemon=True).start()

    def show_backup_result(self, success, message, progress_window):
        """Show backup result message."""
        # Close progress window
        if progress_window and progress_window.winfo_exists():
            progress_window.destroy()
            
        # Show result message
        if success:
            messagebox.showinfo("نجاح", message)
        else:
            messagebox.showerror("خطأ", message) 