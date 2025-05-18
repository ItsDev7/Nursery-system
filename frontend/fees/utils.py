from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk

def validate_amount(amount_str: str) -> tuple[bool, float]:
    """Validate and convert amount string to float."""
    try:
        amount = float(amount_str)
        return True, amount
    except ValueError:
        return False, 0

def validate_date(date_str: str) -> bool:
    """Validate date format (DD-MM-YYYY)."""
    try:
        datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def show_error_message(message: str, parent=None):
    """Show error message box."""
    messagebox.showerror("خطأ", message, parent=parent)

def show_confirmation_message(message: str, parent=None) -> bool:
    """Show confirmation message box and return user's choice."""
    return messagebox.askyesno("تأكيد", message, parent=parent)

def create_description_window(parent, title: str, description: str, amount: float, date: str, 
                            on_save=None, on_cancel=None):
    """Create a reusable description window for both expenses and income."""
    window = ctk.CTkToplevel(parent)
    window.title(title)
    window.geometry("500x420")
    window.resizable(False, False)
    
    frame = ctk.CTkFrame(window)
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Display fields
    date_label = ctk.CTkLabel(frame, text=f"التاريخ: {date}", font=("Arial", 13, "bold"), anchor="e", justify="right")
    date_label.pack(fill="x", pady=(0, 5))
    
    amount_label = ctk.CTkLabel(frame, text=f"المبلغ: {amount}", font=("Arial", 13, "bold"), anchor="e", justify="right")
    amount_label.pack(fill="x", pady=(0, 10))
    
    desc_box = ctk.CTkTextbox(frame, font=("Arial", 14), height=180, wrap="word")
    desc_box.pack(fill="both", expand=True, pady=10)
    desc_box.insert("1.0", description)
    desc_box.configure(state="disabled")
    desc_box._textbox.tag_configure("right", justify="right")
    desc_box._textbox.tag_add("right", "1.0", "end")
    
    # Buttons
    btns_frame = ctk.CTkFrame(frame)
    btns_frame.pack(pady=10)
    
    if on_save:
        save_btn = ctk.CTkButton(
            btns_frame,
            text="حفظ",
            fg_color="#4CAF50",
            text_color="#fff",
            hover_color="#388E3C",
            font=("Arial", 14, "bold"),
            command=lambda: on_save(window)
        )
        save_btn.pack(side="right", padx=10)
    
    if on_cancel:
        cancel_btn = ctk.CTkButton(
            btns_frame,
            text="إلغاء",
            fg_color="#ff3333",
            text_color="#fff",
            hover_color="#b71c1c",
            font=("Arial", 14, "bold"),
            command=lambda: on_cancel(window)
        )
        cancel_btn.pack(side="right", padx=10)
    
    window.protocol("WM_DELETE_WINDOW", lambda: on_cancel(window) if on_cancel else window.destroy())
    window.lift()
    window.grab_set()
    
    return window, frame, desc_box, date_label, amount_label 