"""
Database backup module for Elnada Kindergarten Management System.
This module handles database backup operations.
"""

import os
import shutil
import customtkinter
from customtkinter import CTkProgressBar, CTkLabel, CTkButton
import threading
import time
from datetime import datetime, timedelta, timezone
import webbrowser
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

class DatabaseBackup:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.backup_path = "C:/Elnada_Backup"
        self.db_file = "students.db"
        self.progress_window = None
        self.progress_bar = None
        self.last_backup_time = None
        self.backup_interval = timedelta(hours=24)  # Backup every 24 hours
        
        # Google Drive settings
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.creds = None
        self.drive_service = None
        self.drive_folder_name = "Elnada_Backup"
        
    def create_backup_folder(self):
        """Create backup folder if it doesn't exist."""
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)
            
    def backup_database(self, progress_callback=None, completion_callback=None, is_automatic=False):
        """
        Backup the database file to the specified location.
        
        Args:
            progress_callback: Function to update progress bar
            completion_callback: Function to call when backup is complete
            is_automatic: Whether this is an automatic backup
        """
        try:
            self.create_backup_folder()
            source_path = os.path.join(os.getcwd(), self.db_file)
            destination_path = os.path.join(self.backup_path, self.db_file)
            
            # If file exists, remove it first
            if os.path.exists(destination_path):
                os.remove(destination_path)
                
            # Copy the file
            shutil.copy2(source_path, destination_path)
            
            # Update last backup time
            self.last_backup_time = datetime.now()
            self.save_last_backup_time()
            
            if completion_callback and not is_automatic:
                completion_callback(True, "تم حفظ البيانات محلياً بنجاح")
        except Exception as e:
            if completion_callback and not is_automatic:
                completion_callback(False, f"حدث خطأ أثناء حفظ البيانات محلياً: {str(e)}")

    def setup_google_drive(self):
        """Set up Google Drive authentication."""
        creds = None
        token_path = os.path.join(self.backup_path, 'token.pickle')
        
        # Load existing credentials if available
        if os.path.exists(token_path):
            try:
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
            except Exception as e:
                print(f"Error loading token.pickle: {e}")
                creds = None
                
        # If credentials are not valid or don't exist, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None
            else:
                # Open browser for user authentication
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error getting new token: {e}")
                    # In a real app, you might want to inform the user here
                    return False # Indicate failure to set up
                
            # Save credentials for future use
            if creds:
                try:
                    with open(token_path, 'wb') as token:
                        pickle.dump(creds, token)
                except Exception as e:
                    print(f"Error saving token.pickle: {e}")
        
        self.creds = creds
        if creds:
            try:
                self.drive_service = build('drive', 'v3', credentials=creds)
                return True # Indicate success
            except Exception as e:
                print(f"Error building drive service: {e}")
                return False # Indicate failure
        return False # Indicate failure if creds are None

    def backup_to_google_drive(self, progress_callback=None, completion_callback=None):
        """Backup database to Google Drive."""
        try:
            if not self.drive_service:
                if not self.setup_google_drive():
                    if completion_callback:
                        completion_callback(False, "فشل الاتصال بـ Google Drive")
                    return

            # Create folder if it doesn't exist
            folder_id = self._get_or_create_folder(self.drive_folder_name)
            
            if not folder_id:
                 if completion_callback:
                        completion_callback(False, "فشل إنشاء أو العثور على مجلد النسخ الاحتياطي على Google Drive")
                 return

            # Upload file
            file_metadata = {
                'name': f'students_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db',
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(
                os.path.join(os.getcwd(), self.db_file),
                mimetype='application/octet-stream',
                resumable=True
            )
            
            # Use MediaFileUpload with a progress callback if available, though not implemented here
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, modifiedTime' # Request modifiedTime field
            ).execute()
            
            print("Backup uploaded to Google Drive.")
            
            # Perform cleanup after successful upload
            self.cleanup_google_drive_backups()

            if completion_callback:
                completion_callback(True, "تم حفظ البيانات على Google Drive بنجاح")
                
        except Exception as e:
            print(f"Error during Google Drive backup: {e}")
            if completion_callback:
                completion_callback(False, f"حدث خطأ أثناء حفظ البيانات على Google Drive: {str(e)}")

    def cleanup_google_drive_backups(self):
        """Cleanup old backups from Google Drive."""
        try:
            if not self.drive_service:
                print("Drive service not available for cleanup.")
                return

            folder_id = self._get_or_create_folder(self.drive_folder_name)
            if not folder_id:
                print(f"Could not find or create folder {self.drive_folder_name} for cleanup.")
                return

            # List all backup files in the folder
            results = self.drive_service.files().list(
                q=f"'{folder_id}' in parents and name contains 'students_backup_' and mimeType='application/octet-stream'",
                spaces='drive',
                fields='files(id, name, modifiedTime)'
            ).execute()
            
            items = results.get('files', [])
            
            if not items:
                print("No backup files found for cleanup.")
                return

            # Sort files by modified time (newest first)
            items.sort(key=lambda x: datetime.fromisoformat(x['modifiedTime'].replace('Z', '+00:00')), reverse=True)

            files_to_delete = []
            
            # Rule 1: Keep last 3 backups
            if len(items) > 3:
                files_to_delete.extend(items[3:]) # Add files from index 3 onwards

            # Rule 2: Delete files older than 1 month
            # Calculate one month ago in UTC, consistent with Google Drive's modifiedTime
            one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
            
            for item in items:
                 # Check if the file is not already marked for deletion by Rule 1
                 if item not in files_to_delete:
                    # Ensure modified_time is timezone-aware
                    modified_time = datetime.fromisoformat(item['modifiedTime'].replace('Z', '+00:00'))
                    if modified_time < one_month_ago:
                         files_to_delete.append(item) # Mark for deletion

            # Remove duplicates based on file id
            unique_files_to_delete = {}
            for file in files_to_delete:
                unique_files_to_delete[file['id']] = file

            files_to_delete = list(unique_files_to_delete.values())
            
            if not files_to_delete:
                print("No old backup files to delete.")
                return

            print(f"Deleting {len(files_to_delete)} old backup files...")
            # Delete the identified files
            for file in files_to_delete:
                try:
                    self.drive_service.files().delete(fileId=file['id']).execute()
                    print(f"Deleted file: {file['name']}")
                except Exception as e:
                    print(f"Error deleting file {file['name']}: {e}")

        except Exception as e:
            print(f"Error during Google Drive cleanup: {e}")

    def _get_or_create_folder(self, folder_name):
        """Get or create a folder in Google Drive."""
        try:
            # Check if folder exists
            results = self.drive_service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            items = results.get('files', [])
            
            if items:
                print(f"Found folder: {items[0]['name']}")
                return items[0]['id']
                
            # Create folder if it doesn't exist
            print(f"Creating folder: {folder_name}")
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            print(f"Created folder with ID: {folder.get('id')}")
            return folder.get('id')
        except Exception as e:
            print(f"Error getting or creating folder {folder_name}: {e}")
            return None
                
    def show_backup_progress(self):
        """Show progress bar and status during backup."""
        # Create progress window
        self.progress_window = customtkinter.CTkToplevel(self.parent_frame)
        self.progress_window.title("حفظ البيانات")
        self.progress_window.geometry("400x150")
        self.progress_window.transient(self.parent_frame)
        self.progress_window.grab_set()
        
        # Center the window
        self.progress_window.update_idletasks()
        width = self.progress_window.winfo_width()
        height = self.progress_window.winfo_height()
        x = (self.progress_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.progress_window.winfo_screenheight() // 2) - (height // 2)
        self.progress_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Add progress bar
        self.progress_bar = CTkProgressBar(self.progress_window)
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        self.progress_bar.set(0)
        
        # Add status label
        status_label = CTkLabel(
            self.progress_window,
            text="جاري حفظ البيانات...",
            font=("Arial", 14)
        )
        status_label.pack(pady=10)
        
        # Start progress animation
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
        
        # Load last backup time from file if exists
        last_backup_file = os.path.join(self.backup_path, "last_backup.txt")
        if os.path.exists(last_backup_file):
            try:
                with open(last_backup_file, 'r') as f:
                    timestamp = f.read().strip()
                    self.last_backup_time = datetime.fromisoformat(timestamp)
            except:
                self.last_backup_time = None

        # Check if enough time has passed since the last backup
        if (self.last_backup_time is None or 
            current_time - self.last_backup_time >= self.backup_interval):
            
            # Perform automatic backup (local only as per previous logic)
            # For Google Drive automatic backup, more complex scheduling might be needed
            print("Performing automatic local backup...")
            self.backup_database(is_automatic=True)

        # Schedule next check
        # Note: This currently only schedules local backup check. 
        # For automatic Google Drive backup, a separate timer or logic might be better.
        self.parent_frame.after(3600000, self.check_and_backup)  # Check every hour

    def start_automatic_backup(self):
        """Start the automatic backup system."""
        # Start checking for local backups
        self.check_and_backup()
        # Note: Automatic Google Drive backup is not started here, as it might require user interaction for auth initially.

    def save_last_backup_time(self):
        """Save the last backup time to a file."""
        # Ensure backup directory exists before saving the file
        self.create_backup_folder()
        if self.last_backup_time:
            last_backup_file = os.path.join(self.backup_path, "last_backup.txt")
            try:
                with open(last_backup_file, 'w') as f:
                    f.write(self.last_backup_time.isoformat())
            except Exception as e:
                print(f"Error saving last backup time: {e}") 