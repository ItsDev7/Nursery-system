"""
Income management section of the fees interface.
"""
import customtkinter as ctk
from backend.database import (
    add_income,
    get_all_income,
    delete_income,
    update_income
)
from .utils import validate_amount, validate_description, get_current_date, confirm_delete
from .popups import IncomeEditPopup

class IncomeSection:
    """Manages the income input and display section."""
    
    def __init__(self, master, on_update_summary):
        """
        Initialize the income section.
        
        Args:
            master: Parent widget
            on_update_summary: Callback to update summary after changes
        """
        self.master = master
        self.on_update_summary = on_update_summary
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the income section UI."""
        # Input Frame
        self.input_frame = ctk.CTkFrame(self.master, fg_color=("#F7F7F7", "#232323"))
        self.input_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=10, padx=10)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(2, weight=1)
        
        # Description
        ctk.CTkLabel(
            self.input_frame,
            text="Income Description:",
            font=("Arial", 15, "bold"),
            anchor="e",
            justify="right"
        ).grid(row=0, column=2, sticky="e", padx=10, pady=(0, 5))
        
        self.description_entry = ctk.CTkTextbox(
            self.input_frame,
            height=60,
            width=400,
            font=("Arial", 14),
            fg_color=("#FFFFFF", "#404040"),
            border_width=1,
            wrap="word"
        )
        self.description_entry.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5, padx=10)
        self.description_entry._textbox.tag_configure("right", justify="right")
        self.description_entry._textbox.tag_add("right", "1.0", "end")
        
        # Amount
        ctk.CTkLabel(
            self.input_frame,
            text="Amount:",
            font=("Arial", 15, "bold"),
            anchor="e",
            justify="right"
        ).grid(row=2, column=2, sticky="e", padx=10, pady=(10, 5))
        
        self.amount_entry = ctk.CTkEntry(
            self.input_frame,
            font=("Arial", 14),
            width=180,
            fg_color=("#FFFFFF", "#404040"),
            border_width=1,
            justify="right"
        )
        self.amount_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=10)
        
        # Add Button
        ctk.CTkButton(
            self.input_frame,
            text="Add Income",
            font=("Arial", 15, "bold"),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            height=40,
            width=150,
            corner_radius=8,
            command=self.add_income
        ).grid(row=2, column=0, padx=10, sticky="w")
        
        # Income Table
        self.income_frame = ctk.CTkScrollableFrame(
            self.master,
            width=900,
            height=220,
            fg_color=("#F7F7F7", "#232323")
        )
        self.income_frame.grid(row=1, column=0, columnspan=3, pady=15, sticky="nsew", padx=10)
        self.income_frame.grid_columnconfigure(0, weight=1)
        self.income_frame.grid_columnconfigure(1, weight=1)
        self.income_frame.grid_columnconfigure(2, weight=2)
        self.income_frame.grid_columnconfigure(3, weight=1)
        
        self.load_income()
        
    def add_income(self):
        """Handle adding a new income entry."""
        description = self.description_entry.get("0.0", "end").strip()
        amount_str = self.amount_entry.get().strip()
        
        if not validate_description(description):
            return
            
        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            return
            
        date = get_current_date()
        add_income(description, amount, date)
        
        self.description_entry.delete("0.0", "end")
        self.amount_entry.delete(0, "end")
        self.load_income()
        self.on_update_summary()
        
    def load_income(self):
        """Load and display income entries."""
        for widget in self.income_frame.winfo_children():
            widget.destroy()
            
        transactions = get_all_income()
        
        # Headers
        headers = ["Actions", "Date", "Description", "Amount"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                self.income_frame,
                text=h,
                font=("Arial", 15, "bold"),
                text_color=("#FFFFFF", "#232323"),
                corner_radius=8,
                fg_color=("#4CAF50", "#2D8CFF"),
                height=40,
                width=120,
                anchor="center",
                justify="center"
            ).grid(row=0, column=i, padx=4, pady=4, sticky="ew")
            
        # Transactions
        for row_index, (income_id, desc, amount, date) in enumerate(transactions, start=1):
            delete_button = ctk.CTkButton(
                self.income_frame,
                text="✖",
                width=30,
                height=30,
                fg_color="red",
                text_color="white",
                command=lambda iid=income_id: self.confirm_delete_income(iid)
            )
            delete_button.grid(row=row_index, column=0, padx=4, pady=4, sticky="ew")
            
            ctk.CTkLabel(
                self.income_frame,
                text=date,
                font=("Arial", 13),
                anchor="e",
                justify="right"
            ).grid(row=row_index, column=1, sticky="ew", padx=4, pady=4)
            
            desc_label = ctk.CTkLabel(
                self.income_frame,
                text=desc[:50] + ("..." if len(desc) > 50 else ""),
                font=("Arial", 13),
                cursor="hand2",
                anchor="e",
                justify="right"
            )
            desc_label.grid(row=row_index, column=2, sticky="ew", padx=4, pady=4)
            desc_label.bind(
                "<Button-1>",
                lambda e, d=desc, a=amount, dt=date, iid=income_id: self.show_edit_popup(d, a, dt, iid)
            )
            
            ctk.CTkLabel(
                self.income_frame,
                text=amount,
                font=("Arial", 13),
                anchor="e",
                justify="right"
            ).grid(row=row_index, column=3, sticky="ew", padx=4, pady=4)
            
    def show_edit_popup(self, description, amount, date, income_id):
        """Show popup for editing an income entry."""
        IncomeEditPopup(
            self.master,
            description,
            amount,
            date,
            income_id,
            self.update_income
        )
        
    def update_income(self, income_id, new_desc, new_amount, new_date):
        """Update an income entry in the database."""
        update_income(income_id, new_desc, new_amount, new_date)
        self.load_income()
        self.on_update_summary()
        
    def confirm_delete_income(self, income_id):
        """Confirm and handle income deletion."""
        if confirm_delete("income"):
            delete_income(income_id)
            self.load_income()
            self.on_update_summary() 