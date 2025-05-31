"""
Login module for Management System.
This module handles user authentication and login interface.
"""
# Standard library imports
from tkinter import messagebox

# Third-party imports
from customtkinter import CTkLabel, CTkEntry, CTkFrame, CTkButton
import arabic_reshaper
from bidi.algorithm import get_display

# Local application imports
from .index import NextPage

class Login:
    """
    Handles the user login interface and authentication logic.
    
    This class manages the login page UI, user input validation,
    and authentication process.
    """

    def __init__(self, main_window):
        """
        Initialize the login interface.

        Args:
            main_window: The main application window (CTk object)
        """
        self.main = main_window
        self.setup_ui()
        self._bind_enter_key()

    def _bind_enter_key(self):
        """Bind Enter key to appropriate actions."""
        # Bind Enter key to container for global login trigger
        self.container.bind('<Return>', self._handle_enter)
        
        # Bind Enter key to username field to move to password
        self.username_entry.bind('<Return>', self._handle_username_enter)
        
        # Bind Enter key to password field to trigger login
        self.password_entry.bind('<Return>', self._handle_password_enter)

    def _handle_enter(self, event):
        """Handle Enter key press in the container."""
        self.login_clicked()

    def _handle_username_enter(self, event):
        """Handle Enter key press in username field."""
        self.password_entry.focus()

    def _handle_password_enter(self, event):
        """Handle Enter key press in password field."""
        self.login_clicked()

    def arabic(self, text: str) -> str:
        """
        Format Arabic text for proper display.

        Args:
            text (str): The Arabic text to be displayed

        Returns:
            str: Properly formatted Arabic text
        """
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def setup_ui(self):
        """Set up the login page user interface."""
        self._clear_main_window()
        self._create_main_container()
        self._create_title()
        self._create_login_form()
        self._create_footer()

    def _clear_main_window(self):
        """Clear all existing widgets from the main window."""
        for widget in self.main.winfo_children():
            widget.destroy()

    def _create_main_container(self):
        """Create and configure the main container frame."""
        # Create main container with transparent background
        self.container = CTkFrame(self.main, fg_color=self.main.cget('fg_color'))
        self.container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Configure main window grid
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        # Configure container grid for vertical centering
        self.container.grid_rowconfigure(0, weight=1)  # Top spacing
        self.container.grid_rowconfigure(1, weight=0)  # Title
        self.container.grid_rowconfigure(2, weight=0)  # Form
        self.container.grid_rowconfigure(3, weight=1)  # Bottom spacing
        self.container.grid_rowconfigure(4, weight=0)  # Footer
        self.container.grid_columnconfigure(0, weight=1)  # Center content

    def _create_title(self):
        """Create the login page title."""
        title = CTkLabel(
            self.container,
            text=self.arabic("تسجيل الدخول"),
            font=("Arial Black", 36, "bold"),
            text_color="#1F6BB5"
        )
        title.grid(row=1, column=0, pady=(20, 40), sticky="n")

    def _create_login_form(self):
        """Create the login form with username and password fields."""
        # Create form container
        form_frame = CTkFrame(self.container, fg_color="transparent")
        form_frame.grid(row=2, column=0, sticky="nsew", padx=20)

        # Configure form grid
        self._configure_form_grid(form_frame)

        # Create form elements
        self._create_username_field(form_frame)
        self._create_password_field(form_frame)
        self._create_login_button(form_frame)

    def _configure_form_grid(self, form_frame):
        """Configure the grid layout for the form frame."""
        # Configure columns
        form_frame.grid_columnconfigure(0, weight=1)  # Input fields
        form_frame.grid_columnconfigure(1, weight=0)  # Labels
        form_frame.grid_columnconfigure(2, weight=1)  # Spacing

        # Configure rows
        form_frame.grid_rowconfigure(0, weight=0)  # Username
        form_frame.grid_rowconfigure(1, weight=0)  # Password
        form_frame.grid_rowconfigure(2, weight=0)  # Button

    def _create_username_field(self, parent):
        """Create the username input field and label."""
        # Username label
        username_label = CTkLabel(
            parent,
            text=self.arabic("اسم المستخدم:"),
            text_color="#333333",
            font=("Arial", 18, "bold"),
            anchor="e",
            justify="right"
        )
        username_label.grid(row=0, column=1, sticky="e", padx=(10, 0), pady=(5, 2))

        # Username entry
        self.username_entry = CTkEntry(
            parent,
            text_color="#333333",
            fg_color="#FFFFFF",
            border_color="#2D8CFF",
            font=("Arial", 18),
            width=300,
            corner_radius=8,
            border_width=2,
            height=45
        )
        self.username_entry.grid(row=0, column=0, sticky="ew", padx=(20, 10), pady=(5, 2))

    def _create_password_field(self, parent):
        """Create the password input field and label."""
        # Password label
        password_label = CTkLabel(
            parent,
            text=self.arabic("كلمة المرور:"),
            text_color="#333333",
            font=("Arial", 18, "bold"),
            anchor="e",
            justify="right"
        )
        password_label.grid(row=1, column=1, sticky="e", padx=(10, 0), pady=(10, 2))

        # Password entry
        self.password_entry = CTkEntry(
            parent,
            show="*",
            text_color="#333333",
            fg_color="#FFFFFF",
            border_color="#2D8CFF",
            font=("Arial", 18),
            width=300,
            corner_radius=8,
            border_width=2,
            height=45
        )
        self.password_entry.grid(row=1, column=0, sticky="ew", padx=(20, 10), pady=(10, 2))

    def _create_login_button(self, parent):
        """Create the login button."""
        login_button = CTkButton(
            parent,
            text=self.arabic("تسجيل الدخول"),
            font=("Arial", 20, "bold"),
            height=50,
            width=250,
            corner_radius=12,
            fg_color="#2D8CFF",
            hover_color="#1F6BB5",
            command=self.login_clicked
        )
        login_button.grid(row=2, column=0, columnspan=2, pady=(30, 20), padx=10)

    def _create_footer(self):
        """Create the footer with version and creator information."""
        footer_frame = CTkFrame(self.container, fg_color="transparent")
        footer_frame.grid(row=4, column=0, sticky="s", pady=(10, 20))

        # Creator label
        created_by_label = CTkLabel(
            footer_frame,
            text="Created by Osama",
            font=("Arial", 12),
            text_color="#888888"
        )
        created_by_label.pack()

        # Version label
        version_label = CTkLabel(
            footer_frame,
            text="Version 1.0.0",
            font=("Arial", 12),
            text_color="#888888"
        )
        version_label.pack()

    def login_clicked(self):
        """
        Handle the login button click event.
        
        Validates user credentials and proceeds to the main application
        if authentication is successful.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror(
                ("خطأ"),
                ("يرجى إدخال اسم المستخدم وكلمة المرور"),
                parent=self.main
            )
        elif username != "admin" or password != "admin123":
            messagebox.showerror(
                ("خطأ"),
                ("اسم المستخدم أو كلمة المرور غير صحيحة"),
                parent=self.main
            )
        else:
            # Successful login
            self.container.grid_forget()
            NextPage(self.main)
