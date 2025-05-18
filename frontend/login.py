from customtkinter import CTkLabel, CTkEntry, CTkFrame, CTkButton
from tkinter import messagebox
from .index import NextPage  # تأكد إن الملف اسمه next_page.py

class Login:
    def __init__(self, main_window):
        self.main = main_window
        self.setup_ui()

    def arabic(self, text: str) -> str:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def setup_ui(self):
        # تنظيف أي عناصر موجودة في النافذة الرئيسية
        for widget in self.main.winfo_children():
            widget.destroy()
            
        # إنشاء إطار متجاوب يتكيف مع حجم الشاشة ويستخدم كامل المساحة
        self.container = CTkFrame(self.main)
        self.container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # تكوين الصفوف والأعمدة في النافذة الرئيسية
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        
        # تكوين الصفوف في الحاوية لتكون متجاوبة
        for i in range(6):
            self.container.grid_rowconfigure(i, weight=1)
        
        # تكوين الأعمدة في الحاوية لتكون متجاوبة
        self.container.grid_columnconfigure(0, weight=1)

        # استخدام حجم خط نسبي يتكيف مع حجم الشاشة
        screen_width = self.main.winfo_width()
        title_font_size = max(24, min(32, int(screen_width / 30)))
        
        title = CTkLabel(
            self.container,
            text=self.arabic("تسجيل الدخول"),
            font=("Arial Black", title_font_size),
            text_color="#2D8CFF"
        )
        title.grid(row=0, column=0, pady=(10, 5), sticky="n")

        username_label = CTkLabel(
            self.container,
            text=self.arabic("اسم المستخدم:"),
            text_color="black",
            font=("Arial", 16, "bold"),
            anchor="e",
            justify="right"
        )
        username_label.grid(row=1, column=0, sticky="e", padx=10, pady=(5, 0))

        # حقل إدخال اسم المستخدم مع عرض متجاوب
        self.username_entry = CTkEntry(
            self.container,
            text_color="black",
            fg_color="white",
            border_color="#2D8CFF",
            font=("Arial", 16),
            width=260,  # سيتم تجاهل هذا بسبب sticky="we"
            corner_radius=8,
            border_width=2,
            height=40
        )
        self.username_entry.grid(row=2, column=0, pady=(2, 10), padx=10, sticky="we")

        password_label = CTkLabel(
            self.container,
            text=self.arabic("كلمة المرور:"),
            text_color="black",
            font=("Arial", 16, "bold"),
            anchor="e",
            justify="right"
        )
        password_label.grid(row=3, column=0, sticky="e", padx=10, pady=(5, 0))

        # حقل إدخال كلمة المرور مع عرض متجاوب
        self.password_entry = CTkEntry(
            self.container,
            show="*",
            text_color="black",
            fg_color="white",
            border_color="#2D8CFF",
            font=("Arial", 16),
            width=260,  # سيتم تجاهل هذا بسبب sticky="we"
            corner_radius=8,
            border_width=2,
            height=40
        )
        self.password_entry.grid(row=4, column=0, pady=(2, 10), padx=10, sticky="we")

        # زر تسجيل الدخول مع عرض متجاوب
        # استخدام نسبة من عرض الشاشة لتحديد عرض الزر
        screen_width = self.main.winfo_width()
        button_width = max(120, min(220, int(screen_width / 5)))
        
        login_button = CTkButton(
            self.container,
            text=self.arabic("تسجيل الدخول"),
            font=("Arial", 18, "bold"),
            height=48,
            width=button_width,
            corner_radius=12,
            fg_color="#2D8CFF",
            hover_color="#1F6BB5",
            command=self.login_clicked
        )
        login_button.grid(row=5, column=0, pady=(10, 15), padx=10, sticky="ew")

    def login_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("خطأ", self.arabic("يرجى إدخال اسم المستخدم وكلمة المرور"))
        elif username != "1" or password != "1":
            messagebox.showerror("خطأ", self.arabic("اسم المستخدم أو كلمة المرور غير صحيحة"))
        else:
            # ✅ إخفاء صفحة الدخول
            self.container.grid_forget()

            # ✅ عرض الصفحة التالية
            NextPage(self.main)
