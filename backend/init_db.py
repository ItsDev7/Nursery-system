
# Import necessary table creation functions from the database module
from .database import (
    create_students_table,
    create_general_expenses_table,
    create_teachers_table,
    create_teacher_salaries_table,
    create_income_table,
    create_activities_table,
    create_settings_table
)

def init_database():
    """Initializes all required database tables for the application."""
    # Create all necessary tables
    create_students_table()
    create_general_expenses_table()
    create_teachers_table()
    create_teacher_salaries_table()
    create_income_table()
    create_activities_table()
    create_settings_table()

    # Optional: Print a success message (can be removed in production)
    # print("Database initialized successfully")