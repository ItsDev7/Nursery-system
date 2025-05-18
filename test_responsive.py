# اختبار استجابة التطبيق لمختلف أحجام الشاشة

import tkinter as tk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton
import time

def test_responsive_behavior():
    """اختبار استجابة التطبيق لتغيير حجم النافذة"""
    app = CTk()
    app.title("اختبار الاستجابة")
    
    # إنشاء إطار رئيسي
    main_frame = CTkFrame(app)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # تكوين الصفوف والأعمدة
    main_frame.grid_columnconfigure(0, weight=1)
    for i in range(4):
        main_frame.grid_rowconfigure(i, weight=1)
    
    # إضافة بعض العناصر للاختبار
    CTkLabel(main_frame, text="عنوان كبير", font=("Arial", 24)).grid(row=0, column=0, sticky="ew", pady=10)
    
    content_frame = CTkFrame(main_frame)
    content_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)
    
    CTkLabel(content_frame, text="محتوى متجاوب", font=("Arial", 16)).grid(row=0, column=0, sticky="nsew")
    
    input_frame = CTkFrame(main_frame)
    input_frame.grid(row=2, column=0, sticky="ew", pady=10)
    input_frame.grid_columnconfigure(0, weight=1)
    
    CTkButton(main_frame, text="زر متجاوب").grid(row=3, column=0, sticky="ew", pady=10)
    
    # تغيير حجم النافذة تلقائياً لاختبار الاستجابة
    app.geometry("800x600")
    
    def resize_test():
        """تغيير حجم النافذة تلقائياً لاختبار الاستجابة"""
        sizes = [
            "800x600", "1024x768", "1280x720", "1366x768", "1600x900", "1000x700"
        ]
        
        for size in sizes:
            app.geometry(size)
            app.update()
            # عرض الحجم الحالي
            current_size_label.configure(text=f"الحجم الحالي: {size}")
            time.sleep(2)  # انتظار ثانيتين بين كل تغيير
    
    # إضافة ملصق لعرض الحجم الحالي
    current_size_label = CTkLabel(app, text="الحجم الحالي: 800x600")
    current_size_label.pack(side="bottom", pady=10)
    
    # زر لبدء اختبار تغيير الحجم
    test_button = CTkButton(app, text="بدء اختبار تغيير الحجم", command=resize_test)
    test_button.pack(side="bottom", pady=10)
    
    app.mainloop()

if __name__ == "__main__":
    test_responsive_behavior()