from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkOptionMenu, CTkButton, StringVar
from tkinter import messagebox
from backend.database import add_teacher
import tkinter as tk
class RegisterTeacherPage:
    def __init__(self, main_window, on_back=None):
        self.main = main_window
        self.on_back = on_back
        self.setup_ui()

    def arabic(self, text: str) -> str:
        return text

    def setup_ui(self):
        for widget in self.main.winfo_children():
            widget.destroy()

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

        # اسم المعلمة
        CTkLabel(frame, text=self.arabic(":اسم المعلمة"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
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
        self.gender_var = tk.StringVar(value=self.arabic("أنثى"))
        self.gender_menu = CTkOptionMenu(frame, values=[self.arabic("أنثى"), self.arabic("ذكر")], variable=self.gender_var)
        self.gender_menu.grid(row=row, column=0, sticky="ew", pady=5, padx=(0, 10))
        row += 1

        # هاتف ولي الأمر
        CTkLabel(frame, text=self.arabic(":هاتف المعلمة"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.phone1_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14), placeholder_text=self.arabic("أدخل رقم الهاتف"))
        self.phone1_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # هاتف آخر
        CTkLabel(frame, text=self.arabic(":هاتف آخر*"), font=("Arial", 16, "bold"), anchor="e", justify="right").grid(row=row, column=1, sticky="e", pady=(10, 2), padx=(0, 10))
        row += 1
        self.phone2_entry = CTkEntry(frame, width=300, justify="right", font=("Arial", 14), placeholder_text=self.arabic("أدخل رقم هاتف آخر إن وجد*"))
        self.phone2_entry.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1

        # زر التسجيل
        self.register_button = CTkButton(
            frame,
            text=self.arabic("تسجيل"),
            font=("Arial", 18),
            height=40,
            width=200,
            command=self.register_teacher
        )
        self.register_button.grid(row=row, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        row += 1

    def register_teacher(self):
        name = self.name_entry.get().strip()
        nid = self.nid_entry.get().strip()
        term = self.term_var.get().strip()
        gender = self.gender_var.get().strip()
        phone1 = self.phone1_entry.get().strip()
        phone2 = self.phone2_entry.get().strip()

        # تحقق فقط من الحقول الأساسية
        if not name or not nid or (not phone1 and not phone2):
            messagebox.showerror("خطأ", "يجب إدخال اسم المعلمة والرقم القومي ورقم هاتف واحد على الأقل")
            return

        add_teacher(name, nid, term, gender, phone1, phone2)
        messagebox.showinfo("تم", "تم تسجيل المعلمة بنجاح")

        # تفريغ الحقول
        self.name_entry.delete(0, "end")
        self.name_entry.configure(placeholder_text=self.arabic("أدخل الاسم"))
        self.nid_entry.delete(0, "end")
        self.nid_entry.configure(placeholder_text=self.arabic("أدخل الرقم القومي"))
        self.phone1_entry.delete(0, "end")
        self.phone1_entry.configure(placeholder_text=self.arabic("أدخل رقم الهاتف"))
        self.phone2_entry.delete(0, "end")
        self.phone2_entry.configure(placeholder_text=self.arabic("أدخل رقم هاتف آخر إن وجد*"))

    def go_back(self):
        for widget in self.main.winfo_children():
            widget.destroy()
        self.on_back() 