"""
Main application window and navigation.
"""
import customtkinter as ctk
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage, CTkScrollableFrame, CTkProgressBar, CTkEntry
from PIL import Image
import os
from pathlib import Path
import sqlite3
from .register_student_page import RegisterStudentPage
from .fees.views import FeesPage
from .register_teacher_page import RegisterTeacherPage
from .statistics_page import StatisticsPage
from backend.database import get_all_activities, add_activity, update_activity, delete_activity
from datetime import datetime
from tkinter import messagebox
from .person_management.search_page import SearchPage
from .person_management.edit_pages.student_edit import EditStudentPage
from .person_management.edit_pages.teacher_edit import EditTeacherPage
from .person_management.student_details_popup import StudentDetailsPopup
from .person_management.teacher_details_popup import TeacherDetailsPopup

class NextPage:
    def __init__(self, main_window):
        self.main = main_window
        self.current_page = None
        self.setup_ui()

    def arabic(self, text: str) -> str:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def open_register_student_page(self):
        self.clear_content_frame()
        self.current_page = RegisterStudentPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("register_student")

    def open_search_student_page(self):
        self.clear_content_frame()
        self.current_page = SearchPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("search")

    def open_fees_page(self):
        self.clear_content_frame()
        self.current_page = FeesPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("fees")

    def open_register_teacher_page(self):
        self.clear_content_frame()
        self.current_page = RegisterTeacherPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("register_teacher")
        
    def open_statistics_page(self):
        self.clear_content_frame()
        self.current_page = StatisticsPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("statistics")
    
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def highlight_active_nav_button(self, active_button_id):
        # إعادة تعيين جميع الأزرار إلى اللون الافتراضي
        for button_id, button in self.nav_buttons.items():
            if button_id == active_button_id:
                button.configure(fg_color="#3489f1")  # Active color from screenshot
            else:
                button.configure(fg_color="#4A90E2")  # Default color from screenshot
    
    def show_dashboard(self):
        self.clear_content_frame()
        self.create_dashboard()
        self.highlight_active_nav_button("dashboard")

    def get_statistics(self):
        # الحصول على إحصائيات من قاعدة البيانات
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            
            # عدد الطلاب
            cursor.execute("SELECT COUNT(*) FROM students")
            students_count = cursor.fetchone()[0]
            
            # عدد المعلمات
            cursor.execute("SELECT COUNT(*) FROM teachers")
            teachers_count = cursor.fetchone()[0]
            
            # إجمالي الإيرادات
            cursor.execute("SELECT SUM(amount) FROM income")
            result = cursor.fetchone()[0]
            total_income = result if result is not None else 0
            
            # إجمالي المصروفات
            cursor.execute("SELECT SUM(amount) FROM general_expenses")
            result = cursor.fetchone()[0]
            total_expenses = result if result is not None else 0
            
            conn.close()
            
            return {
                "students": students_count,
                "teachers": teachers_count,
                "income": total_income,
                "expenses": total_expenses
            }
        except Exception as e:
            print(f"خطأ في الحصول على الإحصائيات: {e}")
            # قيم افتراضية في حالة حدوث خطأ
            return {
                "students": 0,
                "teachers": 0,
                "income": 0,
                "expenses": 0
            }
    
    def create_dashboard(self):
        # إنشاء لوحة المعلومات
        dashboard_frame = CTkFrame(self.content_frame, fg_color="transparent")
        dashboard_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # تكوين الصفوف والأعمدة في لوحة المعلومات
        dashboard_frame.grid_columnconfigure(0, weight=1)
        dashboard_frame.grid_columnconfigure(1, weight=1)
        dashboard_frame.grid_columnconfigure(2, weight=1)
        
        # تكوين الصفوف
        for i in range(6):
            dashboard_frame.grid_rowconfigure(i, weight=1)
        
        # العنوان الرئيسي
        header_frame = CTkFrame(dashboard_frame, fg_color="#1F6BB5", corner_radius=10)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=(5, 15))
        
        title = CTkLabel(
            header_frame,
            text=self.arabic("لوحة معلومات حضانة الندى"),
            font=("Arial Black", 32),
            text_color="white"
        )
        title.pack(pady=20)
        
        # الحصول على الإحصائيات
        stats = self.get_statistics()
        
        # صف البطاقات الرئيسية
        self.create_stat_card(
            dashboard_frame, 1, 0,
            self.arabic("عدد الطلاب"),
            str(stats["students"]),
            "#4CAF50",
            "👨‍🎓"
        )
        
        self.create_stat_card(
            dashboard_frame, 1, 1,
            self.arabic("عدد المعلمات"),
            str(stats["teachers"]),
            "#E91E63",
            "👩‍🏫"
        )
        
        # إضافة بطاقة جديدة للنسبة بين الطلاب والمعلمات
        ratio = stats["students"] / stats["teachers"] if stats["teachers"] > 0 else 0
        self.create_stat_card(
            dashboard_frame, 1, 2,
            self.arabic("نسبة الطلاب/المعلمات"),
            f"{ratio:.1f}",
            "#3F51B5",
            "📊"
        )
        
        # صف البطاقات المالية
        self.create_stat_card(
            dashboard_frame, 2, 0,
            self.arabic("إجمالي الإيرادات"),
            f"{stats['income']} ج.م",
            "#FF9800",
            "💰"
        )
        
        self.create_stat_card(
            dashboard_frame, 2, 1,
            self.arabic("إجمالي المصروفات"),
            f"{stats['expenses']} ج.م",
            "#9C27B0",
            "💸"
        )
        
        # إضافة بطاقة جديدة للربح الصافي
        net_profit = stats["income"] - stats["expenses"]
        profit_color = "#4CAF50" if net_profit >= 0 else "#F44336"
        self.create_stat_card(
            dashboard_frame, 2, 2,
            self.arabic("صافي الربح"),
            f"{net_profit} ج.م",
            profit_color,
            "📈"
        )
        
        # إضافة رسم بياني للإيرادات والمصروفات
        chart_frame = CTkFrame(dashboard_frame, fg_color="white", corner_radius=10)
        chart_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        
        chart_title = CTkLabel(
            chart_frame,
            text=self.arabic("مقارنة الإيرادات والمصروفات"),
            font=("Arial", 20, "bold"),
            text_color="#333"
        )
        chart_title.pack(pady=(15, 10))
        
        # إنشاء رسم بياني بسيط باستخدام أشرطة التقدم
        chart_container = CTkFrame(chart_frame, fg_color="transparent")
        chart_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # تكوين الأعمدة في حاوية الرسم البياني
        chart_container.grid_columnconfigure(0, weight=1)  # عمود العناوين
        chart_container.grid_columnconfigure(1, weight=4)  # عمود شريط التقدم
        chart_container.grid_columnconfigure(2, weight=1)  # عمود القيم
        
        # شريط الإيرادات
        income_label = CTkLabel(chart_container, text=self.arabic("الإيرادات:"), font=("Arial", 16, "bold"))
        income_label.grid(row=0, column=2, sticky="e", pady=8)
        
        max_value = max(stats["income"], stats["expenses"]) if max(stats["income"], stats["expenses"]) > 0 else 1
        income_progress = CTkProgressBar(chart_container, width=500, height=30, corner_radius=5)
        income_progress.grid(row=0, column=1, padx=10, pady=8)
        income_progress.set(stats["income"] / max_value if max_value > 0 else 0)
        income_progress.configure(progress_color="#FF9800")
        
        income_value = CTkLabel(chart_container, text=f"{stats['income']} ج.م", font=("Arial", 16, "bold"))
        income_value.grid(row=0, column=0, sticky="w", pady=8)
        
        # شريط المصروفات
        expenses_label = CTkLabel(chart_container, text=self.arabic("المصروفات:"), font=("Arial", 16, "bold"))
        expenses_label.grid(row=1, column=2, sticky="e", pady=8)
        
        expenses_progress = CTkProgressBar(chart_container, width=500, height=30, corner_radius=5)
        expenses_progress.grid(row=1, column=1, padx=10, pady=8)
        expenses_progress.set(stats["expenses"] / max_value if max_value > 0 else 0)
        expenses_progress.configure(progress_color="#9C27B0")
        
        expenses_value = CTkLabel(chart_container, text=f"{stats['expenses']} ج.م", font=("Arial", 16, "bold"))
        expenses_value.grid(row=1, column=0, sticky="w", pady=8)
        
        # شريط صافي الربح
        profit_label = CTkLabel(chart_container, text=self.arabic("صافي الربح:"), font=("Arial", 16, "bold"))
        profit_label.grid(row=2, column=2, sticky="e", pady=8)
        
        profit_progress = CTkProgressBar(chart_container, width=500, height=30, corner_radius=5)
        profit_progress.grid(row=2, column=1, padx=10, pady=8)
        profit_value_normalized = abs(net_profit) / max_value if max_value > 0 else 0
        profit_progress.set(profit_value_normalized)
        profit_progress.configure(progress_color=profit_color)
        
        profit_value = CTkLabel(chart_container, text=f"{net_profit} ج.م", font=("Arial", 16, "bold"))
        profit_value.grid(row=2, column=0, sticky="w", pady=8)
        
        # تقسيم المعلومات والأنشطة إلى عمودين
        info_activities_frame = CTkFrame(dashboard_frame, fg_color="transparent")
        info_activities_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        info_activities_frame.grid_columnconfigure(0, weight=1)
        info_activities_frame.grid_columnconfigure(1, weight=1)
        
        # معلومات الحضانة
        info_frame = CTkFrame(info_activities_frame, fg_color="#f0f0f0", corner_radius=10)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        info_title = CTkLabel(
            info_frame,
            text=self.arabic("معلومات عن حضانة الندى"),
            font=("Arial", 20, "bold"),
            text_color="#333"
        )
        info_title.pack(pady=(15, 5))
        
        info_text = CTkLabel(
            info_frame,
            text=self.arabic("حضانة الندى هي مؤسسة تعليمية متميزة تهدف إلى تنمية مهارات الأطفال وتطوير قدراتهم في بيئة آمنة ومحفزة للإبداع. نقدم برامج تعليمية متنوعة تناسب مختلف الأعمار والقدرات، مع التركيز على تنمية المهارات الاجتماعية والإبداعية والذهنية."),
            font=("Arial", 16),
            text_color="#333",
            wraplength=500
        )
        info_text.pack(pady=(5, 15), padx=20, fill="both", expand=True)
        
        # إضافة قسم للإعلانات والأنشطة القادمة
        activities_frame = CTkFrame(info_activities_frame, fg_color="#E3F2FD", corner_radius=10)
        activities_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        activities_title = CTkLabel(
            activities_frame,
            text=self.arabic("الأنشطة القادمة"),
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        )
        activities_title.pack(pady=(15, 10), anchor="n")
        
        # Input fields for new activity
        input_frame = CTkFrame(activities_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        CTkLabel(input_frame, text=self.arabic("الوصف:"), font=("Arial", 14), anchor="e").grid(row=0, column=1, sticky="e", padx=5)
        self.activity_description_entry = CTkEntry(input_frame, font=("Arial", 14), justify="right")
        self.activity_description_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)

        CTkLabel(input_frame, text=self.arabic("التاريخ:"), font=("Arial", 14), anchor="e").grid(row=2, column=1, sticky="e", padx=5)
        self.activity_date_entry = CTkEntry(input_frame, font=("Arial", 14), justify="right", placeholder_text=self.arabic("YYYY-MM-DD"))
        self.activity_date_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5)

        add_activity_button = CTkButton(activities_frame, text=self.arabic("إضافة نشاط"), font=("Arial", 14, "bold"), command=self.add_new_activity)
        add_activity_button.pack(pady=(0, 10))

        # Scrollable frame to display activities
        self.activities_display_frame = CTkScrollableFrame(activities_frame, fg_color="transparent", height=200)
        self.activities_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.activities_display_frame.grid_columnconfigure(0, weight=1)

        self.load_activities()

    def create_stat_card(self, parent, row, col, title, value, color, icon=None):
        # إنشاء بطاقة إحصائية
        card = CTkFrame(parent, fg_color="white", corner_radius=10)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # تكوين الصفوف والأعمدة في البطاقة
        card.grid_rowconfigure(0, weight=0)  # صف العنوان
        card.grid_rowconfigure(1, weight=0)  # صف الأيقونة
        card.grid_rowconfigure(2, weight=1)  # صف القيمة
        card.grid_columnconfigure(0, weight=1)
        
        # إضافة خط ملون في أعلى البطاقة
        color_bar = CTkFrame(card, fg_color=color, height=8, corner_radius=5)
        color_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        
        # عنوان البطاقة
        card_title = CTkLabel(
            card,
            text=title,
            font=("Arial", 18, "bold"),
            text_color="#333"
        )
        card_title.grid(row=0, column=0, pady=(15, 5), sticky="n")
        
        # أيقونة البطاقة (إذا تم توفيرها)
        if icon:
            icon_label = CTkLabel(
                card,
                text=icon,
                font=("Arial", 42),
                text_color=color
            )
            icon_label.grid(row=1, column=0, pady=(5, 5), sticky="n")
        
        # قيمة البطاقة
        card_value = CTkLabel(
            card,
            text=value,
            font=("Arial", 32, "bold"),
            text_color=color
        )
        card_value.grid(row=2, column=0, pady=(5, 15), sticky="n")

    def setup_ui(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        # إنشاء الإطار الرئيسي الذي يستخدم كامل مساحة النافذة
        main_frame = CTkFrame(self.main, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        
        # تكوين الصفوف والأعمدة في الإطار الرئيسي
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0, minsize=150)  # Increased sidebar width
        
        # إنشاء شريط التنقل الجانبي
        sidebar = CTkFrame(main_frame, fg_color="#4A90E2", corner_radius=0, width=150)
        sidebar.grid(row=0, column=1, sticky="nsew")
        sidebar.grid_propagate(False)  # منع تغيير حجم الشريط الجانبي
        
        # تكوين الصفوف في شريط التنقل
        for i in range(7):
            sidebar.grid_rowconfigure(i, weight=0)
        sidebar.grid_rowconfigure(7, weight=1)  # مساحة فارغة في الأسفل
        sidebar.grid_columnconfigure(0, weight=1)
        
        # عنوان شريط التنقل
        logo_label = CTkLabel(
            sidebar,
            text=self.arabic("حضانة الندى"),
            font=("Arial Black", 20),
            text_color="white"
        )
        logo_label.grid(row=0, column=0, pady=(20, 30), padx=10, sticky="ne")
        
        # أزرار التنقل
        self.nav_buttons = {}
        
        # زر لوحة المعلومات
        dashboard_button = CTkButton(
            sidebar,
            text=self.arabic("لوحة المعلومات"),
            font=("Arial", 14, "bold"),
            fg_color="#3489f1",
            hover_color="#2970c2",
            corner_radius=0,
            anchor="e",
            height=40,
            command=self.show_dashboard
        )
        dashboard_button.grid(row=1, column=0, padx=10, sticky="ew")
        self.nav_buttons["dashboard"] = dashboard_button
        
        # زر تسجيل طالب جديد
        register_student_button = CTkButton(
            sidebar,
            text=self.arabic("تسجيل طالب جديد"),
            font=("Arial", 14, "bold"),
            fg_color="#4A90E2",
            hover_color="#3489f1",
            corner_radius=0,
            anchor="e",
            height=40,
            command=self.open_register_student_page
        )
        register_student_button.grid(row=2, column=0, padx=10, sticky="ew")
        self.nav_buttons["register_student"] = register_student_button
        
        # زر تسجيل معلمة جديدة
        register_teacher_button = CTkButton(
            sidebar,
            text=self.arabic("تسجيل معلمة جديدة"),
            font=("Arial", 14, "bold"),
            fg_color="#4A90E2",
            hover_color="#3489f1",
            corner_radius=0,
            anchor="e",
            height=40,
            command=self.open_register_teacher_page
        )
        register_teacher_button.grid(row=3, column=0, padx=10, sticky="ew")
        self.nav_buttons["register_teacher"] = register_teacher_button
        
        # زر البحث
        search_button = CTkButton(
            sidebar,
            text=self.arabic("البحث عن طالب / معلمة"),
            font=("Arial", 14, "bold"),
            fg_color="#4A90E2",
            hover_color="#3489f1",
            corner_radius=0,
            anchor="e",
            height=40,
            command=self.open_search_student_page
        )
        search_button.grid(row=4, column=0, padx=10, sticky="ew")
        self.nav_buttons["search"] = search_button
        
        # زر المصروفات
        fees_button = CTkButton(
            sidebar,
            text=self.arabic("المصروفات والإيرادات"),
            font=("Arial", 14, "bold"),
            fg_color="#4A90E2",
            hover_color="#3489f1",
            corner_radius=0,
            anchor="e",
            height=40,
            command=self.open_fees_page
        )
        fees_button.grid(row=5, column=0, padx=10, sticky="ew")
        self.nav_buttons["fees"] = fees_button
        
        # زر الإحصائيات
        statistics_button = CTkButton(
            sidebar,
            text=self.arabic("الإحصائيات والتقارير"),
            font=("Arial", 14, "bold"),
            fg_color="#4A90E2",
            hover_color="#3489f1",
            corner_radius=0,
            anchor="e",
            height=40,
            command=self.open_statistics_page
        )
        statistics_button.grid(row=6, column=0, padx=10, sticky="ew")
        self.nav_buttons["statistics"] = statistics_button
        
        # إطار المحتوى الرئيسي
        content_container = CTkFrame(main_frame, fg_color="#f5f5f5", corner_radius=0)
        content_container.grid(row=0, column=0, sticky="nsew")
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_columnconfigure(0, weight=1)
        
        # إنشاء المحتوى الرئيسي (استخدام CTkFrame بدلاً من CTkScrollableFrame)
        self.content_frame = CTkScrollableFrame(content_container, fg_color="#f5f5f5")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # عرض لوحة المعلومات الافتراضية
        self.show_dashboard()

    def load_activities(self):
        # Clear existing activities
        for widget in self.activities_display_frame.winfo_children():
            widget.destroy()

        activities = get_all_activities()

        if not activities:
            CTkLabel(self.activities_display_frame, text=self.arabic("لا يوجد أنشطة قادمة حاليًا."), font=("Arial", 14), text_color="#555").pack(pady=10)
            return

        for activity_id, description, date in activities:
            activity_frame = CTkFrame(self.activities_display_frame, fg_color="#BBDEFB", corner_radius=8)
            activity_frame.pack(fill="x", pady=4)
            activity_frame.grid_columnconfigure(0, weight=1) # Description column
            activity_frame.grid_columnconfigure(1, weight=0) # Buttons column

            # Description and Date
            desc_date_frame = CTkFrame(activity_frame, fg_color="transparent")
            desc_date_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
            desc_date_frame.grid_columnconfigure(0, weight=1)

            CTkLabel(desc_date_frame, text=self.arabic(f"الوصف: {description}"), font=("Arial", 14), anchor="e").pack(fill="x")
            CTkLabel(desc_date_frame, text=self.arabic(f"التاريخ: {date}"), font=("Arial", 12), anchor="e", text_color="#555").pack(fill="x")

            # Buttons (Edit and Delete)
            buttons_frame = CTkFrame(activity_frame, fg_color="transparent")
            buttons_frame.grid(row=0, column=1, sticky="e", padx=10, pady=5)

            delete_button = CTkButton(
                buttons_frame,
                text="✖",
                width=30,
                height=30,
                fg_color="red",
                text_color="white",
                command=lambda a_id=activity_id: self.confirm_delete_activity(a_id)
            )
            delete_button.pack(side="right", padx=5)

            edit_button = CTkButton(
                buttons_frame,
                text="✎",
                width=30,
                height=30,
                fg_color="orange",
                text_color="white",
                command=lambda a_id=activity_id, desc=description, dt=date: self.open_edit_activity_window(a_id, desc, dt)
            )
            edit_button.pack(side="right", padx=5)

    def add_new_activity(self):
        description = self.activity_description_entry.get().strip()
        date = self.activity_date_entry.get().strip()

        if not description or not date:
            from tkinter import messagebox
            messagebox.showerror("خطأ", self.arabic("يرجى إدخال الوصف والتاريخ للنشاط."))
            return

        # Basic date format validation (YYYY-MM-DD)
        try:
            datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("خطأ", self.arabic("صيغة التاريخ غير صحيحة. يرجى استخدام DD-MM-YYYY."))
            return

        add_activity(description, date)
        self.activity_description_entry.delete(0, "end")
        self.activity_date_entry.delete(0, "end")
        self.load_activities()

    def confirm_delete_activity(self, activity_id):
        from tkinter import messagebox
        result = messagebox.askyesno(self.arabic("تأكيد الحذف"), self.arabic("هل أنت متأكد أنك تريد حذف هذا النشاط؟"))
        if result:
            delete_activity(activity_id)
            self.load_activities()

    def open_edit_activity_window(self, activity_id, description, date):
        import customtkinter as ctk
        edit_window = ctk.CTkToplevel(self.main)
        edit_window.title(self.arabic("تعديل النشاط"))
        edit_window.geometry("400x250")
        edit_window.transient(self.main) # Keep window on top of main window
        edit_window.grab_set() # Modal window

        frame = ctk.CTkFrame(edit_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        CTkLabel(frame, text=self.arabic("الوصف الجديد:"), font=("Arial", 14), anchor="e").grid(row=0, column=1, sticky="e", padx=5, pady=(0,2))
        desc_entry = ctk.CTkEntry(frame, font=("Arial", 14), justify="right")
        desc_entry.insert(0, description)
        desc_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0,10))

        CTkLabel(frame, text=self.arabic("التاريخ الجديد:"), font=("Arial", 14), anchor="e").grid(row=2, column=1, sticky="e", padx=5, pady=(0,2))
        date_entry = ctk.CTkEntry(frame, font=("Arial", 14), justify="right", placeholder_text=self.arabic("YYYY-MM-DD"))
        date_entry.insert(0, date)
        date_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(0,10))

        def save_edit():
            new_desc = desc_entry.get().strip()
            new_date = date_entry.get().strip()

            if not new_desc or not new_date:
                messagebox.showerror("خطأ", self.arabic("يرجى إدخال كل الحقول."), parent=edit_window)
                return

            try:
                datetime.strptime(new_date, '%d-%m-%Y')
            except ValueError:
                messagebox.showerror("خطأ", self.arabic("صيغة التاريخ غير صحيحة. يرجى استخدام DD-MM-YYYY."), parent=edit_window)
                return

            update_activity(activity_id, new_desc, new_date)
            self.load_activities()
            edit_window.destroy()

        save_button = ctk.CTkButton(frame, text=self.arabic("حفظ"), font=("Arial", 14, "bold"), command=save_edit)
        save_button.grid(row=4, column=0, sticky="e", padx=5)

        cancel_button = ctk.CTkButton(frame, text=self.arabic("إلغاء"), font=("Arial", 14, "bold"), command=edit_window.destroy)
        cancel_button.grid(row=4, column=1, sticky="w", padx=5)