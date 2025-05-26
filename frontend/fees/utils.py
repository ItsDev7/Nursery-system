"""Utility functions for the fees management section."""
from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk

def validate_amount(amount_str: str) -> tuple[bool, float]:
    """Validates if a string can be converted to a float and returns the result.

    Args:
        amount_str: The string to validate.

    Returns:
        A tuple containing a boolean (True if valid, False otherwise) and the
        converted float amount (or 0.0 if invalid).
    """
    try:
        amount = float(amount_str)
        return True, amount
    except ValueError:
        return False, 0

def validate_date(date_str: str) -> bool:
    """Validates if a string matches the date format DD-MM-YYYY.

    Args:
        date_str: The date string to validate.

    Returns:
        True if the date string is valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def show_error_message(message: str, parent=None):
    """Displays an error message box.

    Args:
        message: The error message to display.
        parent: The parent window for the message box (optional).
    """
    messagebox.showerror("Error", message, parent=parent)

def show_confirmation_message(message: str, parent=None) -> bool:
    """Displays a confirmation message box and returns the user's choice.

    Args:
        message: The confirmation message to display.
        parent: The parent window for the message box (optional).

    Returns:
        True if the user clicks 'Yes', False if the user clicks 'No'.
    """
    return messagebox.askyesno("Confirmation", message, parent=parent)

def create_description_window(parent, title: str, description: str, amount: float, date: str, 
                            on_save=None, on_cancel=None):
    """Creates and displays a reusable Toplevel window for viewing/editing details.

    This window is used to show the full description, amount, and date of
    an expense or income record. It can optionally include Save and Cancel buttons.

    Args:
        parent: The parent widget (usually the main application window or frame).
        title: The title for the new window.
        description: The description text to display.
        amount: The amount to display.
        date: The date string to display.
        on_save: Callback function for the Save button (optional).
        on_cancel: Callback function for the Cancel button (optional).

    Returns:
        A tuple containing the created window object and its main frame, description
        textbox, date label, and amount label.
    """
    # Create the top-level window
    window = ctk.CTkToplevel(parent)
    window.title(title)
    window.geometry("500x420")
    window.resizable(False, False)
    
    # Make the popup transient relative to the parent window
    window.transient(parent)
    # Grab focus to make the popup modal
    window.grab_set()

    # Create the main frame inside the window
    frame = ctk.CTkFrame(window)
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Display fields (Date, Amount, Description)
    # Date label
    date_label = ctk.CTkLabel(frame, text=f"التاريخ: {date}", font=("Arial", 13, "bold"), anchor="e", justify="right")
    date_label.pack(fill="x", pady=(0, 5))
    
    # Amount label
    amount_label = ctk.CTkLabel(frame, text=f"المبلغ: {amount}", font=("Arial", 13, "bold"), anchor="e", justify="right")
    amount_label.pack(fill="x", pady=(0, 10))
    
    # Description textbox (initially disabled for viewing)
    desc_box = ctk.CTkTextbox(frame, font=("Arial", 14), height=180, wrap="word")
    desc_box.pack(fill="both", expand=True, pady=10)
    # Insert description and configure for RTL display
    desc_box.insert("1.0", description)
    desc_box.configure(state="disabled") # Make it read-only initially
    desc_box._textbox.tag_configure("right", justify="right")
    desc_box._textbox.tag_add("right", "1.0", "end")
    
    # Buttons frame
    btns_frame = ctk.CTkFrame(frame)
    btns_frame.pack(pady=10)
    
    # Save button (optional)
    if on_save:
        save_btn = ctk.CTkButton(
            btns_frame,
            text="حفظ",
            fg_color="#4CAF50", # Green color
            text_color="#fff",
            hover_color="#388E3C",
            font=("Arial", 14, "bold"),
            command=lambda: on_save(window)
        )
        # Pack to the right side of the buttons frame
        save_btn.pack(side="right", padx=10)
    
    # Cancel button (optional)
    if on_cancel:
        cancel_btn = ctk.CTkButton(
            btns_frame,
            text="إلغاء",
            fg_color="#ff3333", # Red color
            text_color="#fff",
            hover_color="#b71c1c",
            font=("Arial", 14, "bold"),
            command=lambda: on_cancel(window)
        )
        # Pack to the right side of the buttons frame
        cancel_btn.pack(side="right", padx=10)
    
    # Protocol to handle closing the window (e.g., clicking the X button)
    window.protocol("WM_DELETE_WINDOW", lambda: on_cancel(window) if on_cancel else window.destroy())
    
    # Bring window to front and set focus
    window.lift()
    window.grab_set()
    
    # Return key widgets for potential further manipulation (e.g., enabling editing)
    return window, frame, desc_box, date_label, amount_label 