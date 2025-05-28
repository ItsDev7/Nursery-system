"""
Database backup module for Elnada Kindergarten Management System.
This module handles database backup operations including local and Google Drive backups.
"""

import os
import shutil
import customtkinter
from customtkinter import CTkProgressBar, CTkLabel
from datetime import datetime, timedelta, timezone
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
from backend import database

class DatabaseBackup:
    """
    Handles database backup operations including local and Google Drive backups.
    
    Attributes:
        parent_frame: The parent frame for UI elements
        db_file: Name of the database file
        progress_window: Window showing backup progress
        progress_bar: Progress bar widget
        last_backup_time: Timestamp of last backup
        backup_interval: Time interval between automatic backups
        SCOPES: Google Drive API scopes
        creds: Google Drive credentials
        drive_service: Google Drive service instance
        drive_folder_name: Name of the backup folder in Google Drive
        auth_callback: Callback function for authentication
    """
    
    def __init__(self, parent_frame):
        """Initialize DatabaseBackup with default settings."""
        self.parent_frame = parent_frame
        self.db_file = "students.db"
        self.progress_window = None
        self.progress_bar = None
        self.last_backup_time = None
        self.backup_interval = timedelta(hours=24)
        
        # Google Drive settings
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.creds = None
        self.drive_service = None
        self.drive_folder_name = "Elnada_Backup"
        self.auth_callback = None

    def create_backup_folder(self, backup_path):
        """Create backup folder if it doesn't exist."""
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

    def backup_database(self, backup_path, progress_callback=None, completion_callback=None, is_automatic=False):
        """
        Backup the database file to the specified location.
        
        Args:
            backup_path: Path where backup should be saved
            progress_callback: Function to update progress
            completion_callback: Function to call when backup is complete
            is_automatic: Whether this is an automatic backup
        """
        try:
            self.create_backup_folder(backup_path)
            source_path = os.path.join(os.getcwd(), self.db_file)
            destination_path = os.path.join(backup_path, self.db_file)
            
            if os.path.exists(destination_path):
                os.remove(destination_path)
                
            shutil.copy2(source_path, destination_path)
            self.last_backup_time = datetime.now()
            self.save_last_backup_time(backup_path)
            
            if completion_callback and not is_automatic:
                completion_callback(True, "تم حفظ البيانات محلياً بنجاح")
        except Exception as e:
            if completion_callback and not is_automatic:
                completion_callback(False, f"حدث خطأ أثناء حفظ البيانات محلياً: {str(e)}")

    def setup_google_drive(self, auth_callback=None):
        """
        Set up Google Drive authentication using OOB flow.
        
        Args:
            auth_callback: Callback function to handle auth URL and verification code
        """
        self.auth_callback = auth_callback
        creds = None
        
        # Determine base path for resources (credentials.json, token.pickle)
        # Use sys._MEIPASS when running as a PyInstaller bundle (one-file mode)
        # Otherwise, use the current working directory
        import sys
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
        else:
            # Running as a script
            base_path = os.getcwd()

        credentials_path = os.path.join(base_path, 'credentials.json')
        
        # Token pickle should be stored in a writable location, e.g., next to the executable
        # or in a user data directory. For simplicity, let's try next to the executable first.
        # In one-file mode, os.path.dirname(sys.executable) is the dir of the exe.
        if getattr(sys, 'frozen', False):
            token_dir = os.path.join(os.path.dirname(sys.executable), "Elnada_Backup_Tokens")
        else:
            token_dir = os.path.join(os.getcwd(), "Elnada_Backup_Tokens")

        if not os.path.exists(token_dir):
            os.makedirs(token_dir)
            
        token_path = os.path.join(token_dir, 'token.pickle')

        if os.path.exists(token_path):
            try:
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
            except Exception:
                creds = None
                
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    creds = None
            else:
                try:
                    if not os.path.exists(credentials_path):
                        # This error indicates credentials.json was not bundled correctly
                        print(f"Error: credentials.json not found at {credentials_path}")
                        return False

                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, 
                        self.SCOPES,
                        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
                    )
                    
                    auth_url, _ = flow.authorization_url(
                        access_type='offline',
                        include_granted_scopes='true',
                        prompt='consent'
                    )
                    
                    if self.auth_callback:
                        self.auth_callback(auth_url)
                    
                    return True
                    
                except Exception:
                    return False
                
            if creds:
                try:
                    with open(token_path, 'wb') as token:
                        pickle.dump(creds, token)
                except Exception:
                    pass
        
        self.creds = creds
        if creds:
            try:
                self.drive_service = build('drive', 'v3', credentials=creds)
                return True
            except Exception:
                return False
        return False

    def complete_google_drive_auth(self, verification_code):
        """
        Complete Google Drive authentication using the verification code.
        
        Args:
            verification_code: The verification code from the OOB flow
        """
        try:
            import sys
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.getcwd()
                
            credentials_path = os.path.join(base_path, 'credentials.json')

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, 
                self.SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            
            flow.fetch_token(code=verification_code)
            creds = flow.credentials
            
            # Token pickle should be stored in a writable location
            if getattr(sys, 'frozen', False):
                token_dir = os.path.join(os.path.dirname(sys.executable), "Elnada_Backup_Tokens")
            else:
                token_dir = os.path.join(os.getcwd(), "Elnada_Backup_Tokens")

            if not os.path.exists(token_dir):
                os.makedirs(token_dir)
                
            token_path = os.path.join(token_dir, 'token.pickle')

            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            
            self.creds = creds
            self.drive_service = build('drive', 'v3', credentials=creds)
            return True
            
        except Exception:
            return False

    def backup_to_google_drive(self, progress_callback=None, completion_callback=None, auth_callback=None):
        """
        Backup database to Google Drive.
        
        Args:
            progress_callback: Function to update progress
            completion_callback: Function to call when backup is complete
            auth_callback: Callback function for authentication
        """
        try:
            if not self.drive_service:
                if not self.setup_google_drive(auth_callback):
                    if completion_callback:
                        completion_callback(False, "فشل الاتصال بـ Google Drive")
                    return

            folder_id = self._get_or_create_folder(self.drive_folder_name)
            
            if not folder_id:
                if completion_callback:
                    completion_callback(False, "فشل إنشاء أو العثور على مجلد النسخ الاحتياطي على Google Drive")
                return

            file_metadata = {
                'name': f'students_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db',
                'parents': [folder_id]
            }
            
            database_file_path = os.path.join(os.getcwd(), self.db_file)

            if not os.path.exists(database_file_path):
                if completion_callback:
                    completion_callback(False, f"ملف قاعدة البيانات غير موجود: {self.db_file}")
                return

            media = MediaFileUpload(
                database_file_path,
                mimetype='application/octet-stream',
                resumable=True
            )
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, modifiedTime'
            ).execute()
            
            self.cleanup_google_drive_backups()

            if completion_callback:
                completion_callback(True, "تم حفظ البيانات على Google Drive بنجاح")
                
        except Exception as e:
            if completion_callback:
                completion_callback(False, f"حدث خطأ أثناء حفظ البيانات على Google Drive: {str(e)}")
            raise

    def cleanup_google_drive_backups(self):
        """Cleanup old backups from Google Drive."""
        try:
            if not self.drive_service:
                return

            folder_id = self._get_or_create_folder(self.drive_folder_name)
            if not folder_id:
                return

            results = self.drive_service.files().list(
                q=f"'{folder_id}' in parents and name contains 'students_backup_' and mimeType='application/octet-stream'",
                spaces='drive',
                fields='files(id, name, modifiedTime)'
            ).execute()
            
            items = results.get('files', [])
            
            if not items:
                return

            items.sort(key=lambda x: datetime.fromisoformat(x['modifiedTime'].replace('Z', '+00:00')), reverse=True)
            files_to_delete = []
            
            if len(items) > 3:
                files_to_delete.extend(items[3:])

            one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
            
            for item in items:
                if item not in files_to_delete:
                    modified_time = datetime.fromisoformat(item['modifiedTime'].replace('Z', '+00:00'))
                    if modified_time < one_month_ago:
                        files_to_delete.append(item)

            unique_files_to_delete = {}
            for file in files_to_delete:
                unique_files_to_delete[file['id']] = file

            files_to_delete = list(unique_files_to_delete.values())
            
            if not files_to_delete:
                return

            for file in files_to_delete:
                try:
                    self.drive_service.files().delete(fileId=file['id']).execute()
                except Exception:
                    pass

        except Exception:
            pass

    def _get_or_create_folder(self, folder_name):
        """
        Get or create a folder in Google Drive.
        
        Args:
            folder_name: Name of the folder to get or create
        """
        try:
            results = self.drive_service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            items = results.get('files', [])
            
            if items:
                return items[0]['id']
                
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            return folder.get('id')
        except Exception:
            return None

    def show_backup_progress(self):
        """Show progress bar and status during backup."""
        self.progress_window = customtkinter.CTkToplevel(self.parent_frame)
        self.progress_window.title("حفظ البيانات")
        self.progress_window.geometry("400x150")
        self.progress_window.transient(self.parent_frame)
        self.progress_window.grab_set()
        
        self.progress_window.update_idletasks()
        width = self.progress_window.winfo_width()
        height = self.progress_window.winfo_height()
        x = (self.progress_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.progress_window.winfo_screenheight() // 2) - (height // 2)
        self.progress_window.geometry(f'{width}x{height}+{x}+{y}')
        
        self.progress_bar = CTkProgressBar(self.progress_window)
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        self.progress_bar.set(0)
        
        status_label = CTkLabel(
            self.progress_window,
            text="جاري حفظ البيانات...",
            font=("Arial", 14)
        )
        status_label.pack(pady=10)
        
        self.progress_window.after(100, self.update_progress)
        
        return self.progress_window

    def update_progress(self):
        """Update progress bar in the main thread."""
        if self.progress_window and self.progress_bar:
            current = self.progress_bar.get()
            if current < 1.0:
                self.progress_bar.set(current + 0.1)
                self.progress_window.after(100, self.update_progress)
            else:
                self.progress_window.destroy()

    def check_and_backup(self):
        """Check if automatic backup is needed and perform it if necessary."""
        current_time = datetime.now()
        last_backup_file = os.path.join(os.getcwd(), "Elnada_Backup", "last_backup.txt")

        last_backup_time = None
        if os.path.exists(last_backup_file):
            try:
                with open(last_backup_file, 'r') as f:
                    timestamp = f.read().strip()
                    last_backup_time = datetime.fromisoformat(timestamp)
            except Exception:
                last_backup_time = None

        if (last_backup_time is None or
            current_time - last_backup_time >= self.backup_interval):
            
            saved_path = database.get_setting('local_backup_path')

            if saved_path:
                self.backup_database(saved_path, is_automatic=True)
                self.save_last_backup_time(os.path.join(os.getcwd(), "Elnada_Backup", "last_backup.txt"))

        self.parent_frame.after(3600000, self.check_and_backup)

    def start_automatic_backup(self):
        """Start the automatic backup system."""
        self.check_and_backup()

    def save_last_backup_time(self, file_path=None):
        """
        Save the last backup time to a file.
        
        Args:
            file_path: Path to save the backup time to
        """
        backup_dir_for_time_file = os.path.join(os.getcwd(), "Elnada_Backup")
        if not os.path.exists(backup_dir_for_time_file):
            os.makedirs(backup_dir_for_time_file)

        time_file_path = file_path if file_path else os.path.join(backup_dir_for_time_file, "last_backup.txt")

        if self.last_backup_time:
            try:
                with open(time_file_path, 'w') as f:
                    f.write(self.last_backup_time.isoformat())
            except Exception:
                pass 