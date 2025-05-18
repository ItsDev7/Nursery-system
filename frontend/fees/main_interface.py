"""
Main interface for the fees management system.
"""
import customtkinter as ctk
from backend.database import get_summary
from .expense_section import ExpenseSection
from .income_section import IncomeSection

class FeesPage:
    """Main fees management page combining expenses and income sections."""
    
    def __init__(self, master, on_back=None):
        """
        Initialize the fees page.
        
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
        self.main_frame = ctk.CTkFrame(self.master, fg_color=("#F7F7F7", "#232323"))
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Back button
        if self.on_back:
            back_icon = ctk.CTkButton(
                self.main_frame,
                text="←",
                font=("Arial", 18, "bold"),
                width=40,
                height=40,
                fg_color="#ff3333",
                text_color="#000000",
                hover_color="#b71c1c",
                corner_radius=20,
                command=self.on_back
            )
            back_icon.grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=(0, 10))
            
        # Expense section
        self.expense_section = ExpenseSection(
            self.main_frame,
            self.update_summary
        )
        
        # Income section
        self.income_section = IncomeSection(
            self.main_frame,
            self.update_summary
        )
        
        # Summary section
        summary_frame = ctk.CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        summary_frame.grid(row=4, column=0, columnspan=3, pady=15)
        
        self.summary_label = ctk.CTkLabel(
            summary_frame,
            text="",
            font=("Arial", 17, "bold"),
            text_color=("#2D8CFF", "#4CAF50")
        )
        self.summary_label.pack(pady=5)
        
        # Configure grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        
        # Initial summary update
        self.update_summary()
        
    def update_summary(self):
        """Update the summary display with current totals."""
        summary = get_summary()
        self.summary_label.configure(
            text=f"Income: {summary['income']} | Expenses: {summary['expenses']} | Remaining: {summary['remaining']}"
        ) 