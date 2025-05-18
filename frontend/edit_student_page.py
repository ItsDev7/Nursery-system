from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkOptionMenu, CTkButton, StringVar
from tkinter import messagebox
from backend.database import update_student

class EditStudentPage:
    def __init__(self, main_window, student_data, on_back=None):
        self.main = main_window
        self.on_back = on_back
        self.student_data = student_data
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

        # زر الرجوع سهم في الأعلى يسار
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
        self.name_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14))
        self.name_entry.insert(0, self.student_data["name"])
        self.name_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # الرقم القومي
        CTkLabel(frame, text=self.arabic(":الرقم القومي"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.nid_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14))
        self.nid_entry.insert(0, self.student_data["nid"])
        self.nid_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # الفصل الدراسي والجنس في صف واحد
        CTkLabel(frame, text=self.arabic(":الفصل الدراسي"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        CTkLabel(frame, text=self.arabic(":الجنس"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=0, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        levels = ["التمهيدي", "الاول المستوى", "الثاني المستوى", "الصغار فصل", "يومي اشتراك"]
        arabic_levels = [self.arabic(level) for level in levels]
        self.term_var = StringVar(value=self.student_data["term"])
        self.term_menu = CTkOptionMenu(frame, values=arabic_levels, variable=self.term_var)
        self.term_menu.grid(row=row, column=1, sticky="ew", pady=5, padx=(0, 10))
        self.gender_var = StringVar(value=self.student_data["gender"])
        self.gender_menu = CTkOptionMenu(frame, values=[self.arabic("ذكر"), self.arabic("أنثى")], variable=self.gender_var)
        self.gender_menu.grid(row=row, column=0, sticky="ew", pady=5, padx=(0, 10))
        row += 1

        # هاتف ولي الأمر
        CTkLabel(frame, text=self.arabic(":هاتف ولي الأمر"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.phone1_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14))
        self.phone1_entry.insert(0, self.student_data["phone1"])
        self.phone1_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # هاتف ولي أمر آخر
        CTkLabel(frame, text=self.arabic(":هاتف ولي أمر آخر*"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.phone2_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14))
        self.phone2_entry.insert(0, self.student_data["phone2"])
        self.phone2_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # الرسوم
        CTkLabel(frame, text=self.arabic(":الرسوم"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.fee_entries = []
        self.fee_date_widgets = []
        fees = [self.student_data["fee1"], self.student_data["fee2"], self.student_data["fee3"], self.student_data["fee4"]]
        fee_dates = [self.student_data["fee1_date"], self.student_data["fee2_date"], self.student_data["fee3_date"], self.student_data["fee4_date"]]
        # رأس جدول الرسوم
        fee_header = CTkFrame(frame)
        fee_header.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 2))
        for idx, txt in enumerate([self.arabic("يوم"), self.arabic("شهر"), self.arabic("سنة"), self.arabic("المبلغ"), self.arabic("اسم القسط")]):
            CTkLabel(fee_header, text=txt, font=("Arial", 13, "bold"), anchor="center", justify="center").grid(row=0, column=idx, padx=4, pady=2, sticky="ew")
        row += 1
        for i in range(4):
            fee_row_frame = CTkFrame(frame)
            fee_row_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=2)
            for idx in range(5):
                fee_row_frame.grid_columnconfigure(idx, weight=1)
            # التاريخ: يوم / شهر / سنة
            day_entry = CTkEntry(fee_row_frame, width=35, justify="center")
            month_entry = CTkEntry(fee_row_frame, width=35, justify="center")
            year_entry = CTkEntry(fee_row_frame, width=50, justify="center")
            # تعبئة القيم القديمة
            if fee_dates[i]:
                try:
                    d, m, y = fee_dates[i].split("/")
                except:
                    d, m, y = "", "", ""
            else:
                d, m, y = "", "", ""
            day_entry.insert(0, d)
            month_entry.insert(0, m)
            year_entry.insert(0, y)
            day_entry.grid(row=0, column=0, padx=4, sticky="ew")
            month_entry.grid(row=0, column=1, padx=4, sticky="ew")
            year_entry.grid(row=0, column=2, padx=4, sticky="ew")
            self.fee_date_widgets.append((day_entry, month_entry, year_entry))
            # مربع القسط
            entry = CTkEntry(fee_row_frame, width=80, justify="right", font=("Arial", 14))
            entry.insert(0, fees[i])
            entry.grid(row=0, column=3, padx=4, sticky="ew")
            self.fee_entries.append(entry)
            # اسم القسط
            CTkLabel(fee_row_frame, text=[self.arabic("القسط الأول"), self.arabic("القسط الثاني"), self.arabic("القسط الثالث"), self.arabic("الملابس او القسط الرابع*")][i], font=("Arial", 13)).grid(row=0, column=4, padx=2, sticky="ew")
            row += 1

        # زر الحفظ
        self.save_button = CTkButton(
            frame,
            text=self.arabic("حفظ التعديلات"),
            font=("Arial", 18),
            height=40,
            width=200,
            command=self.update_student
        )
        self.save_button.grid(row=row, column=0, columnspan=2, pady=(20, 10), sticky="ew")

    def update_student(self):
        original_name = self.student_data["name"]
        name = self.name_entry.get().strip()
        nid = self.nid_entry.get().strip()
        term = self.term_var.get().strip()
        gender = self.gender_var.get().strip()
        phone1 = self.phone1_entry.get().strip()
        phone2 = self.phone2_entry.get().strip()
        fees = [f.get().strip() for f in self.fee_entries]
        fee_dates = [f"{d.get().strip()}/{m.get().strip()}/{y.get().strip()}" for d, m, y in self.fee_date_widgets]

        if not all([name, nid, term, gender, phone1, phone2]) or not all(fees):
            messagebox.showerror("خطأ", "من فضلك املأ جميع الحقول")
            return

        update_student(original_name, name, nid, term, gender, phone1, phone2, fees, fee_dates)
        messagebox.showinfo("تم", "تم تحديث البيانات بنجاح")
        self.go_back()

    def go_back(self):
        for widget in self.main.winfo_children():
            widget.destroy()
        self.on_back()