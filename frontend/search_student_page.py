from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu, CTkScrollableFrame
from tkinter import RIGHT, messagebox
import arabic_reshaper
from bidi.algorithm import get_display
from backend.database import get_all_students, delete_student_by_name, get_all_teachers, get_teacher_salaries  # ✅ استيراد دالة حذف الطالب بالاسم
from .edit_student_page import EditStudentPage
import tkinter as tk  # تأكد أن هذا موجود في الأعلى
import unicodedata
import customtkinter as ctk
from .student_details_popup import StudentDetailsPopup
from .teacher_details_popup import TeacherDetailsPopup

class SearchStudentPage:
    def __init__(self, main_window, on_back=None):
        self.main = main_window
        self.on_back = on_back

        self.mode_var = tk.StringVar(value="الطلاب")
        self.all_students = get_all_students()
        self.all_teachers = get_all_teachers()
        self.students_data = self.all_students.copy()
        self.teachers_data = self.all_teachers.copy()

        self.setup_ui()

    def arabic(self, text: str) -> str:
        return text  
    
    def open_edit_page(self, student_data):
        for widget in self.main.winfo_children():
            widget.destroy()
        EditStudentPage(self.main, student_data, on_back=self.on_back)
    
    def setup_ui(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        frame = CTkFrame(self.main)
        frame.grid(row=0, column=0, sticky="nsew", padx=80, pady=40)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_rowconfigure(3, weight=1)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

        # زر الرجوع في أعلى يسار الصفحة كأيقونة سهم
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

        # اختيار البحث بين الطلاب والمعلمات
        self.mode_menu = CTkOptionMenu(frame, values=["الطلاب", "المعلمات"], variable=self.mode_var, command=lambda _: self.switch_mode())
        self.mode_menu.grid(row=0, column=3, sticky="ne", padx=(0, 10), pady=(0, 10))

        # عنوان الصفحة
        self.title_label = CTkLabel(frame, text=self.arabic("البحث عن " + self.mode_var.get()), font=("Arial", 22, "bold"))
        self.title_label.grid(row=1, column=0, columnspan=4, pady=(0, 20), sticky="n")

        # شريط البحث
        search_frame = CTkFrame(frame)
        search_frame.grid(row=2, column=0, columnspan=4, pady=(0, 15), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=2)
        search_frame.grid_columnconfigure(2, weight=1)

        self.term_var = tk.StringVar(value="الجميع")
        self.term_menu = CTkOptionMenu(
            search_frame,
            values=["الجميع", "التمهيدي", "الاول المستوى", "الثاني المستوى", "الصغار فصل", "يومي اشتراك"],
            variable=self.term_var,
            command=lambda _: self.search_student()
        )
        self.term_menu.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.search_entry = CTkEntry(search_frame, width=200, justify="right", font=("Arial", 16))
        self.search_entry.grid(row=0, column=1, padx=(0, 8), sticky="ew")

        search_button = CTkButton(search_frame, text=self.arabic("بحث"), command=self.search_student, width=80)
        search_button.grid(row=0, column=2, sticky="ew")

        # رأس الجدول
        self.header_frame = CTkFrame(frame, fg_color="#e5e5e5")
        self.header_frame.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(0, 0))
        self.update_table_headers()

        # جسم الجدول (جدول الطلاب أو المعلمات فقط) داخل ScrollableFrame بارتفاع ثابت
        self.body_frame = CTkScrollableFrame(frame, fg_color="#f5f5f5", height=420)
        self.body_frame.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=(0, 10))
        for col in range(4):
            self.body_frame.grid_columnconfigure(col, weight=1)

        self.display_students()

    def go_back(self):
        for widget in self.main.winfo_children():
            widget.destroy()
        self.on_back()

    def switch_mode(self):
        # Update the title label text
        self.title_label.configure(text=self.arabic("البحث عن " + self.mode_var.get()))

        if self.mode_var.get() == "الطلاب":
            self.students_data = get_all_students()
        else:
            self.teachers_data = get_all_teachers()
        self.update_table_headers()
        self.display_students()

    def update_table_headers(self):
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        if self.mode_var.get() == "الطلاب":
            headers = ["الإجراءات", "الفصل الدراسي", "اسم الطالب", "الرقم التسلسلي"]
        else:
            headers = ["الإجراءات", "الفصل الدراسي", "اسم المعلمة", "الرقم التسلسلي"]
        for idx, header in enumerate(headers):
            label = CTkLabel(self.header_frame, text=self.arabic(header), font=("Arial", 16, "bold"), width=120, anchor="center")
            label.grid(row=0, column=idx, sticky="ew", padx=2, pady=2)
            self.header_frame.grid_columnconfigure(idx, weight=1)

    def display_students(self):
        for widget in self.body_frame.winfo_children():
            widget.destroy()
        if self.mode_var.get() == "الطلاب":
            data = self.students_data
        else:
            data = self.teachers_data
        for i, person in enumerate(data):
            row_data = [
                "",  # الإجراءات في الآخر
                person["term"],
                person["name"],
                str(i + 1)
            ]
            for j, item in enumerate(row_data):
                if j == 0:  # الإجراءات
                    action_frame = CTkFrame(self.body_frame)
                    action_frame.grid(row=i, column=0, padx=5)
                    if self.mode_var.get() == "الطلاب":
                        # زر تعديل
                        CTkButton(action_frame, text=self.arabic("تعديل"), fg_color="green", width=50,
                        command=lambda s=person: self.open_edit_page(s)).grid(row=0, column=0, padx=2)
                        # زر حذف
                        delete_button = CTkButton(action_frame, text=self.arabic("حذف"), fg_color="red", width=50,
                                                  command=lambda name=person["name"]: self.delete_student(name))
                        delete_button.grid(row=0, column=1, padx=2)
                        # زر عرض البيانات
                        view_button = CTkButton(action_frame, text=self.arabic("عرض"), fg_color="blue", width=50,
                                                command=lambda s=person: self.show_student_details(s))
                        view_button.grid(row=0, column=2, padx=2)
                    else:
                        # زر تعديل للمعلمة
                        CTkButton(action_frame, text=self.arabic("تعديل"), fg_color="green", width=50,
                        command=lambda t=person: self.edit_teacher_popup(t)).grid(row=0, column=0, padx=2)
                        # زر حذف للمعلمة
                        delete_button = CTkButton(action_frame, text=self.arabic("حذف"), fg_color="red", width=50,
                                                  command=lambda name=person["name"]: self.delete_teacher(name))
                        delete_button.grid(row=0, column=1, padx=2)
                        # زر عرض بيانات المعلمة
                        view_button = CTkButton(action_frame, text=self.arabic("عرض"), fg_color="blue", width=50,
                                                command=lambda t=person: self.show_teacher_details(t))
                        view_button.grid(row=0, column=2, padx=2)
                        # زر إضافة مرتب
                        salary_button = CTkButton(action_frame, text=self.arabic("إضافة مرتب"), fg_color="#E91E63", width=70,
                                                  command=lambda t=person: self.add_salary_popup(t))
                        salary_button.grid(row=0, column=3, padx=2)
                else:
                    CTkLabel(self.body_frame, text=item, width=120).grid(row=i, column=j, padx=2, pady=2)

    def show_student_details(self, student):
        StudentDetailsPopup(self.main, student)

    def show_teacher_details(self, teacher):
        TeacherDetailsPopup(self.main, teacher)

    def search_student(self):
        query = self.search_entry.get().strip()
        selected_term = self.term_menu.get()

        if self.mode_var.get() == "الطلاب":
            filtered = self.all_students
            # نفلتر حسب البحث إن وُجد
            if query:
                query_normalized = self.normalize_arabic(query)
                filtered = [
                    s for s in filtered
                    if query_normalized in self.normalize_arabic(s["name"]) or query_normalized in s["nid"]
                ]
            # نفلتر حسب الفصل الدراسي إن لم يكن "الجميع"
            if selected_term != "الجميع":
                filtered = [
                    s for s in filtered
                    if s["term"] == selected_term
                ]
            self.students_data = filtered
        else:
            filtered = self.all_teachers
            # نفلتر حسب البحث إن وُجد
            if query:
                query_normalized = self.normalize_arabic(query)
                filtered = [
                    t for t in filtered
                    if query_normalized in self.normalize_arabic(t["name"]) or query_normalized in t["nid"]
                ]
            # نفلتر حسب الفصل الدراسي إن لم يكن "الجميع"
            if selected_term != "الجميع":
                filtered = [
                    t for t in filtered
                    if t["term"] == selected_term
                ]
            self.teachers_data = filtered
        self.display_students()

    def normalize_arabic(self, text: str) -> str:
        # تحويل النص إلى صيغة موحدة
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

    def delete_student(self, name: str):
        # تأكيد الحذف
        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب؟")
        if not result:
            return
        # حذف الطالب من قاعدة البيانات
        delete_student_by_name(name)

        # إعادة تحميل البيانات بعد الحذف
        self.all_students = get_all_students()
        self.students_data = self.all_students.copy()
        self.display_students()

    def delete_teacher(self, name: str):
        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذه المعلمة؟")
        if not result:
            return
        conn = __import__('backend.database').database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers WHERE name = ?", (name,))
        conn.commit()
        conn.close()
        self.all_teachers = get_all_teachers()
        self.teachers_data = self.all_teachers.copy()
        self.display_students()

    def add_salary_popup(self, teacher):
        import customtkinter as ctk
        from datetime import datetime
        from backend.database import add_teacher_salary, get_all_teachers
        salary_win = ctk.CTkToplevel(self.main)
        salary_win.title("إضافة مرتب")
        salary_win.geometry("350x270")
        salary_win.resizable(False, False)
        salary_win.lift()
        salary_win.grab_set()
        salary_win.focus_force()
        frame = ctk.CTkFrame(salary_win)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(frame, text="إضافة مرتب للمعلمة:", font=("Arial", 16, "bold"), text_color="#E91E63").pack(pady=(0, 10))
        amount_var = ctk.StringVar()
        date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ctk.CTkLabel(frame, text="المبلغ:", font=("Arial", 14)).pack(anchor="e")
        amount_entry = ctk.CTkEntry(frame, textvariable=amount_var, font=("Arial", 14), justify="right")
        amount_entry.pack(fill="x", pady=5)
        ctk.CTkLabel(frame, text="التاريخ:", font=("Arial", 14)).pack(anchor="e")
        date_entry = ctk.CTkEntry(frame, textvariable=date_var, font=("Arial", 14), justify="right")
        date_entry.pack(fill="x", pady=5)
        def save_salary():
            try:
                amount = float(amount_var.get())
            except ValueError:
                from tkinter import messagebox
                messagebox.showerror("خطأ", "المبلغ يجب أن يكون رقمًا")
                return
            if not amount_var.get():
                from tkinter import messagebox
                messagebox.showerror("خطأ", "يرجى إدخال مبلغ المرتب")
                return
            add_teacher_salary(teacher["id"], amount, date_var.get())
            from tkinter import messagebox
            messagebox.showinfo("تم", "تمت إضافة المرتب بنجاح")
            salary_win.destroy()
        btns = ctk.CTkFrame(frame)
        btns.pack(fill="x", pady=10)
        ctk.CTkButton(btns, text="إضافة", fg_color="#4CAF50", text_color="#fff", font=("Arial", 14, "bold"), command=save_salary).pack(side="right", padx=8, pady=2, ipadx=10, ipady=4)
        ctk.CTkButton(btns, text="إلغاء", fg_color="#ff3333", text_color="#fff", font=("Arial", 14, "bold"), command=salary_win.destroy).pack(side="right", padx=8, pady=2, ipadx=10, ipady=4)
        salary_win.protocol("WM_DELETE_WINDOW", salary_win.destroy)

    def edit_teacher_popup(self, teacher):
        # Placeholder for edit teacher logic
        from tkinter import messagebox
        messagebox.showinfo("تعديل المعلمة", "سيتم تنفيذ صفحة التعديل لاحقًا")
