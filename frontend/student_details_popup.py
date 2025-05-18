import customtkinter as ctk

class StudentDetailsPopup:
    def __init__(self, main, student, on_close=None):
        self.main = main
        self.student = student
        self.on_close = on_close
        self.details_window = None
        self.show()

    def show(self):
        if self.details_window is not None and self.details_window.winfo_exists():
            self.details_window.focus_force()
            return
        self.details_window = ctk.CTkToplevel(self.main)
        self.details_window.title("تفاصيل الطالب")
        self.details_window.geometry("420x500")
        self.details_window.resizable(False, False)
        frame = ctk.CTkFrame(self.details_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(
            frame, 
            text="معلومات الطالب", 
            font=("Arial", 20, "bold"),
            text_color="#2D8CFF"
        )
        title_label.pack(pady=(0, 15))
        info = [
            ("👤", f"الاسم: {self.student['name']}"),
            ("🧾", f"الرقم القومي: {self.student['nid']}"),
            ("🏫", f"الفصل الدراسي: {self.student['term']}"),
            ("⚧", f"الجنس: {self.student['gender']}"),
            ("📞", f"هاتف ولي الأمر: {self.student['phone1']}"),
            ("📞", f"هاتف ولي أمر آخر: {self.student['phone2']}")
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
        fees_title = ctk.CTkLabel(
            frame, 
            text="الرسوم", 
            font=("Arial", 18, "bold"),
            text_color="#4CAF50"
        )
        fees_title.pack(pady=(15, 10))
        fee_names = [
            "القسط الأول", "القسط الثاني", "القسط الثالث", "الملابس أو القسط الرابع*"
        ]
        fees = [self.student.get(f"fee{i+1}", "") for i in range(4)]
        fee_dates = [self.student.get(f"fee{i+1}_date", "") for i in range(4)]
        for i in range(4):
            row_fee = ctk.CTkFrame(frame, fg_color="transparent")
            row_fee.pack(fill="x", pady=2)
            ctk.CTkLabel(
                row_fee, 
                text=f"{fee_names[i]}:", 
                font=("Arial", 15, "bold"), 
                width=120, 
                anchor="e"
            ).pack(side="right")
            ctk.CTkLabel(
                row_fee, 
                text=f"{fees[i]}", 
                font=("Arial", 15), 
                width=60, 
                anchor="e",
                text_color="#2D8CFF"
            ).pack(side="right", padx=(0, 10))
            ctk.CTkLabel(
                row_fee, 
                text=f"التاريخ: {fee_dates[i]}", 
                font=("Arial", 14), 
                anchor="e",
                text_color="#666666"
            ).pack(side="right", padx=(0, 10))
        def close_window():
            self.details_window.destroy()
            self.details_window = None
            if self.on_close:
                self.on_close()
            self.main.focus_force()
        ctk.CTkButton(
            frame, 
            text="إغلاق", 
            fg_color="#ff3333", 
            text_color="#fff", 
            hover_color="#b71c1c", 
            font=("Arial", 16, "bold"),
            height=40,
            command=close_window
        ).pack(pady=15)
        self.details_window.protocol("WM_DELETE_WINDOW", close_window)
        self.details_window.lift()
        self.details_window.grab_set()
        self.details_window.focus_force()