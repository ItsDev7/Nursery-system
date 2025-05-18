from customtkinter import CTk, CTkScrollableFrame, CTkButton, CTkLabel, CTkEntry, CTkFrame, CTkOptionMenu
import os
import sys
from pathlib import Path
from frontend.login import Login
from backend.init_db import init_database

class Main:
    def __init__(self):
        self.main_window = CTk()
        
        # Configure main window for responsiveness
        # تكوين النافذة الرئيسية لتكون متجاوبة
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)
        
        # Adjust window size based on screen size
        # ضبط حجم النافذة بناءً على حجم الشاشة
        self.set_window_size()
        
        # Scale UI elements based on screen resolution
        # تعيين نسبة التكبير للعناصر حسب دقة الشاشة
        self.scale_ui_elements()
        
        self.setup_main_window()
        
    def set_window_size(self):
        """Adjust window size based on screen size, with a minimum size."""
        # Get screen dimensions
        # الحصول على دقة الشاشة
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        
        # Calculate initial window size as 50% of screen size
        # حساب نصف حجم الشاشة
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        
        # Define minimum window size
        # تحديد الحد الأدنى لحجم النافذة
        min_width = 800
        min_height = 540
        
        # Ensure window size is not less than the minimum
        # التأكد من أن حجم النافذة لا يقل عن الحد الأدنى المسموح به
        window_width = max(window_width, min_width)
        window_height = max(window_height, min_height)
        
        # Set minimum window size to prevent excessive shrinking
        # تعيين الحد الأدنى لحجم النافذة لضمان عدم تصغيرها أكثر من اللازم
        self.main_window.minsize(min_width, min_height)
        
        # Set maximum window size (can be maximized to full screen)
        # تعيين الحد الأقصى لحجم النافذة (يمكن تكبيرها حتى حجم الشاشة الكامل)
        self.main_window.maxsize(screen_width, screen_height)
        
        # Enable window resizing
        # تمكين خاصية تغيير الحجم
        self.main_window.resizable(True, True)
        
        # Calculate window position to center it on the screen
        # حساب موقع النافذة لتكون في وسط الشاشة
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)
        
        # Apply the calculated size and position
        # تطبيق الحجم والموقع
        self.main_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        
    def scale_ui_elements(self):
        """Adjust UI element scaling based on screen resolution for better user experience."""
        # Get screen dimensions
        # الحصول على دقة الشاشة
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        
        # Calculate aspect ratio
        # حساب نسبة العرض إلى الارتفاع
        aspect_ratio = screen_width / screen_height
        
        # Calculate scaling factor based on screen resolution and aspect ratio
        # حساب عامل التحجيم بناءً على دقة الشاشة ونسبة العرض إلى الارتفاع
        if screen_width >= 2560 and screen_height >= 1440:  # Ultra HD (2K and above)
            # شاشات فائقة الدقة (2K وأعلى)
            scaling_factor = 1.4
        elif screen_width >= 1920 and screen_height >= 1080:  # Full HD
            # شاشات عالية الدقة (Full HD)
            scaling_factor = 1.2
        elif screen_width >= 1366 and screen_height >= 768:  # Medium resolution screens
            # شاشات متوسطة الدقة
            scaling_factor = 1.0
        else:  # Low resolution screens
            # شاشات منخفضة الدقة
            scaling_factor = 0.8
        
        # Adjust scaling factor for very wide screens
        # تعديل عامل التحجيم بناءً على نسبة العرض إلى الارتفاع (للشاشات العريضة جدًا)
        if aspect_ratio > 2.0:  # Very wide screens
            # شاشات عريضة جدًا
            scaling_factor *= 0.9
        
        # Apply the scaling factor to the UI
        # تطبيق عامل التحجيم على واجهة المستخدم
        self.main_window.tk.call("tk", "scaling", scaling_factor)
        
        # Print scaling information for development (can be removed in final version)
        # طباعة معلومات التحجيم للتطوير (يمكن إزالتها في الإصدار النهائي)
        print(f"Screen resolution: {screen_width}x{screen_height}, Aspect ratio: {aspect_ratio:.2f}, Scaling factor: {scaling_factor}")
    
    def setup_main_window(self):
        """Configures the main application window."""
        # Set window title
        # تعيين عنوان النافذة
        self.main_window.title("EL-NADA")
        
        # Load application icon
        # تحميل أيقونة التطبيق
        icon_path = os.path.join(Path(__file__).resolve().parent, "images", "ELNADA-icon.ico")
        try:
            self.main_window.iconbitmap(icon_path)
        except:
            # Ignore error if icon file is not found
            # تجاهل الخطأ إذا لم يتم العثور على الأيقونة
            print("Warning: Icon file not found.") # Changed to English
            pass
        
        # Enable window resizing (re-confirming)
        # تمكين خاصية تغيير الحجم (للتأكيد)
        self.main_window.resizable(True, True)
        
        # Bind window resize event
        # تعيين سلوك النافذة عند تغيير الحجم
        self.main_window.bind("<Configure>", self.on_window_resize)
            
        # Add a menu for testing different resolutions if the --test-resolution argument is provided
        # إضافة قائمة لاختبار أحجام مختلفة من الشاشة
        if len(sys.argv) > 1 and sys.argv[1] == "--test-resolution":
            self.add_resolution_tester()
          
    def add_resolution_tester(self):
        """Adds resolution testing tools for development/debugging."""
        # إضافة أدوات اختبار الدقة للتطوير
        test_frame = CTkFrame(self.main_window)
        test_frame.grid(row=0, column=1, sticky="ne", padx=10, pady=10)
        
        resolutions = [
            "800x600", "1024x768", "1280x720", "1366x768", 
            "1600x900", "1920x1080", "2560x1440"
        ]
        
        CTkLabel(test_frame, text="Test Resolution:").grid(row=0, column=0, padx=5, pady=5) # Changed to English
        
        resolution_menu = CTkOptionMenu(
            test_frame, 
            values=resolutions,
            command=self.change_resolution
        )
        resolution_menu.grid(row=1, column=0, padx=5, pady=5)
        resolution_menu.set("1000x700")
    
    def change_resolution(self, resolution):
        """Changes the window size for testing purposes."""
        # تغيير حجم النافذة للاختبار
        self.main_window.geometry(resolution)
    
    def on_window_resize(self, event):
        """Handles window resize events, including logging with threshold and delay."""
        # This function is called when the window is resized
        # يمكن استخدامها لتحديث العناصر التي تعتمد على حجم النافذة
        
        # Get the new window dimensions
        # الحصول على الحجم الجديد للنافذة
        new_width = event.width
        new_height = event.height
        
        # Define the minimum window size to prevent excessive shrinking
        # تحديد الحد الأدنى للنافذة لمنع التصغير المفرط
        min_width = 800
        min_height = 540
        
        # Note: Code that reset window size has been removed to allow free resizing.
        # We only log the new window size for monitoring.
        # ملاحظة: تم إزالة الكود الذي يعيد ضبط حجم النافذة لتمكين تغيير الحجم بحرية
        # نكتفي بتسجيل الحجم الجديد للنافذة في سجل التطبيق للمتابعة
        
        # Update elements if necessary (e.g., update font size)
        # This is useful if you want to dynamically resize some elements based on window size.
        # تحديث العناصر إذا لزم الأمر (مثال: تحديث حجم الخط في العناصر)
        # هذا مفيد إذا كنت تريد تغيير حجم بعض العناصر بناءً على حجم النافذة
        
        # Avoid frequent printing for small, consecutive size changes
        # تجنب الطباعة المتكررة للأحجام المتقاربة جدًا
        if not hasattr(self, 'last_logged_size'):
            self.last_logged_size = (new_width, new_height)
            self.last_log_time = 0
            print(f"Window resized to: {new_width}x{new_height}") # Changed to English
            return
        
        # Calculate the difference from the last logged size
        # حساب الفرق بين الحجم الحالي والحجم السابق
        width_diff = abs(new_width - self.last_logged_size[0])
        height_diff = abs(new_height - self.last_logged_size[1])
        
        # Define the minimum change threshold before logging (in pixels)
        # تحديد الحد الأدنى للتغيير قبل الطباعة (بالبكسل)
        min_change_threshold = 20
        
        # Get current time to apply delay between logs
        # الحصول على الوقت الحالي لتطبيق التأخير بين الطباعات
        import time # This import is used here, should keep it
        current_time = time.time()
        
        # Define minimum time delay between logs (in seconds)
        # تحديد الحد الأدنى للوقت بين الطباعات (بالثواني)
        min_time_between_logs = 0.5
        
        # Log the new size only if the change is significant enough and sufficient time has passed since the last log
        # طباعة معلومات الحجم الجديد فقط إذا كان التغيير كبيرًا بما فيه الكفاية ومر وقت كافٍ منذ آخر طباعة
        if ((width_diff > min_change_threshold or height_diff > min_change_threshold) and 
                (current_time - getattr(self, 'last_log_time', 0) > min_time_between_logs)):
            self.last_logged_size = (new_width, new_height)
            self.last_log_time = current_time
            print(f"Window resized to: {new_width}x{new_height}") # Changed to English

    
    def run(self):
        """Starts the main application loop."""
        # Use the main window directly without an extra scrollable frame
        # This will make the interface use the full window space
        # استخدام النافذة الرئيسية مباشرة بدون إطار قابل للتمرير إضافي
        # هذا سيجعل الواجهة تستخدم كامل مساحة النافذة
        
        # Pass the main window directly to the pages
        # تمرير النافذة الرئيسية مباشرة للصفحات
        Login(self.main_window)
        
        # Start the main event loop
        # بدء الحلقة الرئيسية
        self.main_window.mainloop()

if __name__ == "__main__":
    # Initialize the database before starting the application
    # تهيئة قاعدة البيانات قبل بدء التطبيق
    init_database()
    
    app = Main()
    app.run()    
# To run the program in resolution testing mode, use:
# لتشغيل البرنامج في وضع اختبار الدقة، استخدم:
# python main.py --test-resolution