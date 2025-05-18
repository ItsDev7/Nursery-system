from customtkinter import *
from .controllers import FeesController
from .utils import create_description_window

class FeesPage:
    def __init__(self, master, on_back=None):
        self.master = master
        self.on_back = on_back
        self.controller = FeesController(self)
        self.setup_ui()

    def setup_ui(self):
        """Set up the main UI components."""
        for widget in self.master.winfo_children():
            widget.destroy()

        self.main_frame = CTkFrame(self.master, fg_color=("#F7F7F7", "#232323"))
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Configure grid weights for main_frame
        self.main_frame.grid_columnconfigure(0, weight=0)  # Back button column
        self.main_frame.grid_columnconfigure(1, weight=1)  # Content columns
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1) # Expense table row
        self.main_frame.grid_rowconfigure(3, weight=1) # Income table row

        # Back button
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
            # Place back button in column 0, row 0
            back_icon.grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=(0, 10))

        # Expense section
        self.setup_expense_section()
        
        # Income section
        self.setup_income_section()
        
        # Summary section
        self.setup_summary_section()

        # Load initial data
        self.load_expenses()
        self.load_income()

    def setup_expense_section(self):
        """Set up the expense input and display section."""
        # Expense Input Frame
        input_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        # Place input_frame in row 0, spanning columns 1 to 3
        input_frame.grid(row=0, column=1, columnspan=3, sticky="ew", pady=10, padx=10)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(2, weight=1)

        # Description
        CTkLabel(input_frame, 
                text="وصف المصروف:", 
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

        # Amount
        CTkLabel(input_frame, 
                text="المبلغ:", 
                font=("Arial", 15, "bold"), anchor="e", justify="right").grid(row=2, column=2, sticky="e", padx=10, pady=(10, 5))
        self.amount_entry = CTkEntry(input_frame, 
                                    font=("Arial", 14),
                                    width=180,
                                    fg_color=("#FFFFFF", "#404040"),
                                    border_width=1,
                                    justify="right")
        self.amount_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=10)

        # Add Expense Button
        CTkButton(input_frame, 
                 text="إضافة مصروف", 
                 font=("Arial", 15, "bold"),
                 fg_color="#2D8CFF",
                 hover_color="#1F6BB5",
                 height=40,
                 width=150,
                 corner_radius=8,
                 command=self.add_expense).grid(row=2, column=0, padx=10, sticky="w")

        # Expenses Table
        self.expense_frame = CTkScrollableFrame(self.main_frame, width=900, height=220, fg_color=("#F7F7F7", "#232323"))
        # Place expense_frame in row 1, spanning columns 0 to 3
        self.expense_frame.grid(row=1, column=0, columnspan=4, pady=15, sticky="nsew", padx=10)
        self.expense_frame.grid_columnconfigure(0, weight=1)
        self.expense_frame.grid_columnconfigure(1, weight=1)
        self.expense_frame.grid_columnconfigure(2, weight=2)
        self.expense_frame.grid_columnconfigure(3, weight=1)

    def setup_income_section(self):
        """Set up the income input and display section."""
        # Income Input Frame
        income_input_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        # Place income_input_frame in row 2, spanning columns 1 to 3
        income_input_frame.grid(row=2, column=1, columnspan=3, sticky="ew", pady=10, padx=10)
        income_input_frame.grid_columnconfigure(0, weight=1)
        income_input_frame.grid_columnconfigure(1, weight=1)
        income_input_frame.grid_columnconfigure(2, weight=1)

        # Description
        CTkLabel(income_input_frame, 
                text="وصف الإيراد:", 
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

        # Amount
        CTkLabel(income_input_frame, 
                text="المبلغ:", 
                font=("Arial", 15, "bold"), anchor="e", justify="right").grid(row=2, column=2, sticky="e", padx=10, pady=(10, 5))
        self.income_amount_entry = CTkEntry(income_input_frame, 
                                    font=("Arial", 14),
                                    width=180,
                                    fg_color=("#FFFFFF", "#404040"),
                                    border_width=1,
                                    justify="right")
        self.income_amount_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=10)

        # Add Income Button
        CTkButton(income_input_frame, 
                 text="إضافة إيراد", 
                 font=("Arial", 15, "bold"),
                 fg_color="#4CAF50",
                 hover_color="#388E3C",
                 height=40,
                 width=150,
                 corner_radius=8,
                 command=self.add_income).grid(row=2, column=0, padx=10, sticky="w")

        # Income Table
        self.income_frame = CTkScrollableFrame(self.main_frame, width=900, height=220, fg_color=("#F7F7F7", "#232323"))
        # Place income_frame in row 3, spanning columns 0 to 3
        self.income_frame.grid(row=3, column=0, columnspan=4, pady=15, sticky="nsew", padx=10)
        self.income_frame.grid_columnconfigure(0, weight=1)
        self.income_frame.grid_columnconfigure(1, weight=1)
        self.income_frame.grid_columnconfigure(2, weight=2)
        self.income_frame.grid_columnconfigure(3, weight=1)

    def setup_summary_section(self):
        """Set up the financial summary section."""
        summary_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        # Place summary_frame in row 4, spanning columns 0 to 3
        summary_frame.grid(row=4, column=0, columnspan=4, pady=15)
        self.summary_label = CTkLabel(summary_frame, 
                                     text="", 
                                     font=("Arial", 17, "bold"),
                                     text_color=("#2D8CFF", "#4CAF50"))
        self.summary_label.pack(pady=5)

    def add_expense(self):
        """Handle adding a new expense."""
        description = self.description_entry.get("0.0", "end").strip()
        amount_str = self.amount_entry.get().strip()
        
        if self.controller.add_expense(description, amount_str):
            self.description_entry.delete("0.0", "end")
            self.amount_entry.delete(0, "end")
            self.load_expenses()
            self.load_income()

    def add_income(self):
        """Handle adding a new income."""
        description = self.income_description_entry.get("0.0", "end").strip()
        amount_str = self.income_amount_entry.get().strip()
        
        if self.controller.add_income(description, amount_str):
            self.income_description_entry.delete("0.0", "end")
            self.income_amount_entry.delete(0, "end")
            self.load_income()
            self.load_expenses()

    def load_expenses(self):
        """Load and display expenses."""
        for widget in self.expense_frame.winfo_children():
            widget.destroy()

        # Table Headers
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

        # Load expenses
        expenses = self.controller.get_all_expenses()
        for row_index, (expense_id, desc, amount, date) in enumerate(expenses, start=1):
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

            CTkLabel(self.expense_frame, text=date, font=("Arial", 13), anchor="e", justify="right").grid(row=row_index, column=1, sticky="ew", padx=4, pady=4)
            desc_label = CTkLabel(
                self.expense_frame,
                text=desc[:50] + ("..." if len(desc) > 50 else ""),
                font=("Arial", 13),
                cursor="hand2",
                anchor="e", justify="right"
            )
            desc_label.grid(row=row_index, column=2, sticky="ew", padx=4, pady=4)
            desc_label.bind("<Button-1>", lambda e, d=desc, a=amount, dt=date, eid=expense_id: self.show_full_description(d, a, dt, eid))

            CTkLabel(self.expense_frame, text=amount, font=("Arial", 13), anchor="e", justify="right").grid(row=row_index, column=3, sticky="ew", padx=4, pady=4)

        self.update_summary()

    def load_income(self):
        """Load and display income records."""
        for widget in self.income_frame.winfo_children():
            widget.destroy()

        # Table Headers
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

        # Load income records
        income_records = self.controller.get_all_income()
        for row_index, (income_id, desc, amount, date) in enumerate(income_records, start=1):
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

            CTkLabel(self.income_frame, text=date, font=("Arial", 13), anchor="e", justify="right").grid(row=row_index, column=1, sticky="ew", padx=4, pady=4)
            desc_label = CTkLabel(
                self.income_frame,
                text=desc[:50] + ("..." if len(desc) > 50 else ""),
                font=("Arial", 13),
                cursor="hand2",
                anchor="e", justify="right"
            )
            desc_label.grid(row=row_index, column=2, sticky="ew", padx=4, pady=4)
            desc_label.bind("<Button-1>", lambda e, d=desc, a=amount, dt=date, iid=income_id: self.show_full_income_description(d, a, dt, iid))

            CTkLabel(self.income_frame, text=amount, font=("Arial", 13), anchor="e", justify="right").grid(row=row_index, column=3, sticky="ew", padx=4, pady=4)

        self.update_summary()

    def update_summary(self):
        """Update the financial summary display."""
        summary = self.controller.get_summary()
        self.summary_label.configure(
            text=f"الإيرادات: {summary['income']} | المصروفات: {summary['expenses']} | المتبقي: {summary['remaining']}"
        )

    def show_full_description(self, description, amount, date, expense_id=None):
        """Show full expense description in a popup window."""
        # Define callbacks
        # Modify on_save to accept entry widgets directly
        def on_save(window, desc_edit_box_widget, amount_entry_widget, date_entry_widget):
            new_desc = desc_edit_box_widget.get("1.0", "end").strip()
            new_amount = amount_entry_widget.get().strip()
            new_date = date_entry_widget.get().strip()

            if self.controller.update_expense(expense_id, new_desc, new_amount, new_date):
                window.destroy()
                self.load_expenses()
                self.load_income()

        def on_cancel(window):
            window.destroy()

        # Create the basic window structure, passing on_save and on_cancel to create the initial buttons
        # Pass on_save now so the button is created in utils.py, but the command will be updated later
        window, frame, desc_box, date_label, amount_label = create_description_window(
            self.master,
            "تفاصيل الوصف",
            description,
            amount,
            date,
            on_save=lambda: None,  # Pass a dummy command initially so the save button is created
            on_cancel=on_cancel
        )

        # Get references to the buttons created by create_description_window
        # Assuming the buttons are in the last CTkFrame packed in the window's main frame
        btns_frame = None
        for child in reversed(frame.winfo_children()): # Iterate in reverse to find the last CTkFrame
             if isinstance(child, CTkFrame): # Assuming the button frame is a CTkFrame
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

        # Initially hide the save button
        if save_btn:
            save_btn.pack_forget()

        # Create the edit button and pack it initially into the buttons frame
        edit_button = None # Initialize edit_button to None
        if btns_frame:
            edit_button = CTkButton(
                btns_frame,
                text="تعديل الوصف",
                fg_color="#2D8CFF",
                text_color="#fff",
                hover_color="#1F6BB5",
                font=("Arial", 14, "bold"),
                command=lambda: enable_edit(edit_button, save_btn, cancel_btn, date_label, amount_label, desc_box, frame, description, amount, date, btns_frame)
            )
            # Ensure edit button is packed alongside the initial cancel button in the correct order (Edit | Cancel)
            if cancel_btn:
                cancel_btn.pack_forget() # Unpack existing cancel button

            # Pack buttons for initial view (Edit | Cancel)
            edit_button.pack(side="right", padx=10)
            if cancel_btn:
                cancel_btn.pack(side="right", padx=10)

        # Add edit functionality
        # Pass btns_frame to enable_edit
        def enable_edit(edit_btn, save_btn, cancel_btn, date_lbl, amount_lbl, desc_box_widget, parent_frame, original_description, original_amount, original_date, button_frame):
            # Hide view mode widgets
            if edit_btn:
                edit_btn.pack_forget()
            date_lbl.pack_forget()
            amount_lbl.pack_forget()
            desc_box_widget.pack_forget()

            # Unpack all buttons currently packed in the button frame
            if button_frame:
                 for child in button_frame.winfo_children():
                      child.pack_forget()

            # Create editable widgets
            self.date_entry_widget = CTkEntry(parent_frame, font=("Arial", 13))
            self.date_entry_widget.insert(0, original_date)
            self.date_entry_widget.pack(fill="x", pady=(0, 5))

            self.amount_entry_widget = CTkEntry(parent_frame, font=("Arial", 13))
            self.amount_entry_widget.insert(0, str(original_amount))
            self.amount_entry_widget.pack(fill="x", pady=(0, 10))

            self.desc_edit_box_widget = CTkTextbox(parent_frame, font=("Arial", 14), height=180, wrap="word")
            self.desc_edit_box_widget.pack(fill="both", expand=True, pady=10)
            self.desc_edit_box_widget.insert("1.0", original_description)

            # Pack edit mode buttons: Save and Cancel in the correct order within the buttons frame (Save | Cancel)
            if button_frame:
                # Pack save button first, then cancel button
                if save_btn:
                    save_btn.pack(side="right", padx=10)
                    # Connect the save command now that the entry widgets are created
                    save_btn.configure(command=lambda: on_save(window, self.desc_edit_box_widget, self.amount_entry_widget, self.date_entry_widget))

                if cancel_btn:
                    cancel_btn.pack(side="right", padx=10)


        # Ensure the initial state is correct: Cancel and Edit buttons visible, Save button hidden
        # This is handled by the initial packing above.

        window.protocol("WM_DELETE_WINDOW", lambda: on_cancel(window))
        window.lift()
        window.grab_set()


    def show_full_income_description(self, description, amount, date, income_id=None):
        """Show full income description in a popup window."""
        # Define callbacks
        # Modify on_save to accept entry widgets directly
        def on_save(window, desc_edit_box_widget, amount_entry_widget, date_entry_widget):
            new_desc = desc_edit_box_widget.get("1.0", "end").strip()
            new_amount = amount_entry_widget.get().strip()
            new_date = date_entry_widget.get().strip()

            if self.controller.update_income(income_id, new_desc, new_amount, new_date):
                window.destroy()
                self.load_income()
                self.load_expenses()

        def on_cancel(window):
            window.destroy()

        # Create the basic window structure, passing on_save and on_cancel to create the initial buttons
        # Pass on_save now so the button is created in utils.py, but the command will be updated later
        window, frame, desc_box, date_label, amount_label = create_description_window(
            self.master,
            "تفاصيل الإيراد",
            description,
            amount,
            date,
            on_save=lambda: None, # Pass a dummy command initially so the save button is created
            on_cancel=on_cancel
        )

        # Get references to the buttons created by create_description_window
        # Assuming the buttons are in the last CTkFrame packed in the window's main frame
        btns_frame = None
        for child in reversed(frame.winfo_children()): # Iterate in reverse to find the last CTkFrame
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

        # Initially hide the save button
        if save_btn:
            save_btn.pack_forget()

        # Create the edit button and pack it initially into the buttons frame
        edit_button = None # Initialize edit_button to None
        if btns_frame:
            edit_button = CTkButton(
                btns_frame,
                text="تعديل الإيراد",
                fg_color="#4CAF50",
                text_color="#fff",
                hover_color="#388E3C",
                font=("Arial", 14, "bold"),
                command=lambda: enable_edit(edit_button, save_btn, cancel_btn, date_label, amount_label, desc_box, frame, description, amount, date, btns_frame)
            )
            # Ensure edit button is packed alongside the initial cancel button in the correct order (Edit | Cancel)
            if cancel_btn:
                cancel_btn.pack_forget() # Unpack existing cancel button

            # Pack buttons for initial view (Edit | Cancel)
            edit_button.pack(side="right", padx=10);
            if cancel_btn:
                cancel_btn.pack(side="right", padx=10);

        # Add edit functionality
        # Pass btns_frame to enable_edit
        def enable_edit(edit_btn, save_btn, cancel_btn, date_lbl, amount_lbl, desc_box_widget, parent_frame, original_description, original_amount, original_date, button_frame):
            # Hide view mode widgets
            if edit_btn:
                edit_btn.pack_forget()
            date_lbl.pack_forget()
            amount_lbl.pack_forget()
            desc_box_widget.pack_forget()

            # Unpack all buttons currently packed in the button frame
            if button_frame:
                 for child in button_frame.winfo_children():
                      child.pack_forget()

            # Create editable widgets
            self.date_entry_widget = CTkEntry(parent_frame, font=("Arial", 13))
            self.date_entry_widget.insert(0, original_date)
            self.date_entry_widget.pack(fill="x", pady=(0, 5))

            self.amount_entry_widget = CTkEntry(parent_frame, font=("Arial", 13))
            self.amount_entry_widget.insert(0, str(original_amount))
            self.amount_entry_widget.pack(fill="x", pady=(0, 10))

            self.desc_edit_box_widget = CTkTextbox(parent_frame, font=("Arial", 14), height=180, wrap="word")
            self.desc_edit_box_widget.pack(fill="both", expand=True, pady=10)
            self.desc_edit_box_widget.insert("1.0", original_description)

            # Pack edit mode buttons: Save and Cancel in the correct order within the buttons frame (Save | Cancel)
            if button_frame:
                # Pack save button first, then cancel button
                if save_btn:
                    save_btn.pack(side="right", padx=10)
                    # Connect the save command now that the entry widgets are created
                    save_btn.configure(command=lambda: on_save(window, self.desc_edit_box_widget, self.amount_entry_widget, self.date_entry_widget))

                if cancel_btn:
                    cancel_btn.pack(side="right", padx=10)

        # Ensure the initial state is correct: Cancel and Edit buttons visible, Save button hidden
        # This is handled by the initial packing above.

        window.protocol("WM_DELETE_WINDOW", lambda: on_cancel(window))
        window.lift()
        window.grab_set()

    def confirm_delete_expense(self, expense_id):
        """Handle expense deletion confirmation."""
        if self.controller.delete_expense(expense_id):
            self.load_expenses()
            self.load_income()

    def confirm_delete_income(self, income_id):
        """Handle income deletion confirmation."""
        if self.controller.delete_income(income_id):
            self.load_income()
            self.load_expenses() 