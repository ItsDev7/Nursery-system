"""
Main registration interface that combines student and teacher registration forms.
"""
import customtkinter as ctk
from .student_form import StudentRegistrationForm
from .teacher_form import TeacherRegistrationForm

class RegistrationPage:
    """Main registration page that manages both student and teacher registration."""
    
    def __init__(self, master, on_back=None):
        """
        Initialize the registration page.
        
        Args:
            master: Parent window
            on_back: Callback for back button
        """
        self.master = master
        self.on_back = on_back
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the main UI components."""
        # Clear existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()
            
        # Main frame
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Registration",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.main_frame)
        buttons_frame.pack(pady=20)
        
        # Student registration button
        student_button = ctk.CTkButton(
            buttons_frame,
            text="Register Student",
            font=("Arial", 16, "bold"),
            width=200,
            height=40,
            command=self.show_student_form
        )
        student_button.pack(side="left", padx=10)
        
        # Teacher registration button
        teacher_button = ctk.CTkButton(
            buttons_frame,
            text="Register Teacher",
            font=("Arial", 16, "bold"),
            width=200,
            height=40,
            command=self.show_teacher_form
        )
        teacher_button.pack(side="left", padx=10)
        
        # Back button
        if self.on_back:
            back_button = ctk.CTkButton(
                self.main_frame,
                text="← Back",
                font=("Arial", 14),
                width=100,
                height=30,
                fg_color="#ff3333",
                hover_color="#b71c1c",
                command=self.on_back
            )
            back_button.pack(side="bottom", pady=20)
            
    def show_student_form(self):
        """Show the student registration form."""
        StudentRegistrationForm(self.master, self.setup_ui)
        
    def show_teacher_form(self):
        """Show the teacher registration form."""
        TeacherRegistrationForm(self.master, self.setup_ui) 