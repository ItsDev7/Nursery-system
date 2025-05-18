"""
Teacher registration page - Main entry point for teacher registration.
This file serves as a bridge between the main application and the registration package.
"""
from .registration.teacher_form import TeacherRegistrationForm

# For backward compatibility, alias the new class name to the old one
RegisterTeacherPage = TeacherRegistrationForm

# Re-export the class for backward compatibility
__all__ = ['RegisterTeacherPage']
