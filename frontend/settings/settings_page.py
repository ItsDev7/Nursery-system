"""
Settings module for Elnada Kindergarten Management System.
This module handles the settings interface and backup operations.
"""

# Third-party imports
import customtkinter
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkTextbox
import arabic_reshaper
from bidi.algorithm import get_display
import threading
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import webbrowser

# Local imports
from .database_backup import DatabaseBackup
from backend import database

class SettingsPage(CTkFrame):
    """
    Handles the application settings interface and backup operations.

    This class manages the settings page UI and provides functionality for:
    - Local database backup
    - Google Drive backup
    - Backup path configuration
    - Automatic backup scheduling

    Attributes:
        main_window: The main application window
        on_back: Callback function to return to previous page
        db_backup: DatabaseBackup instance for backup operations
        local_backup_path_entry: Entry widget for local backup path
        auth_window: Window for Google Drive authentication
        auth_url_textbox: Textbox for displaying auth URL
        verification_code_entry: Entry widget for verification code
    """

    def __init__(self, parent_frame, main_window, on_back):
        """
        Initialize the settings interface.

        Args:
            parent_frame: The frame to place the settings UI in
            main_window: The main application window
            on_back: Callback function to return to previous page
        """
        super().__init__(parent_frame, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.main_window = main_window
        self.on_back = on_back
        self.db_backup = DatabaseBackup(self)
        self.local_backup_path_entry = None
        self.auth_window = None
        self.auth_url_textbox = None
        self.verification_code_entry = None
        
        self.setup_ui()
        self.load_saved_backup_path()
        self.db_backup.start_automatic_backup()

    def arabic(self, text: str) -> str:
        """
        Convert and display Arabic text properly.

        Args:
            text: The Arabic text to be displayed

        Returns:
            Properly formatted Arabic text
        """
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def setup_ui(self):
        """Set up the settings page user interface."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content

        # Create header
        header_frame = CTkFrame(self, fg_color="#1F6BB5", corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = CTkLabel(
            header_frame,
            text=self.arabic("الإعدادات"),
            font=("Arial Black", 32), 
            text_color="white"
        )
        title_label.grid(row=0, column=0, pady=10)

        # Create content frame
        content_frame = CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)  # Labels/entries
        content_frame.grid_columnconfigure(1, weight=2)  # Entries/buttons
        content_frame.grid_columnconfigure(2, weight=0)  # Browse button

        # Backup section
        backup_label = CTkLabel(
            content_frame,
            text=self.arabic("نسخ احتياطي للبيانات:"),
            font=("Arial", 18, "bold"),
            text_color="#333"
        )
        backup_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="e", columnspan=3)

        # Local backup path
        local_path_label = CTkLabel(
            content_frame,
            text=self.arabic("مسار الحفظ المحلي:"),
            font=("Arial", 16),
            text_color="#333"
        )
        local_path_label.grid(row=1, column=2, padx=(20, 0), pady=5, sticky="w")

        self.local_backup_path_entry = CTkEntry(
            content_frame,
            placeholder_text=self.arabic("أدخل مسار الحفظ المحلي هنا"),
            font=("Arial", 14),
            width=300
        )
        self.local_backup_path_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        browse_button = CTkButton(
            content_frame,
            text=self.arabic("استعراض"),
            font=("Arial", 14),
            command=self.browse_local_backup_path
        )
        browse_button.grid(row=1, column=0, padx=(0, 20), pady=5, sticky="e")

        # Save path button
        save_path_button = CTkButton(
            content_frame,
            text=self.arabic("حفظ المسار"),
            font=("Arial", 16),
            command=self.save_local_backup_path
        )
        save_path_button.grid(row=2, column=1, padx=5, pady=5, sticky="n")

        # Backup buttons
        local_backup_button = CTkButton(
            content_frame,
            text=self.arabic("حفظ البيانات محلياً الآن"),
            font=("Arial", 16),
            command=self.backup_database
        )
        local_backup_button.grid(row=3, column=1, padx=5, pady=(10, 5), sticky="n")

        drive_backup_button = CTkButton(
            content_frame,
            text=self.arabic("حفظ البيانات على Google Drive"),
            font=("Arial", 16),
            command=self.backup_to_drive
        )
        drive_backup_button.grid(row=4, column=1, padx=5, pady=(5, 20), sticky="n")

        # Spacer
        content_frame.grid_rowconfigure(5, weight=1)

    def browse_local_backup_path(self):
        """Open a file dialog to select a folder for local backup."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.local_backup_path_entry.delete(0, "end")
            self.local_backup_path_entry.insert(0, folder_selected)

    def save_local_backup_path(self):
        """Save the entered local backup path to the database."""
        path = self.local_backup_path_entry.get().strip()
        if path:
            database.save_setting('local_backup_path', path)
            messagebox.showinfo("نجاح", ("تم حفظ مسار الحفظ المحلي بنجاح."))
        else:
            messagebox.showwarning("تحذير", ("الرجاء إدخال مسار صالح للحفظ."))

    def load_saved_backup_path(self):
        """Load the saved local backup path from the database and populate the entry."""
        saved_path = database.get_setting('local_backup_path')
        if saved_path:
            self.local_backup_path_entry.delete(0, "end")
            self.local_backup_path_entry.insert(0, saved_path)

    def backup_database(self):
        """Handle database backup process using the user-specified path."""
        backup_path = self.local_backup_path_entry.get().strip()

        if not backup_path:
            messagebox.showwarning("تحذير", ("الرجاء تحديد مسار الحفظ المحلي أولاً."))
            return

        progress_window = self.db_backup.show_backup_progress()

        def on_backup_complete(success, message):
            if progress_window and progress_window.winfo_exists():
                progress_window.after(100, progress_window.destroy)

            def show_message():
                if success:
                    messagebox.showinfo("نجاح", message)
                else:
                    messagebox.showerror("خطأ", message)

            self.after(0, show_message)

        threading.Thread(
            target=self.db_backup.backup_database,
            args=(backup_path, None, on_backup_complete),
            daemon=True
        ).start()

    def show_auth_window(self, auth_url):
        """
        Show the authentication window with the authorization URL.

        Args:
            auth_url: The Google Drive authorization URL
        """
        if self.auth_window is None or not self.auth_window.winfo_exists():
            self.auth_window = customtkinter.CTkToplevel(self)
            self.auth_window.title(("مصادقة Google Drive"))
            self.auth_window.geometry("600x400")
            self.auth_window.resizable(False, False)
            
            self.auth_window.transient(self)
            self.auth_window.grab_set()
            
            self.auth_window.grid_columnconfigure(0, weight=1)
            self.auth_window.grid_rowconfigure(3, weight=1)
            
            # Instructions
            instructions = CTkLabel(
                self.auth_window,
                text=("""
                للاتصال بـ Google Drive، اتبع الخطوات التالية:
                انسخ الرابط ادناه .1
                2. الصقه في متصفح الويب
                3. قم بتسجيل الدخول إلى حساب Google الخاص بك
                4. وافق على الأذونات المطلوبة
                5. انسخ كود التحقق الذي سيظهر لك
                6. الصق الكود في الحقل أدناه
                """),
                font=("Arial", 14),
                justify="right",
                wraplength=550
            )
            instructions.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
            
            # Auth URL
            self.auth_url_textbox = CTkTextbox(
                self.auth_window,
                height=60,
                font=("Arial", 12)
            )
            self.auth_url_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
            self.auth_url_textbox.insert("1.0", auth_url)
            self.auth_url_textbox.configure(state="disabled")
            
            # Verification code
            verification_frame = CTkFrame(self.auth_window)
            verification_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
            verification_frame.grid_columnconfigure(1, weight=1)
            
            verification_label = CTkLabel(
                verification_frame,
                text=self.arabic("كود التحقق:"),
                font=("Arial", 14)
            )
            verification_label.grid(row=0, column=0, padx=(0, 10))
            
            self.verification_code_entry = CTkEntry(
                verification_frame,
                font=("Arial", 14),
                width=200
            )
            self.verification_code_entry.grid(row=0, column=1, sticky="ew")
            
            # Submit button
            submit_button = CTkButton(
                self.auth_window,
                text=self.arabic("تأكيد"),
                font=("Arial", 14),
                command=self.handle_verification_code
            )
            submit_button.grid(row=3, column=0, padx=20, pady=20)
            
            # Center window
            self.auth_window.update_idletasks()
            width = self.auth_window.winfo_width()
            height = self.auth_window.winfo_height()
            x = (self.auth_window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.auth_window.winfo_screenheight() // 2) - (height // 2)
            self.auth_window.geometry(f"{width}x{height}+{x}+{y}")

    def handle_verification_code(self):
        """Handle the verification code submission."""
        verification_code = self.verification_code_entry.get().strip()
        if not verification_code:
            messagebox.showwarning(
                ("تحذير"),
                ("الرجاء إدخال كود التحقق")
            )
            return
            
        def auth_thread():
            success = self.db_backup.complete_google_drive_auth(verification_code)
            if success:
                self.auth_window.destroy()
                self.backup_to_google_drive()
            else:
                messagebox.showerror(
                    ("خطأ"),
                    ("فشل في إكمال المصادقة. الرجاء المحاولة مرة أخرى.")
                )
                
        threading.Thread(target=auth_thread, daemon=True).start()

    def backup_to_drive(self):
        """Handle Google Drive backup with OOB authentication."""
        def auth_callback(auth_url):
            self.show_auth_window(auth_url)
            
        if not self.db_backup.setup_google_drive(auth_callback):
            messagebox.showerror(
                ("خطأ"),
                ("فشل في الاتصال بـ Google Drive")
            )
        else:
            self.backup_to_google_drive()

    def backup_to_google_drive(self):
        """Perform the actual backup to Google Drive."""
        progress_window = self.db_backup.show_backup_progress()

        def on_backup_complete(success, message):
            if progress_window and progress_window.winfo_exists():
                progress_window.destroy()
            
            if success:
                self.show_backup_result(success, message, progress_window)
            else:
                messagebox.showerror(
                    ("خطأ"),
                    (message)
                )

        def backup_thread():
            try:
                self.db_backup.backup_to_google_drive(
                    progress_callback=None,
                    completion_callback=on_backup_complete,
                    auth_callback=self.show_auth_window
                )
            except Exception as e:
                on_backup_complete(False, f"حدث خطأ أثناء النسخ الاحتياطي: {str(e)}")

        threading.Thread(target=backup_thread, daemon=True).start()

    def show_backup_result(self, success, message, progress_window):
        """Show backup result message."""
        if progress_window and progress_window.winfo_exists():
            progress_window.destroy()

        def show_message():
            if success:
                # Combine the messages and apply Arabic processing once
                full_message = f"""
{message}

تم حفظ البيانات بنجاح على Google Drive.
يمكنك الوصول إلى النسخة الاحتياطية في مجلد "Elnada_Backup" على حسابك.
"""
                processed_message = (full_message)
                messagebox.showinfo(
                    ("نجاح"),
                    processed_message
                )
            else:
                messagebox.showerror(
                    ("خطأ"),
                    (message)
                )

        self.after(0, show_message) 