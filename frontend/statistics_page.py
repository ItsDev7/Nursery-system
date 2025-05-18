from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkScrollableFrame
from tkinter import Canvas, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import numpy as np
from backend.database import get_detailed_statistics

class StatisticsPage:
    def __init__(self, main_window, on_back=None):
        self.main = main_window
        self.on_back = on_back
        self.setup_ui()

    def arabic(self, text: str) -> str:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def setup_ui(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        # إطار رئيسي
        self.main_frame = CTkFrame(self.main)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        # زر الرجوع
        back_button = CTkButton(
            self.main_frame,
            text="←",
            font=("Arial", 24, "bold"),
            width=40,
            height=40,
            fg_color="#ff3333",
            text_color="#000000",
            hover_color="#b71c1c",
            corner_radius=20,
            command=self.go_back
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # العنوان
        title = CTkLabel(
            self.main_frame,
            text=self.arabic("الإحصائيات والتقارير"),
            font=("Arial Black", 30),
            text_color="#2D8CFF"
        )
        title.grid(row=0, column=1, pady=(10, 20), sticky="n")

        # الحصول على البيانات
        try:
            self.stats = get_detailed_statistics()
            self.display_statistics()
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء جلب البيانات: {str(e)}")

    def display_statistics(self):
        # إنشاء إطار للملخص العام (placed directly in main_frame)
        summary_frame = CTkFrame(self.main_frame)
        summary_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10) # Adjusted row
        
        # تكوين الأعمدة لتناسب اللغة العربية (من اليمين لليسار)
        summary_frame.grid_columnconfigure(0, weight=1)  # عمود العنوان
        summary_frame.grid_columnconfigure(1, weight=1)  # عمود القيمة
        
        # عنوان الملخص العام
        summary_title = CTkLabel(
            summary_frame,
            text=self.arabic("الملخص العام"),
            font=("Arial", 24, "bold"),
            text_color="#2D8CFF",
            justify="right"
        )
        summary_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="e")
        
        # بيانات الملخص العام
        summary = self.stats["summary"]
        summary_data = [
            ("إجمالي الإيرادات", f"{summary['income']:.2f}"),
            ("إجمالي المصروفات", f"{summary['expenses']:.2f}"),
            ("الرصيد المتبقي", f"{summary['remaining']:.2f}"),
            ("إجمالي رواتب المعلمات", f"{summary['teacher_salaries']:.2f}")
        ]
        
        # إعادة ترتيب الأعمدة لتناسب اللغة العربية (من اليمين لليسار)
        for i, (label, value) in enumerate(summary_data):
            # عمود التسمية مع النقطتين
            CTkLabel(
                summary_frame,
                text=self.arabic(f"{label}:"),
                font=("Arial", 18, "bold"),
                anchor="e",
                justify="right",
                text_color="#2D8CFF"
            ).grid(row=i+1, column=1, padx=10, pady=8, sticky="e")
            
            # عمود القيمة
            CTkLabel(
                summary_frame,
                text=self.arabic(value),
                font=("Arial", 20),
                anchor="w",
                justify="left",
                text_color="#333333"
            ).grid(row=i+1, column=0, padx=10, pady=8, sticky="w")
        
        # إنشاء إطار لإحصائيات المعلمات (placed directly in main_frame)
        teachers_frame = CTkFrame(self.main_frame)
        teachers_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10) # Adjusted row
        
        # تكوين الأعمدة لتناسب اللغة العربية (من اليمين لليسار)
        teachers_frame.grid_columnconfigure(0, weight=1)  # عمود العنوان
        teachers_frame.grid_columnconfigure(1, weight=1)  # عمود القيمة
        
        # عنوان إحصائيات المعلمات
        teachers_title = CTkLabel(
            teachers_frame,
            text=self.arabic("إحصائيات المعلمات"),
            font=("Arial", 24, "bold"),
            text_color="#E91E63",
            justify="right"
        )
        teachers_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="e")
        
        # بيانات المعلمات
        teachers = self.stats["teachers"]
        teachers_data = [
            ("عدد المعلمات", f"{teachers['teacher_count']}"),
            ("إجمالي الرواتب", f"{teachers['total_salaries']:.2f}")
        ]
        
        # إعادة ترتيب الأعمدة لتناسب اللغة العربية (من اليمين لليسار)
        for i, (label, value) in enumerate(teachers_data):
            CTkLabel(
                teachers_frame,
                text=self.arabic(f"{label}:"),
                font=("Arial", 18, "bold"),
                anchor="e",
                justify="right",
                text_color="#E91E63"
            ).grid(row=i+1, column=1, padx=10, pady=8, sticky="e")
            
            CTkLabel(
                teachers_frame,
                text=self.arabic(value),
                font=("Arial", 20),
                anchor="w",
                justify="left",
                text_color="#333333"
            ).grid(row=i+1, column=0, padx=10, pady=8, sticky="w")
        
        # إنشاء إطار لإحصائيات الطلاب حسب الفصل (placed directly in main_frame)
        students_frame = CTkFrame(self.main_frame)
        students_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=10) # Adjusted row
        
        # تكوين الأعمدة لتناسب اللغة العربية (من اليمين لليسار)
        students_frame.grid_columnconfigure(0, weight=1)  # عمود الفصل
        students_frame.grid_columnconfigure(1, weight=1)  # عمود عدد الطلاب
        students_frame.grid_columnconfigure(2, weight=1)  # عمود إجمالي الرسوم
        
        # عنوان إحصائيات الطلاب
        students_title = CTkLabel(
            students_frame,
            text=self.arabic("إحصائيات الطلاب حسب الفصل"),
            font=("Arial", 24, "bold"),
            text_color="#4CAF50",
            justify="right"
        )
        students_title.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="e")
        
        # إعادة ترتيب الأعمدة لتناسب اللغة العربية (من اليمين لليسار)
        # عناوين الأعمدة
        CTkLabel(
            students_frame,
            text=self.arabic("الفصل:"),
            font=("Arial", 18, "bold"),
            justify="right",
            text_color="#4CAF50"
        ).grid(row=1, column=2, padx=10, pady=8, sticky="e")
        
        CTkLabel(
            students_frame,
            text=self.arabic("عدد الطلاب:"),
            font=("Arial", 18, "bold"),
            justify="right",
            text_color="#4CAF50"
        ).grid(row=1, column=1, padx=10, pady=8, sticky="e")
        
        CTkLabel(
            students_frame,
            text=self.arabic("إجمالي الرسوم:"),
            font=("Arial", 18, "bold"),
            justify="right",
            text_color="#4CAF50"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="e")
        
        # بيانات الطلاب حسب الفصل
        students_by_term = self.stats["students_by_term"]
        row_idx = 2
        
        for term, data in students_by_term.items():
            # اسم الفصل (يظهر على اليمين)
            CTkLabel(
                students_frame,
                text=self.arabic(term),
                font=("Arial", 20),
                justify="right",
                text_color="#333333"
            ).grid(row=row_idx, column=2, padx=10, pady=8, sticky="e")
            
            CTkLabel(
                students_frame,
                text=str(data["student_count"]),
                font=("Arial", 20),
                justify="right",
                text_color="#333333"
            ).grid(row=row_idx, column=1, padx=10, pady=8, sticky="e")
            
            CTkLabel(
                students_frame,
                text=f"{data['total_fees']:.2f}",
                font=("Arial", 20),
                justify="right",
                text_color="#333333"
            ).grid(row=row_idx, column=0, padx=10, pady=8, sticky="e")
            
            row_idx += 1
        
        # إنشاء الرسوم البيانية (placed directly in main_frame)
        charts_frame = CTkFrame(self.main_frame)
        charts_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=10) # Adjusted row

        self.create_charts(charts_frame) # Pass the new charts_frame

    def create_charts(self, parent_frame):
        # عنوان الرسوم البيانية
        charts_title = CTkLabel(
            parent_frame,
            text=self.arabic("الرسوم البيانية"),
            font=("Arial", 24, "bold"),
            text_color="#9C27B0",
            justify="right"
        )
        charts_title.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        
        # رسم بياني للإيرادات حسب الفصل
        self.create_term_fees_chart(parent_frame)
        
        # رسم بياني للإيرادات والمصروفات
        self.create_income_expense_chart(parent_frame)

    def create_term_fees_chart(self, parent_frame):
        # إعداد البيانات
        students_by_term = self.stats["students_by_term"]
        terms = list(students_by_term.keys())
        # تحويل أسماء الفصول إلى نصوص عربية صحيحة
        arabic_terms = [self.arabic(term) for term in terms]
        fees = [students_by_term[term]["total_fees"] for term in terms]
        students = [students_by_term[term]["student_count"] for term in terms]
        
        # إنشاء الرسم البياني
        fig, ax1 = plt.subplots(figsize=(8, 4), dpi=100)
        
        # تعيين الخط العربي
        plt.rcParams['font.family'] = 'Arial'
        
        # رسم أعمدة الرسوم
        bars = ax1.bar(arabic_terms, fees, color='#4CAF50', alpha=0.7)
        ax1.set_ylabel(self.arabic('الرسوم'), color='#4CAF50', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='#4CAF50')
        ax1.set_title(self.arabic('الرسوم وعدد الطلاب حسب الفصل'), fontsize=16)
        
        # إضافة محور ثانوي لعدد الطلاب
        ax2 = ax1.twinx()
        # إصلاح الخطأ بإزالة تحديد اللون المكرر
        line = ax2.plot(arabic_terms, students, marker='o', linewidth=2, markersize=8, color='#E91E63')
        ax2.set_ylabel(self.arabic('عدد الطلاب'), color='#E91E63', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='#E91E63')
        
        # تدوير أسماء الفصول لتكون أكثر وضوحًا
        plt.xticks(rotation=45, ha='right')
        
        # إضافة قيم فوق الأعمدة
        for bar, student in zip(bars, students):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.0f}', ha='center', va='bottom', fontsize=8)
            
        fig.tight_layout()
        
        # إضافة الرسم البياني إلى الواجهة
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def create_income_expense_chart(self, parent_frame):
        # إعداد البيانات
        summary = self.stats["summary"]
        labels = ['الإيرادات', 'المصروفات', 'رواتب المعلمات']
        # تحويل التسميات إلى نصوص عربية صحيحة
        arabic_labels = [self.arabic(label) for label in labels]
        values = [summary['income'], summary['expenses'], summary['teacher_salaries']]
        colors = ['#4CAF50', '#F44336', '#E91E63']
        
        # إنشاء الرسم البياني
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        
        # رسم الأعمدة
        bars = ax.bar(arabic_labels, values, color=colors, alpha=0.7)
        
        # إضافة العنوان والمحاور
        ax.set_title(self.arabic('مقارنة الإيرادات والمصروفات'), fontsize=16)
        ax.set_ylabel(self.arabic('القيمة'), fontsize=12)
        
        # إضافة قيم فوق الأعمدة
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{height:.0f}', ha='center', va='bottom', fontsize=10)
        
        fig.tight_layout()
        
        # إضافة الرسم البياني إلى الواجهة
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def go_back(self):
        # تنظيف الرسوم البيانية قبل الإغلاق لتجنب أخطاء التحديث
        plt.close('all')
        
        try:
            # محاولة تنظيف الواجهة بشكل آمن
            for widget in self.main.winfo_children():
                widget.destroy()
                
            if self.on_back:
                self.on_back()
        except Exception as e:
            # تجاهل أخطاء التحديث عند إغلاق التطبيق
            pass