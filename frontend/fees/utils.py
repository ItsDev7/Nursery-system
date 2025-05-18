"""
Utility functions for the fees management system.
"""
from tkinter import messagebox
from datetime import datetime

def validate_amount(amount_str: str) -> tuple[bool, float]:
    """
    Validate and convert amount string to float.
    
    Args:
        amount_str: String representation of the amount
        
    Returns:
        Tuple of (is_valid, amount)
    """
    if not amount_str:
        messagebox.showerror("Error", "Amount is required")
        return False, 0.0
        
    try:
        amount = float(amount_str)
        return True, amount
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number")
        return False, 0.0

def validate_description(description: str) -> bool:
    """
    Validate description is not empty.
    
    Args:
        description: Description text
        
    Returns:
        True if valid, False otherwise
    """
    if not description:
        messagebox.showerror("Error", "Description is required")
        return False
    return True

def get_current_date() -> str:
    """
    Get current date in YYYY-MM-DD format.
    
    Returns:
        Current date string
    """
    return datetime.now().strftime("%Y-%m-%d")

def confirm_delete(item_type: str) -> bool:
    """
    Show confirmation dialog for deletion.
    
    Args:
        item_type: Type of item being deleted (expense/income)
        
    Returns:
        True if confirmed, False otherwise
    """
    return messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete this {item_type}?"
    ) 