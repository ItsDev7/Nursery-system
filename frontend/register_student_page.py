"""
Student registration page - Main entry point for student registration.
This file serves as a bridge between the main application and the registration package.
"""
from .registration.student_form import StudentRegistrationForm

# For backward compatibility, alias the new class name to the old one
RegisterStudentPage = StudentRegistrationForm

# Re-export the class for backward compatibility
__all__ = ['RegisterStudentPage']
