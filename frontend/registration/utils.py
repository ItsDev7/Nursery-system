"""
Utility functions for the registration system.
"""
from tkinter import messagebox
from typing import List, Tuple

def validate_required_fields(name: str, nid: str, phone1: str, phone2: str) -> bool:
    """
    Validate required fields for registration.
    
    Args:
        name: Person's name
        nid: National ID
        phone1: Primary phone number
        phone2: Secondary phone number
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    if not name or not nid or (not phone1 and not phone2):
        messagebox.showerror("Error", "الاسم والرقم القومي ورقم هاتف واحد على الأقل مطلوب")
        return False
    return True

def clear_entry(entry, placeholder: str):
    """
    Clear an entry widget and set its placeholder.
    
    Args:
        entry: Entry widget to clear
        placeholder: Placeholder text to set
    """
    entry.delete(0, "end")
    entry.configure(placeholder_text=placeholder)

def clear_fee_entries(entries: List, date_widgets: List[Tuple]):
    """
    Clear all fee entries and their date widgets.
    
    Args:
        entries: List of fee entry widgets
        date_widgets: List of date widget tuples (day, month, year)
    """
    for entry in entries:
        entry.delete(0, "end")
        
    for date_widgets_tuple in date_widgets:
        for widget in date_widgets_tuple:
            widget.delete(0, "end")
            if widget == date_widgets_tuple[0]:
                widget.configure(placeholder_text="يوم")
            elif widget == date_widgets_tuple[1]:
                widget.configure(placeholder_text="شهر")
            elif widget == date_widgets_tuple[2]:
                widget.configure(placeholder_text="سنة")

def get_fee_dates(date_widgets: List[Tuple]) -> List[str]:
    """
    Extract dates from fee date widgets.
    
    Args:
        date_widgets: List of date widget tuples (day, month, year)
        
    Returns:
        List of date strings in DD/MM/YYYY format
    """
    return [
        f"{day.get().strip()}/{month.get().strip()}/{year.get().strip()}"
        for day, month, year in date_widgets
    ] 