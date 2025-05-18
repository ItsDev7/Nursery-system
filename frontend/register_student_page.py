from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkOptionMenu, CTkButton, StringVar
from tkinter import messagebox
from backend.database import add_student
import tkinter as tk
class RegisterStudentPage:
    def __init__(self, main_window, on_back=None):
        self.main = main_window
        self.on_back = on_back
        self.setup_ui()

    def arabic(self, text: str) -> str:
        
        return text

    def setup_ui(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        # إطار رئيسي متوسط العرض
        frame = CTkFrame(self.main)
        frame.grid(row=0, column=0, sticky="nsew", padx=80, pady=40)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        for i in range(2):
            frame.grid_columnconfigure(i, weight=1)

        row = 0

        # زر الرجوع في أعلى يسار الشاشة كأيقونة سهم
        if self.on_back:
            back_icon = CTkButton(
                frame,
                text="←",
                font=("Arial", 18, "bold"),
                width=40,
                height=40,
                fg_color="#ff3333",
                text_color="#000000",
                hover_color="#b71c1c",
                corner_radius=20,
                command=self.go_back
            )
            back_icon.grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=(0, 10))

        # اسم الطالب
        CTkLabel(frame, text=self.arabic(":اسم الطالب"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.name_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14), placeholder_text=self.arabic("أدخل الاسم"))
        self.name_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # الرقم القومي
        CTkLabel(frame, text=self.arabic(":الرقم القومي"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.nid_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14), placeholder_text=self.arabic("أدخل الرقم القومي"))
        self.nid_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # الفصل الدراسي والجنس في صف واحد
        CTkLabel(frame, text=self.arabic(":الفصل الدراسي"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        CTkLabel(frame, text=self.arabic(":الجنس"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=0, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        levels = ["التمهيدي", "الاول المستوى", "الثاني المستوى", "الصغار فصل", "يومي اشتراك"]
        arabic_levels = [self.arabic(level) for level in levels]
        self.term_var = tk.StringVar(value=arabic_levels[0])
        self.term_menu = CTkOptionMenu(frame, values=arabic_levels, variable=self.term_var)
        self.term_menu.grid(row=row, column=1, sticky="ew", pady=5, padx=(0, 10))
        self.gender_var = tk.StringVar(value=self.arabic("ذكر"))
        self.gender_menu = CTkOptionMenu(frame, values=[self.arabic("ذكر"), self.arabic("أنثى")], variable=self.gender_var)
        self.gender_menu.grid(row=row, column=0, sticky="ew", pady=5, padx=(0, 10))
        row += 1

        # هاتف ولي الأمر
        CTkLabel(frame, text=self.arabic(":هاتف ولي الأمر"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.phone1_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14), placeholder_text=self.arabic("أدخل رقم الهاتف"))
        self.phone1_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # هاتف ولي أمر آخر
        CTkLabel(frame, text=self.arabic(":هاتف ولي أمر آخر*"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.phone2_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14), placeholder_text=self.arabic("أدخل رقم الهاتف اخر ان وجد*"))
        self.phone2_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # الرسوم
        CTkLabel(frame, text=self.arabic(":الرسوم"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1

        self.fee_entries = []
        self.fee_date_widgets = []
        fee_placeholders = [
            self.arabic("القسط الأول"),
            self.arabic("القسط الثاني"),
            self.arabic("القسط الثالث"),
            self.arabic("الملابس او القسط الرابع*")
        ]
        # رأس جدول الرسوم
        fee_header = CTkFrame(frame)
        fee_header.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 2))
        for idx in range(5):
            fee_header.grid_columnconfigure(idx, weight=1)
        for idx, txt in enumerate([
            self.arabic("يوم"),
            self.arabic("شهر"),
            self.arabic("سنة"),
            self.arabic("المبلغ"),
            self.arabic("اسم القسط")]):
            CTkLabel(fee_header, text=txt, font=("Arial", 13, "bold"), anchor="center", justify="center").grid(row=0, column=idx, padx=4, pady=2, sticky="ew")
        row += 1
        for i in range(4):
            fee_row_frame = CTkFrame(frame)
            fee_row_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=2)
            for idx in range(5):
                fee_row_frame.grid_columnconfigure(idx, weight=1)
            # التاريخ: يوم / شهر / سنة
            day = CTkEntry(fee_row_frame, width=35, placeholder_text=self.arabic("يوم"), justify="center")
            month = CTkEntry(fee_row_frame, width=35, placeholder_text=self.arabic("شهر"), justify="center")
            year = CTkEntry(fee_row_frame, width=50, placeholder_text=self.arabic("سنة"), justify="center")
            day.grid(row=0, column=0, padx=4, sticky="ew")
            month.grid(row=0, column=1, padx=4, sticky="ew")
            year.grid(row=0, column=2, padx=4, sticky="ew")
            self.fee_date_widgets.append((day, month, year))
            # مربع القسط
            entry = CTkEntry(fee_row_frame, width=80, justify="right", font=("Arial", 14))
            entry.grid(row=0, column=3, padx=4, sticky="ew")
            self.fee_entries.append(entry)
            # اسم القسط
            CTkLabel(fee_row_frame, text=fee_placeholders[i], font=("Arial", 13), anchor="e", justify="right").grid(row=0, column=4, padx=4, sticky="ew")
            row += 1

        # زر التسجيل
        self.register_button = CTkButton(
            frame,
            text=self.arabic("تسجيل"),
            font=("Arial", 18),
            height=40,
            width=200,
            command=self.register_student
        )
        self.register_button.grid(row=row, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        row += 1

    def register_student(self):
        name = self.name_entry.get().strip()
        nid = self.nid_entry.get().strip()
        term = self.term_var.get().strip()
        gender = self.gender_var.get().strip()
        phone1 = self.phone1_entry.get().strip()
        phone2 = self.phone2_entry.get().strip()
        fees = [f.get().strip() for f in self.fee_entries]

        # استخراج التواريخ من خانات التاريخ الأربعة بدون تحقق
        fee_dates = []
        for date_widgets in self.fee_date_widgets:
            day, month, year = [w.get().strip() for w in date_widgets]
            fee_dates.append(f"{day}/{month}/{year}")

        # تحقق فقط من الحقول الأساسية
        if not name or not nid or (not phone1 and not phone2):
            messagebox.showerror("خطأ", "يجب إدخال اسم الطالب والرقم القومي ورقم هاتف واحد على الأقل")
            return

        add_student(name, nid, term, gender, phone1, phone2, fees, fee_dates)
        messagebox.showinfo("تم", "تم التسجيل بنجاح")

        # تفريغ الحقول
        self.name_entry.delete(0, "end")
        self.name_entry.configure(placeholder_text=self.arabic("أدخل الاسم"))
        self.nid_entry.delete(0, "end")
        self.nid_entry.configure(placeholder_text=self.arabic("أدخل الرقم القومي"))
        self.phone1_entry.delete(0, "end")
        self.phone1_entry.configure(placeholder_text=self.arabic("أدخل رقم الهاتف"))
        self.phone2_entry.delete(0, "end")
        self.phone2_entry.configure(placeholder_text=self.arabic("أدخل رقم الهاتف اخر ان وجد*"))
        for f in self.fee_entries:
            f.delete(0, "end")
        for idx, date_widgets in enumerate(self.fee_date_widgets):
            for j, widget in enumerate(date_widgets):
                widget.delete(0, "end")
                if j == 0:
                    widget.configure(placeholder_text=self.arabic("يوم"))
                elif j == 1:
                    widget.configure(placeholder_text=self.arabic("شهر"))
                elif j == 2:
                    widget.configure(placeholder_text=self.arabic("سنة"))

    def go_back(self):
        for widget in self.main.winfo_children():
            widget.destroy()
        self.on_back()
