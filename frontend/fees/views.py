"""Fees management page view implementation.

This module implements the user interface for managing expenses and income,
including adding, editing, and deleting financial records.
"""
from customtkinter import *
from .controllers import FeesController
from .utils import create_description_window
from frontend.person_management.utils import DateEntry

class FeesPage:
    """Main fees management page class.
    
    This class handles the UI for managing expenses and income records,
    including displaying tables, handling user input, and managing the
    financial summary.
    """
    def __init__(self, master, on_back=None, on_data_changed=None, arabic_handler=None):
        """Initialize the fees page.
        
        Args:
            master: The parent widget
            on_back: Callback function for back button
            on_data_changed: Callback function when data changes
            arabic_handler: Function to handle Arabic text input
        """
        self.master = master
        self.on_back = on_back
        self.on_data_changed = on_data_changed
        self.controller = FeesController(self)
        self.arabic_handler = arabic_handler
        self.setup_ui()

    def setup_ui(self):
        """Set up the main UI components and layout."""
        # Clear existing widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Create main frame with light/dark mode support
        self.main_frame = CTkFrame(self.master, fg_color=("#F7F7F7", "#232323"))
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Configure grid weights for responsive layout
        self.main_frame.grid_columnconfigure(0, weight=0)  # Back button column
        self.main_frame.grid_columnconfigure(1, weight=1)  # Content columns
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Expense table row
        self.main_frame.grid_rowconfigure(3, weight=1)  # Income table row

        # Add back button if callback provided
        if self.on_back:
            back_icon = CTkButton(
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

        # Initialize all sections
        self.setup_expense_section()
        self.setup_income_section()
        self.setup_summary_section()

        # Load initial data
        self.load_expenses()
        self.load_income()

    def setup_expense_section(self):
        """Set up the expense input and display section.
        
        Creates the expense input form and table for displaying expenses.
        """
        # Create input frame for expense details
        input_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        input_frame.grid(row=0, column=1, columnspan=3, sticky="ew", pady=10, padx=10)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(2, weight=1)

        # Description input
        CTkLabel(input_frame, 
                text=":وصف المصروف", 
                font=("Arial", 15, "bold"),
                anchor="e", justify="right").grid(row=0, column=2, sticky="e", padx=10, pady=(0, 5))
        self.description_entry = CTkTextbox(input_frame, 
                                          height=60, 
                                          width=400,
                                          font=("Arial", 14),
                                          fg_color=("#FFFFFF", "#404040"),
                                          border_width=1,
                                          wrap="word")
        self.description_entry.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5, padx=10)
        self.description_entry._textbox.tag_configure("right", justify="right")
        self.description_entry._textbox.tag_add("right", "1.0", "end")

        # Amount input
        CTkLabel(input_frame, 
                text=":المبلغ", 
                font=("Arial", 15, "bold"), anchor="e", justify="right").grid(row=2, column=2, sticky="e", padx=10, pady=(10, 5))
        self.amount_entry = CTkEntry(input_frame, 
                                    font=("Arial", 14),
                                    width=180,
                                    fg_color=("#FFFFFF", "#404040"),
                                    border_width=1,
                                    justify="right")
        self.amount_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=10)

        # Add expense button
        CTkButton(input_frame, 
                 text="إضافة مصروف", 
                 font=("Arial", 15, "bold"),
                 fg_color="#2D8CFF",
                 hover_color="#1F6BB5",
                 height=40,
                 width=150,
                 corner_radius=8,
                 command=self.add_expense).grid(row=2, column=0, padx=10, sticky="w")

        # Create scrollable frame for expenses table
        self.expense_frame = CTkScrollableFrame(self.main_frame, width=900, height=220, fg_color=("#F7F7F7", "#232323"))
        self.expense_frame.grid(row=1, column=0, columnspan=4, pady=15, sticky="nsew", padx=10)
        self.expense_frame.grid_columnconfigure(0, weight=1)
        self.expense_frame.grid_columnconfigure(1, weight=1)
        self.expense_frame.grid_columnconfigure(2, weight=2)
        self.expense_frame.grid_columnconfigure(3, weight=1)

    def setup_income_section(self):
        """Set up the income input and display section.
        
        Creates the income input form and table for displaying income records.
        """
        # Create input frame for income details
        income_input_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        income_input_frame.grid(row=2, column=1, columnspan=3, sticky="ew", pady=10, padx=10)
        income_input_frame.grid_columnconfigure(0, weight=1)
        income_input_frame.grid_columnconfigure(1, weight=1)
        income_input_frame.grid_columnconfigure(2, weight=1)

        # Description input
        CTkLabel(income_input_frame, 
                text=":وصف الإيراد", 
                font=("Arial", 15, "bold"),
                anchor="e", justify="right").grid(row=0, column=2, sticky="e", padx=10, pady=(0, 5))
        self.income_description_entry = CTkTextbox(income_input_frame, 
                                          height=60, 
                                          width=400,
                                          font=("Arial", 14),
                                          fg_color=("#FFFFFF", "#404040"),
                                          border_width=1,
                                          wrap="word")
        self.income_description_entry.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5, padx=10)
        self.income_description_entry._textbox.tag_configure("right", justify="right")
        self.income_description_entry._textbox.tag_add("right", "1.0", "end")

        # Amount input
        CTkLabel(income_input_frame, 
                text=":المبلغ", 
                font=("Arial", 15, "bold"), anchor="e", justify="right").grid(row=2, column=2, sticky="e", padx=10, pady=(10, 5))
        self.income_amount_entry = CTkEntry(income_input_frame, 
                                    font=("Arial", 14),
                                    width=180,
                                    fg_color=("#FFFFFF", "#404040"),
                                    border_width=1,
                                    justify="right")
        self.income_amount_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=10)

        # Add income button
        CTkButton(income_input_frame, 
                 text="إضافة إيراد", 
                 font=("Arial", 15, "bold"),
                 fg_color="#4CAF50",
                 hover_color="#388E3C",
                 height=40,
                 width=150,
                 corner_radius=8,
                 command=self.add_income).grid(row=2, column=0, padx=10, sticky="w")

        # Create scrollable frame for income table
        self.income_frame = CTkScrollableFrame(self.main_frame, width=900, height=220, fg_color=("#F7F7F7", "#232323"))
        self.income_frame.grid(row=3, column=0, columnspan=4, pady=15, sticky="nsew", padx=10)
        self.income_frame.grid_columnconfigure(0, weight=1)
        self.income_frame.grid_columnconfigure(1, weight=1)
        self.income_frame.grid_columnconfigure(2, weight=2)
        self.income_frame.grid_columnconfigure(3, weight=1)

    def setup_summary_section(self):
        """Set up the financial summary section.
        
        Creates a frame to display total income, expenses, and remaining balance.
        """
        summary_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        summary_frame.grid(row=4, column=0, columnspan=4, pady=15)
        self.summary_label = CTkLabel(summary_frame, 
                                     text="", 
                                     font=("Arial", 17, "bold"),
                                     text_color=("#2D8CFF", "#4CAF50"))
        self.summary_label.pack(pady=5)

    def add_expense(self):
        """Handle adding a new expense record.
        
        Validates input and adds the expense to the database if valid.
        Updates the display and summary after successful addition.
        """
        description = self.description_entry.get("0.0", "end").strip()
        amount_str = self.amount_entry.get().strip()
        
        if self.controller.add_expense(description, amount_str):
            self.description_entry.delete("0.0", "end")
            self.amount_entry.delete(0, "end")
            self.load_expenses()
            self.update_summary()

    def add_income(self):
        """Handle adding a new income record.
        
        Validates input and adds the income to the database if valid.
        Updates the display and summary after successful addition.
        """
        description = self.income_description_entry.get("0.0", "end").strip()
        amount_str = self.income_amount_entry.get().strip()
        
        if self.controller.add_income(description, amount_str):
            self.income_description_entry.delete("0.0", "end")
            self.income_amount_entry.delete(0, "end")
            self.load_income()
            self.update_summary()

    def load_expenses(self):
        """Load and display all expense records in the table.
        
        Creates a table with headers and populates it with expense data.
        Each row includes delete button, date, description, and amount.
        """
        # Clear existing table contents
        for widget in self.expense_frame.winfo_children():
            widget.destroy()

        # Create table headers
        headers = ["الإجراءات", "التاريخ", "الوصف", "المبلغ"]
        for i, h in enumerate(headers):
            CTkLabel(self.expense_frame, 
                    text=h, 
                    font=("Arial", 15, "bold"),
                    text_color=("#FFFFFF", "#232323"),
                    corner_radius=8,
                    fg_color=("#2D8CFF", "#4CAF50"),
                    height=40,
                    width=120,
                    anchor="center", justify="center").grid(
                        row=0, column=i, padx=4, pady=4, sticky="ew")

        # Load and display expense records
        expenses = self.controller.get_all_expenses()
        for row_index, (expense_id, desc, amount, date) in enumerate(expenses, start=1):
            # Delete button
            delete_button = CTkButton(
                self.expense_frame,
                text="✖",
                width=30,
                height=30,
                fg_color="red",
                text_color="white",
                command=lambda eid=expense_id: self.confirm_delete_expense(eid)
            )
            delete_button.grid(row=row_index, column=0, padx=4, pady=4, sticky="ew")

            # Date column
            CTkLabel(self.expense_frame, text=date, font=("Arial", 13), anchor="e", justify="right").grid(
                row=row_index, column=1, sticky="ew", padx=4, pady=4)
            
            # Description column (clickable for full view)
            desc_label = CTkLabel(
                self.expense_frame,
                text=desc[:50] + ("..." if len(desc) > 50 else ""),
                font=("Arial", 13),
                cursor="hand2",
                anchor="e", justify="right"
            )
            desc_label.grid(row=row_index, column=2, sticky="ew", padx=4, pady=4)
            desc_label.bind("<Button-1>", lambda e, d=desc, a=amount, dt=date, eid=expense_id: 
                           self.show_full_description(d, a, dt, eid))

            # Amount column
            CTkLabel(self.expense_frame, text=amount, font=("Arial", 13), anchor="e", justify="right").grid(
                row=row_index, column=3, sticky="ew", padx=4, pady=4)

        self.update_summary()

    def load_income(self):
        """Load and display all income records in the table.
        
        Creates a table with headers and populates it with income data.
        Each row includes delete button, date, description, and amount.
        """
        # Clear existing table contents
        for widget in self.income_frame.winfo_children():
            widget.destroy()

        # Create table headers
        headers = ["الإجراءات", "التاريخ", "الوصف", "المبلغ"]
        for i, h in enumerate(headers):
            CTkLabel(self.income_frame, 
                    text=h, 
                    font=("Arial", 15, "bold"),
                    text_color=("#FFFFFF", "#232323"),
                    corner_radius=8,
                    fg_color=("#4CAF50", "#2D8CFF"),
                    height=40,
                    width=120,
                    anchor="center", justify="center").grid(
                        row=0, column=i, padx=4, pady=4, sticky="ew")

        # Load and display income records
        income_records = self.controller.get_all_income()
        for row_index, (income_id, desc, amount, date) in enumerate(income_records, start=1):
            # Delete button
            delete_button = CTkButton(
                self.income_frame,
                text="✖",
                width=30,
                height=30,
                fg_color="red",
                text_color="white",
                command=lambda iid=income_id: self.confirm_delete_income(iid)
            )
            delete_button.grid(row=row_index, column=0, padx=4, pady=4, sticky="ew")

            # Date column
            CTkLabel(self.income_frame, text=date, font=("Arial", 13), anchor="e", justify="right").grid(
                row=row_index, column=1, sticky="ew", padx=4, pady=4)
            
            # Description column (clickable for full view)
            desc_label = CTkLabel(
                self.income_frame,
                text=desc[:50] + ("..." if len(desc) > 50 else ""),
                font=("Arial", 13),
                cursor="hand2",
                anchor="e", justify="right"
            )
            desc_label.grid(row=row_index, column=2, sticky="ew", padx=4, pady=4)
            desc_label.bind("<Button-1>", lambda e, d=desc, a=amount, dt=date, iid=income_id: 
                           self.show_full_income_description(d, a, dt, iid))

            # Amount column
            CTkLabel(self.income_frame, text=amount, font=("Arial", 13), anchor="e", justify="right").grid(
                row=row_index, column=3, sticky="ew", padx=4, pady=4)

        self.update_summary()

    def update_summary(self):
        """Update the financial summary display with current totals."""
        summary = self.controller.get_summary()
        self.summary_label.configure(
            text=f"الإيرادات: {summary['income']} | المصروفات: {summary['expenses']} | المتبقي: {summary['remaining']}"
        )

    def show_full_description(self, description, amount, date, expense_id=None):
        """Show full expense description in a popup window with edit capability.
        
        Args:
            description: The expense description
            amount: The expense amount
            date: The expense date
            expense_id: The ID of the expense record
        """
        def on_save(window, desc_edit_box_widget, amount_entry_widget, date_entry_widget):
            """Handle saving edited expense details."""
            new_desc = desc_edit_box_widget.get("1.0", "end").strip()
            new_amount = amount_entry_widget.get().strip()
            new_date = date_entry_widget.get_date()

            if self.controller.update_expense(expense_id, new_desc, new_amount, new_date):
                window.destroy()
                self.load_expenses()
                self.load_income()

        def on_cancel(window):
            """Handle canceling the edit operation."""
            window.destroy()

        # Create the description window
        window, frame, desc_box, date_label, amount_label = create_description_window(
            self.master,
            "تفاصيل الوصف",
            description,
            amount,
            date,
            on_save=lambda: None,  # Dummy command for initial button creation
            on_cancel=on_cancel
        )

        # Get button references
        btns_frame = None
        for child in reversed(frame.winfo_children()):
            if isinstance(child, CTkFrame):
                btns_frame = child
                break

        cancel_btn = None
        save_btn = None

        if btns_frame:
            for btn in btns_frame.winfo_children():
                if isinstance(btn, CTkButton):
                    if btn.cget("text") == "إلغاء":
                        cancel_btn = btn
                    elif btn.cget("text") == "حفظ":
                        save_btn = btn

        # Initially hide save button
        if save_btn:
            save_btn.pack_forget()

        # Create edit button
        edit_button = None
        if btns_frame:
            edit_button = CTkButton(
                btns_frame,
                text="تعديل الوصف",
                fg_color="#2D8CFF",
                text_color="#fff",
                hover_color="#1F6BB5",
                font=("Arial", 14, "bold"),
                command=lambda: enable_edit(edit_button, save_btn, cancel_btn, date_label, 
                                          amount_label, desc_box, frame, description, 
                                          amount, date, btns_frame)
            )
            if cancel_btn:
                cancel_btn.pack_forget()

            edit_button.pack(side="right", padx=10)
            if cancel_btn:
                cancel_btn.pack(side="right", padx=10)

        def enable_edit(edit_btn, save_btn, cancel_btn, date_lbl, amount_lbl, desc_box_widget, 
                       parent_frame, original_description, original_amount, original_date, button_frame):
            """Enable editing mode for the expense details."""
            # Hide view mode widgets
            if edit_btn:
                edit_btn.pack_forget()
            date_lbl.pack_forget()
            amount_lbl.pack_forget()
            desc_box_widget.pack_forget()

            # Clear button frame
            if button_frame:
                for child in button_frame.winfo_children():
                    child.pack_forget()

            # Create editable widgets
            self.date_entry_widget = DateEntry(parent_frame, self.arabic_handler)
            self.date_entry_widget.set_date(original_date)
            self.date_entry_widget.pack(fill="x", pady=(0, 5))

            self.amount_entry_widget = CTkEntry(parent_frame, font=("Arial", 13))
            self.amount_entry_widget.insert(0, str(original_amount))
            self.amount_entry_widget.pack(fill="x", pady=(0, 10))

            self.desc_edit_box_widget = CTkTextbox(parent_frame, font=("Arial", 14), height=180, wrap="word")
            self.desc_edit_box_widget.pack(fill="both", expand=True, pady=10)
            self.desc_edit_box_widget.insert("1.0", original_description)

            # Pack edit mode buttons
            if button_frame:
                if save_btn:
                    save_btn.pack(side="right", padx=10)
                    save_btn.configure(command=lambda: on_save(window, self.desc_edit_box_widget, 
                                                             self.amount_entry_widget, self.date_entry_widget))

                if cancel_btn:
                    cancel_btn.pack(side="right", padx=10)

        window.protocol("WM_DELETE_WINDOW", lambda: on_cancel(window))
        window.lift()
        window.grab_set()

    def show_full_income_description(self, description, amount, date, income_id=None):
        """Show full income description in a popup window with edit capability.
        
        Args:
            description: The income description
            amount: The income amount
            date: The income date
            income_id: The ID of the income record
        """
        def on_save(window, desc_edit_box_widget, amount_entry_widget, date_entry_widget):
            """Handle saving edited income details."""
            new_desc = desc_edit_box_widget.get("1.0", "end").strip()
            new_amount = amount_entry_widget.get().strip()
            new_date = date_entry_widget.get_date()

            if self.controller.update_income(income_id, new_desc, new_amount, new_date):
                window.destroy()
                self.load_income()
                self.load_expenses()

        def on_cancel(window):
            """Handle canceling the edit operation."""
            window.destroy()

        # Create the description window
        window, frame, desc_box, date_label, amount_label = create_description_window(
            self.master,
            "تفاصيل الإيراد",
            description,
            amount,
            date,
            on_save=lambda: None,  # Dummy command for initial button creation
            on_cancel=on_cancel
        )

        # Get button references
        btns_frame = None
        for child in reversed(frame.winfo_children()):
            if isinstance(child, CTkFrame):
                btns_frame = child
                break

        cancel_btn = None
        save_btn = None

        if btns_frame:
            for btn in btns_frame.winfo_children():
                if isinstance(btn, CTkButton):
                    if btn.cget("text") == "إلغاء":
                        cancel_btn = btn
                    elif btn.cget("text") == "حفظ":
                        save_btn = btn

        # Initially hide save button
        if save_btn:
            save_btn.pack_forget()

        # Create edit button
        edit_button = None
        if btns_frame:
            edit_button = CTkButton(
                btns_frame,
                text="تعديل الإيراد",
                fg_color="#4CAF50",
                text_color="#fff",
                hover_color="#388E3C",
                font=("Arial", 14, "bold"),
                command=lambda: enable_edit(edit_button, save_btn, cancel_btn, date_label, 
                                          amount_label, desc_box, frame, description, 
                                          amount, date, btns_frame)
            )
            if cancel_btn:
                cancel_btn.pack_forget()

            edit_button.pack(side="right", padx=10)
            if cancel_btn:
                cancel_btn.pack(side="right", padx=10)

        def enable_edit(edit_btn, save_btn, cancel_btn, date_lbl, amount_lbl, desc_box_widget, 
                       parent_frame, original_description, original_amount, original_date, button_frame):
            """Enable editing mode for the income details."""
            # Hide view mode widgets
            if edit_btn:
                edit_btn.pack_forget()
            date_lbl.pack_forget()
            amount_lbl.pack_forget()
            desc_box_widget.pack_forget()

            # Clear button frame
            if button_frame:
                for child in button_frame.winfo_children():
                    child.pack_forget()

            # Create editable widgets
            self.date_entry_widget = DateEntry(parent_frame, self.arabic_handler)
            self.date_entry_widget.set_date(original_date)
            self.date_entry_widget.pack(fill="x", pady=(0, 5))

            self.amount_entry_widget = CTkEntry(parent_frame, font=("Arial", 13))
            self.amount_entry_widget.insert(0, str(original_amount))
            self.amount_entry_widget.pack(fill="x", pady=(0, 10))

            self.desc_edit_box_widget = CTkTextbox(parent_frame, font=("Arial", 14), height=180, wrap="word")
            self.desc_edit_box_widget.pack(fill="both", expand=True, pady=10)
            self.desc_edit_box_widget.insert("1.0", original_description)

            # Pack edit mode buttons
            if button_frame:
                if save_btn:
                    save_btn.pack(side="right", padx=10)
                    save_btn.configure(command=lambda: on_save(window, self.desc_edit_box_widget, 
                                                             self.amount_entry_widget, self.date_entry_widget))

                if cancel_btn:
                    cancel_btn.pack(side="right", padx=10)

        window.protocol("WM_DELETE_WINDOW", lambda: on_cancel(window))
        window.lift()
        window.grab_set()

    def confirm_delete_expense(self, expense_id):
        """Handle expense deletion confirmation and removal.
        
        Args:
            expense_id: The ID of the expense to delete
        """
        if self.controller.delete_expense(expense_id):
            self.load_expenses()
            self.load_income()

    def confirm_delete_income(self, income_id):
        """Handle income deletion confirmation and removal.
        
        Args:
            income_id: The ID of the income to delete
        """
        if self.controller.delete_income(income_id):
            self.load_income()
            self.load_expenses() 