"""
Popup windows for editing expenses and income entries.
"""
import customtkinter as ctk
from .utils import validate_amount, validate_description

class EditPopup:
    """Base class for edit popups with common functionality."""
    
    def __init__(self, master, title, description, amount, date, on_save, on_cancel):
        """
        Initialize the edit popup.
        
        Args:
            master: Parent window
            title: Window title
            description: Initial description
            amount: Initial amount
            date: Initial date
            on_save: Callback for save action
            on_cancel: Callback for cancel action
        """
        self.window = ctk.CTkToplevel(master)
        self.window.title(title)
        self.window.geometry("500x420")
        self.window.resizable(False, False)
        
        self.frame = ctk.CTkFrame(self.window)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Variables
        self.desc_var = ctk.StringVar(value=description)
        self.amount_var = ctk.StringVar(value=str(amount))
        self.date_var = ctk.StringVar(value=date)
        
        # Callbacks
        self.on_save = on_save
        self.on_cancel = on_cancel
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the popup UI elements."""
        # Date
        self.date_entry = ctk.CTkEntry(
            self.frame,
            font=("Arial", 13),
            textvariable=self.date_var
        )
        self.date_entry.pack(fill="x", pady=(0, 5))
        
        # Amount
        self.amount_entry = ctk.CTkEntry(
            self.frame,
            font=("Arial", 13),
            textvariable=self.amount_var
        )
        self.amount_entry.pack(fill="x", pady=(0, 10))
        
        # Description
        self.desc_edit_box = ctk.CTkTextbox(
            self.frame,
            font=("Arial", 14),
            height=180,
            wrap="word"
        )
        self.desc_edit_box.pack(fill="both", expand=True, pady=10)
        self.desc_edit_box.insert("1.0", self.desc_var.get())
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.frame)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Save",
            fg_color="#4CAF50",
            text_color="#fff",
            hover_color="#388E3C",
            font=("Arial", 14, "bold"),
            command=self.save_edit
        ).pack(side="right", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="#ff3333",
            text_color="#fff",
            hover_color="#b71c1c",
            font=("Arial", 14, "bold"),
            command=self.on_cancel
        ).pack(side="right", padx=10)
        
    def save_edit(self):
        """Handle save action."""
        new_desc = self.desc_edit_box.get("1.0", "end").strip()
        new_amount = self.amount_entry.get().strip()
        new_date = self.date_entry.get().strip()
        
        if not validate_description(new_desc):
            return
            
        is_valid, amount = validate_amount(new_amount)
        if not is_valid:
            return
            
        if not new_date:
            ctk.messagebox.showerror("Error", "Date is required")
            return
            
        self.on_save(new_desc, amount, new_date)
        self.window.destroy()

class ExpenseEditPopup(EditPopup):
    """Popup for editing expense entries."""
    
    def __init__(self, master, description, amount, date, expense_id, on_save):
        super().__init__(
            master,
            "Edit Expense",
            description,
            amount,
            date,
            lambda d, a, dt: on_save(expense_id, d, a, dt),
            lambda: master.focus()
        )

class IncomeEditPopup(EditPopup):
    """Popup for editing income entries."""
    
    def __init__(self, master, description, amount, date, income_id, on_save):
        super().__init__(
            master,
            "Edit Income",
            description,
            amount,
            date,
            lambda d, a, dt: on_save(income_id, d, a, dt),
            lambda: master.focus()
        ) 