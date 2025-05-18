import customtkinter as ctk
from backend.database import get_teacher_salaries

class TeacherDetailsPopup:
    def __init__(self, main, teacher, on_close=None):
        self.main = main
        self.teacher = teacher
        self.on_close = on_close
        self.details_window = None
        self.show()

    def show(self):
        if self.details_window is not None and self.details_window.winfo_exists():
            self.details_window.focus_force()
            return
        self.details_window = ctk.CTkToplevel(self.main)
        self.details_window.title("تفاصيل المعلمة")
        self.details_window.geometry("420x420")
        self.details_window.resizable(False, False)
        frame = ctk.CTkFrame(self.details_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(
            frame, 
            text="معلومات المعلمة", 
            font=("Arial", 20, "bold"),
            text_color="#E91E63"
        )
        title_label.pack(pady=(0, 15))
        info = [
            ("👤", f"الاسم: {self.teacher['name']}"),
            ("🧾", f"الرقم القومي: {self.teacher['nid']}"),
            ("🏫", f"الفصل الدراسي: {self.teacher['term']}"),
            ("⚧", f"الجنس: {self.teacher['gender']}"),
            ("📞", f"هاتف: {self.teacher['phone1']}"),
            ("📞", f"هاتف آخر: {self.teacher['phone2']}")
        ]
        for i, (icon, text) in enumerate(info):
            row_frame = ctk.CTkFrame(frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=3)
            ctk.CTkLabel(
                row_frame, 
                text=icon, 
                font=("Arial", 20), 
                width=30, 
                anchor="e"
            ).pack(side="right")
            ctk.CTkLabel(
                row_frame, 
                text=text, 
                font=("Arial", 16), 
                anchor="e", 
                justify="right"
            ).pack(side="right", fill="x", expand=True)
        ctk.CTkLabel(
            frame, text="المرتبات:", 
            font=("Arial", 15, "bold"), 
            text_color="#4CAF50"
        ).pack(pady=(15, 2), anchor="e")

        # Scrollable Frame للمرتبات
        salary_scroll_frame = ctk.CTkScrollableFrame(frame, fg_color="#f5f5f5", height=150)
        salary_scroll_frame.pack(fill="x", pady=(0, 10))

        # العناوين
        ctk.CTkLabel(salary_scroll_frame, text="المبلغ", font=("Arial", 13, "bold"), width=80).grid(row=0, column=0, padx=4, pady=2)
        ctk.CTkLabel(salary_scroll_frame, text="التاريخ", font=("Arial", 13, "bold"), width=120).grid(row=0, column=1, padx=4, pady=2)
        salaries = get_teacher_salaries(self.teacher['id'])  # أو self.teacher['nid'] حسب تصميمك

        # البيانات
        for idx, (amount, date) in enumerate(salaries, start=1):
            ctk.CTkLabel(salary_scroll_frame, text=str(amount), font=("Arial", 13), width=80).grid(row=idx, column=0, padx=4, pady=2)
            ctk.CTkLabel(salary_scroll_frame, text=date, font=("Arial", 13), width=120).grid(row=idx, column=1, padx=4, pady=2)

        def close_window():
            self.details_window.destroy()
            self.details_window = None
            if self.on_close:
                self.on_close()
            self.main.focus_force()
        ctk.CTkButton(frame, text="إغلاق", fg_color="#ff3333", text_color="#fff", hover_color="#b71c1c", font=("Arial", 14, "bold"), command=close_window).pack(pady=15)
        self.details_window.protocol("WM_DELETE_WINDOW", close_window)
        self.details_window.lift()
        self.details_window.grab_set()
        self.details_window.focus_force()