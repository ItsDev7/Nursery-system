# أداة اختبار الريزوليوشن للتطبيق
# هذا الملف يساعد على اختبار التطبيق بأحجام شاشة مختلفة

import sys
import os
import subprocess
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Frame

def run_app_with_resolution(resolution=None):
    """تشغيل التطبيق مع خيار اختبار الريزوليوشن"""
    cmd = [sys.executable, "main.py"]
    if resolution:
        cmd.append("--test-resolution")
    subprocess.Popen(cmd)

def main():
    """واجهة اختبار الريزوليوشن"""
    root = Tk()
    root.title("اختبار الريزوليوشن - EL-NADA")
    root.geometry("400x300")
    
    frame = Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill="both")
    
    Label(frame, text="أداة اختبار الريزوليوشن", font=("Arial", 16, "bold")).pack(pady=10)
    Label(frame, text="هذه الأداة تساعدك على اختبار التطبيق بأحجام مختلفة").pack(pady=5)
    
    # زر تشغيل التطبيق بالحجم العادي
    Button(
        frame, 
        text="تشغيل التطبيق بالحجم العادي", 
        command=lambda: run_app_with_resolution(),
        height=2,
        width=30
    ).pack(pady=10)
    
    # زر تشغيل التطبيق مع أداة اختبار الريزوليوشن
    Button(
        frame, 
        text="تشغيل مع أداة اختبار الريزوليوشن", 
        command=lambda: run_app_with_resolution(True),
        height=2,
        width=30
    ).pack(pady=10)
    
    # معلومات إضافية
    Label(frame, text="ملاحظة: يمكنك تشغيل التطبيق مباشرة من سطر الأوامر باستخدام:").pack(pady=(20, 5))
    Label(frame, text="python main.py --test-resolution", font=("Courier", 10)).pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()