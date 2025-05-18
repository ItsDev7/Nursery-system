from customtkinter import *
from tkinter import ttk, Toplevel, Text, END
from datetime import datetime
from backend.database import get_all_students, add_general_expense, get_all_general_expenses, get_summary, add_income, get_all_income, delete_income, update_income
import tkinter as tk
# set_appearance_mode("dark")
# set_default_color_theme("dark-blue")

class FeesPage:
    def __init__(self, master, on_back=None):
        self.master = master
        self.on_back = on_back
        self.setup_ui()

    def setup_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.main_frame = CTkFrame(self.master, fg_color=("#F7F7F7", "#232323"))
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # --- Expense Input Section ---
        input_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        input_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=10, padx=10)
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
        # دعم الكتابة من اليمين لليسار في مربع الوصف
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

        # --- Expenses Table ---
        self.expense_frame = CTkScrollableFrame(self.main_frame, width=900, height=220, fg_color=("#F7F7F7", "#232323"))
        self.expense_frame.grid(row=1, column=0, columnspan=3, pady=15, sticky="nsew", padx=10)
        self.expense_frame.grid_columnconfigure(0, weight=1)
        self.expense_frame.grid_columnconfigure(1, weight=1)
        self.expense_frame.grid_columnconfigure(2, weight=2)
        self.expense_frame.grid_columnconfigure(3, weight=1)
        
        # --- Income Input Section ---
        income_input_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        income_input_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10, padx=10)
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
        # دعم الكتابة من اليمين لليسار في مربع الوصف
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
                 
        # --- Income Table ---
        self.income_frame = CTkScrollableFrame(self.main_frame, width=900, height=220, fg_color=("#F7F7F7", "#232323"))
        self.income_frame.grid(row=3, column=0, columnspan=3, pady=15, sticky="nsew", padx=10)
        self.income_frame.grid_columnconfigure(0, weight=1)
        self.income_frame.grid_columnconfigure(1, weight=1)
        self.income_frame.grid_columnconfigure(2, weight=2)
        self.income_frame.grid_columnconfigure(3, weight=1)

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

        # --- Summary Section ---
        summary_frame = CTkFrame(self.main_frame, fg_color=("#F7F7F7", "#232323"))
        summary_frame.grid(row=4, column=0, columnspan=3, pady=15)
        self.summary_label = CTkLabel(summary_frame, 
                                     text="", 
                                     font=("Arial", 17, "bold"),
                                     text_color=("#2D8CFF", "#4CAF50"))
        self.summary_label.pack(pady=5)

        # زر الرجوع في أعلى يسار الصفحة كأيقونة سهم
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

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.load_expenses()
        self.load_income()

    # ============ أهم جزء: التأكد من وجود جميع الدوال المطلوبة ============
    # ============ دوال المصروفات ============
    def add_expense(self):
        description = self.description_entry.get("0.0", "end").strip()
        amount_str = self.amount_entry.get().strip()
        if not description or not amount_str:
            from tkinter import messagebox
            messagebox.showerror("خطأ", "يجب إدخال كل من الوصف والمبلغ لإضافة المصروف")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا صحيحًا أو عشريًا")
            return
        date = datetime.now().strftime("%Y-%m-%d")
        add_general_expense(description, amount, date)
        self.description_entry.delete("0.0", "end")
        self.amount_entry.delete(0, "end")
        self.load_expenses()
        self.load_income()

    def load_expenses(self):
        for widget in self.expense_frame.winfo_children():
            widget.destroy()

        transactions = get_all_general_expenses()
        # رأس الجدول
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

        for row_index, (expense_id, desc, amount, date) in enumerate(transactions, start=1):
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

        summary = get_summary()
        self.summary_label.configure(
            text=f"الإيرادات: {summary['income']} | المصروفات: {summary['expenses']} | المتبقي: {summary['remaining']}"
        )

    def show_full_description(self, description, amount, date, expense_id=None):
        # لا تفتح أكثر من نافذة وصف في نفس الوقت
        if hasattr(self, 'desc_window') and self.desc_window is not None and self.desc_window.winfo_exists():
            self.desc_window.focus()
            return
        import customtkinter as ctk
        self.desc_window = ctk.CTkToplevel(self.master)
        self.desc_window.title("تفاصيل الوصف")
        self.desc_window.geometry("500x420")
        self.desc_window.resizable(False, False)
        frame = ctk.CTkFrame(self.desc_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # متغيرات التحرير
        edit_mode = {'active': False}
        desc_var = ctk.StringVar(value=description)
        amount_var = ctk.StringVar(value=str(amount))
        date_var = ctk.StringVar(value=date)

        # عناصر العرض
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

        # زر إغلاق
        def close_desc():
            self.desc_window.destroy()
            self.desc_window = None
            self.master.focus()
        # زر تعديل
        def enable_edit():
            if edit_mode['active']:
                return
            edit_mode['active'] = True
            # إخفاء أزرار التعديل والإغلاق العلوية
            btns_frame.pack_forget()
            # تحويل الحقول إلى Editable
            date_label.pack_forget()
            amount_label.pack_forget()
            desc_box.pack_forget()
            # حقول قابلة للتعديل
            date_entry = ctk.CTkEntry(frame, font=("Arial", 13), textvariable=date_var)
            date_entry.pack(fill="x", pady=(0, 5))
            amount_entry = ctk.CTkEntry(frame, font=("Arial", 13), textvariable=amount_var)
            amount_entry.pack(fill="x", pady=(0, 10))
            desc_edit_box = ctk.CTkTextbox(frame, font=("Arial", 14), height=180, wrap="word")
            desc_edit_box.pack(fill="both", expand=True, pady=10)
            desc_edit_box.insert("1.0", desc_var.get())
            # أزرار الحفظ والإلغاء
            def save_edit():
                new_desc = desc_edit_box.get("1.0", "end").strip()
                new_amount = amount_entry.get().strip()
                new_date = date_entry.get().strip()
                if not new_desc or not new_amount or not new_date:
                    from tkinter import messagebox
                    messagebox.showerror("خطأ", "يجب إدخال كل من الوصف والمبلغ والتاريخ")
                    return
                try:
                    float(new_amount)
                except ValueError:
                    from tkinter import messagebox
                    messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا")
                    return
                # تحديث في قاعدة البيانات
                self.update_expense_in_db(expense_id, new_desc, new_amount, new_date)
                close_desc()
                self.load_expenses()
                self.load_income()
            def cancel_edit():
                close_desc()
            btn_frame = ctk.CTkFrame(frame)
            btn_frame.pack(pady=10)
            ctk.CTkButton(btn_frame, text="حفظ", fg_color="#4CAF50", text_color="#fff", hover_color="#388E3C", font=("Arial", 14, "bold"), command=save_edit).pack(side="right", padx=10)
            ctk.CTkButton(btn_frame, text="إلغاء", fg_color="#ff3333", text_color="#fff", hover_color="#b71c1c", font=("Arial", 14, "bold"), command=cancel_edit).pack(side="right", padx=10)

        btns_frame = ctk.CTkFrame(frame)
        btns_frame.pack(pady=10)
        ctk.CTkButton(btns_frame, text="تعديل الوصف", fg_color="#2D8CFF", text_color="#fff", hover_color="#1F6BB5", font=("Arial", 14, "bold"), command=enable_edit).pack(side="right", padx=10)
        ctk.CTkButton(btns_frame, text="إغلاق", fg_color="#ff3333", text_color="#fff", hover_color="#b71c1c", font=("Arial", 14, "bold"), command=close_desc).pack(side="right", padx=10)
        # عند إغلاق النافذة من X
        self.desc_window.protocol("WM_DELETE_WINDOW", close_desc)
        self.desc_window.lift()
        self.desc_window.grab_set()

    def update_expense_in_db(self, expense_id, new_desc, new_amount, new_date):
        from backend.database import update_expense
        update_expense(expense_id, new_desc, new_amount, new_date)

    def confirm_delete_expense(self, expense_id):
        from tkinter import messagebox
        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذا المصروف؟")
        if result:
            from backend.database import delete_expense
            delete_expense(expense_id)
            self.load_expenses()
            
    # ============ دوال الإيرادات ============
    def add_income(self):
        description = self.income_description_entry.get("0.0", "end").strip()
        amount_str = self.income_amount_entry.get().strip()
        if not description or not amount_str:
            from tkinter import messagebox
            messagebox.showerror("خطأ", "يجب إدخال كل من الوصف والمبلغ لإضافة الإيراد")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا صحيحًا أو عشريًا")
            return
        date = datetime.now().strftime("%Y-%m-%d")
        add_income(description, amount, date)
        self.income_description_entry.delete("0.0", "end")
        self.income_amount_entry.delete(0, "end")
        self.load_income()
        self.load_expenses()  # لتحديث الملخص

    def load_income(self):
        for widget in self.income_frame.winfo_children():
            widget.destroy()

        transactions = get_all_income()
        # رأس الجدول
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

        for row_index, (income_id, desc, amount, date) in enumerate(transactions, start=1):
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

        summary = get_summary()
        self.summary_label.configure(
            text=f"الإيرادات: {summary['income']} | المصروفات: {summary['expenses']} | المتبقي: {summary['remaining']}"
        )

    def show_full_income_description(self, description, amount, date, income_id=None):
        # لا تفتح أكثر من نافذة وصف في نفس الوقت
        if hasattr(self, 'income_desc_window') and self.income_desc_window is not None and self.income_desc_window.winfo_exists():
            self.income_desc_window.focus()
            return
        import customtkinter as ctk
        self.income_desc_window = ctk.CTkToplevel(self.master)
        self.income_desc_window.title("تفاصيل الإيراد")
        self.income_desc_window.geometry("500x420")
        self.income_desc_window.resizable(False, False)
        frame = ctk.CTkFrame(self.income_desc_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # متغيرات التحرير
        edit_mode = {'active': False}
        desc_var = ctk.StringVar(value=description)
        amount_var = ctk.StringVar(value=str(amount))
        date_var = ctk.StringVar(value=date)

        # عناصر العرض
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

        # زر إغلاق
        def close_desc():
            self.income_desc_window.destroy()
            self.income_desc_window = None
            self.master.focus()
        # زر تعديل
        def enable_edit():
            if edit_mode['active']:
                return
            edit_mode['active'] = True
            # إخفاء أزرار التعديل والإغلاق العلوية
            btns_frame.pack_forget()
            # تحويل الحقول إلى Editable
            date_label.pack_forget()
            amount_label.pack_forget()
            desc_box.pack_forget()
            # حقول قابلة للتعديل
            date_entry = ctk.CTkEntry(frame, font=("Arial", 13), textvariable=date_var)
            date_entry.pack(fill="x", pady=(0, 5))
            amount_entry = ctk.CTkEntry(frame, font=("Arial", 13), textvariable=amount_var)
            amount_entry.pack(fill="x", pady=(0, 10))
            desc_edit_box = ctk.CTkTextbox(frame, font=("Arial", 14), height=180, wrap="word")
            desc_edit_box.pack(fill="both", expand=True, pady=10)
            desc_edit_box.insert("1.0", desc_var.get())
            # أزرار الحفظ والإلغاء
            def save_edit():
                new_desc = desc_edit_box.get("1.0", "end").strip()
                new_amount = amount_entry.get().strip()
                new_date = date_entry.get().strip()
                if not new_desc or not new_amount or not new_date:
                    from tkinter import messagebox
                    messagebox.showerror("خطأ", "يجب إدخال كل من الوصف والمبلغ والتاريخ")
                    return
                try:
                    float(new_amount)
                except ValueError:
                    from tkinter import messagebox
                    messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا")
                    return
                # تحديث في قاعدة البيانات
                self.update_income_in_db(income_id, new_desc, new_amount, new_date)
                close_desc()
                self.load_income()
                self.load_expenses()  # لتحديث الملخص
            def cancel_edit():
                close_desc()
            btn_frame = ctk.CTkFrame(frame)
            btn_frame.pack(pady=10)
            ctk.CTkButton(btn_frame, text="حفظ", fg_color="#4CAF50", text_color="#fff", hover_color="#388E3C", font=("Arial", 14, "bold"), command=save_edit).pack(side="right", padx=10)
            ctk.CTkButton(btn_frame, text="إلغاء", fg_color="#ff3333", text_color="#fff", hover_color="#b71c1c", font=("Arial", 14, "bold"), command=cancel_edit).pack(side="right", padx=10)

        btns_frame = ctk.CTkFrame(frame)
        btns_frame.pack(pady=10)
        ctk.CTkButton(btns_frame, text="تعديل الإيراد", fg_color="#4CAF50", text_color="#fff", hover_color="#388E3C", font=("Arial", 14, "bold"), command=enable_edit).pack(side="right", padx=10)
        ctk.CTkButton(btns_frame, text="إغلاق", fg_color="#ff3333", text_color="#fff", hover_color="#b71c1c", font=("Arial", 14, "bold"), command=close_desc).pack(side="right", padx=10)
        # عند إغلاق النافذة من X
        self.income_desc_window.protocol("WM_DELETE_WINDOW", close_desc)
        self.income_desc_window.lift()
        self.income_desc_window.grab_set()

    def update_income_in_db(self, income_id, new_desc, new_amount, new_date):
        update_income(income_id, new_desc, new_amount, new_date)

    def confirm_delete_income(self, income_id):
        from tkinter import messagebox
        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذا الإيراد؟")
        if result:
            delete_income(income_id)
            self.load_income()
            self.load_expenses()  # لتحديث الملخص