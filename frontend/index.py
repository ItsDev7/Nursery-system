"""
Main application window and navigation forManagement System.
This module handles the main application window, navigation, and dashboard functionality.
"""

# Standard library imports
import sqlite3
from datetime import datetime
from tkinter import messagebox

# Third-party imports
from customtkinter import (
    CTkFrame, CTkLabel, CTkButton, CTkScrollableFrame,
    CTkProgressBar, CTkEntry
)
import arabic_reshaper
from bidi.algorithm import get_display

# Local application imports
from .register_student_page import RegisterStudentPage
from .fees.views import FeesPage
from .register_teacher_page import RegisterTeacherPage
from .statistics_page import StatisticsPage
from .person_management.search_page import SearchPage
from .person_management.utils import DateEntry
from backend.database import (
    get_all_activities, add_activity,
    update_activity, delete_activity, get_summary
)
from .settings import SettingsPage

class NextPage:
    """
    Main application window class that handles navigation and dashboard functionality.
    This class manages the main window layout, navigation sidebar, and different pages.
    """

    def __init__(self, main_window):
        """
        Initialize the main application window.
        
        Args:
            main_window: The root window of the application
        """
        self.main = main_window
        self.current_page = None
        self.setup_ui()

    def arabic(self, text: str) -> str:
        """
        Convert and display Arabic text properly.
        
        Args:
            text (str): The Arabic text to be displayed
            
        Returns:
            str: Properly formatted Arabic text
        """
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    # Navigation Methods
    def open_register_student_page(self):
        """Open the student registration page."""
        self.clear_content_frame()
        self.current_page = RegisterStudentPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("register_student")

    def open_search_student_page(self):
        """Open the student search page."""
        self.clear_content_frame()
        self.current_page = SearchPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("search")

    def open_fees_page(self):
        """Open the fees management page."""
        self.clear_content_frame()
        self.current_page = FeesPage(
            self.content_frame,
            on_back=self.show_dashboard,
            on_data_changed=self.show_dashboard,
            arabic_handler=self.arabic
        )
        self.highlight_active_nav_button("fees")

    def open_register_teacher_page(self):
        """Open the teacher registration page."""
        self.clear_content_frame()
        self.current_page = RegisterTeacherPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("register_teacher")
        
    def open_statistics_page(self):
        """Open the statistics and reports page."""
        self.clear_content_frame()
        self.current_page = StatisticsPage(self.content_frame, on_back=self.show_dashboard)
        self.highlight_active_nav_button("statistics")

    def open_settings_page(self):
        """Open the settings page."""
        self.clear_content_frame()
        self.current_page = SettingsPage(self.content_frame, self.main, on_back=self.show_dashboard)
        self.highlight_active_nav_button("settings")

    # UI Helper Methods
    def clear_content_frame(self):
        """Clear all widgets from the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def highlight_active_nav_button(self, active_button_id):
        """
        Highlight the active navigation button (frame).
        
        Args:
            active_button_id (str): ID of the active navigation button
        """
        # Reset all buttons to default color
        for button_id, button_frame in self.nav_buttons.items():
             # Re-apply default color to the frame
             button_frame.configure(fg_color="#4A90E2")

        # Highlight the active button
        if active_button_id in self.nav_buttons:
            active_frame = self.nav_buttons[active_button_id]
            # Apply active color to the frame
            active_frame.configure(fg_color="#3489f1") # Active color

    # Dashboard Methods
    def show_dashboard(self):
        """Display the main dashboard."""
        self.clear_content_frame()
        self.create_dashboard()
        self.highlight_active_nav_button("dashboard")

    def get_statistics(self):
        """
        Retrieve statistics from the database.
        
        Returns:
            dict: Dictionary containing various statistics
        """
        try:
            summary_data = get_summary()
            
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            
            # Get student count
            cursor.execute("SELECT COUNT(*) FROM students")
            students_count = cursor.fetchone()[0] or 0
            
            # Get teacher count
            cursor.execute("SELECT COUNT(*) FROM teachers")
            teachers_count = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                "students": students_count,
                "teachers": teachers_count,
                "income": summary_data.get('income', 0.0),
                "expenses": summary_data.get('expenses', 0.0)
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                "students": 0,
                "teachers": 0,
                "income": 0,
                "expenses": 0
            }

    def create_dashboard(self):
        """Create and display the main dashboard with statistics and activities."""
        # Create main dashboard frame
        dashboard_frame = CTkFrame(self.content_frame, fg_color="transparent")
        dashboard_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Configure grid layout
        for i in range(3):
            dashboard_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            dashboard_frame.grid_rowconfigure(i, weight=1)
        
        # Create header
        self._create_dashboard_header(dashboard_frame)
        
        # Get and display statistics
        stats = self.get_statistics()
        
        # Create statistics cards
        self._create_statistics_cards(dashboard_frame, stats)
        
        # Create financial chart
        self._create_financial_chart(dashboard_frame, stats)
        
        # Create info and activities section
        self._create_info_activities_section(dashboard_frame)

    def _create_dashboard_header(self, parent):
        """Create the dashboard header with title."""
        header_frame = CTkFrame(parent, fg_color="#1F6BB5", corner_radius=10)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=(5, 15))
        
        title = CTkLabel(
            header_frame,
            text=self.arabic("لوحة المعلومات عن الحضانة"),
            font=("Arial Black", 32),
            text_color="white"
        )
        title.pack(pady=20)

    def _create_statistics_cards(self, parent, stats):
        """Create statistics cards showing key metrics."""
        # Student and teacher cards
        self.create_stat_card(
            parent, 1, 0,
            self.arabic("عدد الطلاب"),
            str(stats["students"]),
            "#4CAF50",
            "👨‍🎓"
        )
        
        self.create_stat_card(
            parent, 1, 1,
            self.arabic("عدد المعلمات"),
            str(stats["teachers"]),
            "#E91E63",
            "👩‍🏫"
        )
        
        # Student-teacher ratio card
        ratio = stats["students"] / stats["teachers"] if stats["teachers"] > 0 else 0
        self.create_stat_card(
            parent, 1, 2,
            self.arabic("نسبة الطلاب/المعلمات"),
            f"{ratio:.1f}",
            "#3F51B5",
            "📊"
        )
        
        # Financial cards
        self.create_stat_card(
            parent, 2, 0,
            self.arabic("إجمالي الإيرادات"),
            f"{stats['income']} ج.م",
            "#FF9800",
            "💰"
        )
        
        self.create_stat_card(
            parent, 2, 1,
            self.arabic("إجمالي المصروفات"),
            f"{stats['expenses']} ج.م",
            "#9C27B0",
            "💸"
        )
        
        # Net profit card
        net_profit = stats["income"] - stats["expenses"]
        profit_color = "#4CAF50" if net_profit >= 0 else "#F44336"
        self.create_stat_card(
            parent, 2, 2,
            self.arabic("صافي الربح"),
            f"{net_profit} ج.م",
            profit_color,
            "📈"
        )

    def _create_financial_chart(self, parent, stats):
        """Create financial comparison chart."""
        chart_frame = CTkFrame(parent, fg_color="white", corner_radius=10)
        chart_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        
        # Chart title
        chart_title = CTkLabel(
            chart_frame,
            text=self.arabic("مقارنة الإيرادات والمصروفات"),
            font=("Arial", 20, "bold"),
            text_color="#333"
        )
        chart_title.pack(pady=(15, 10))
        
        # Create chart container
        chart_container = CTkFrame(chart_frame, fg_color="transparent")
        chart_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure chart columns
        chart_container.grid_columnconfigure(0, weight=1)
        chart_container.grid_columnconfigure(1, weight=4)
        chart_container.grid_columnconfigure(2, weight=1)
        
        # Create financial bars
        self._create_financial_bars(chart_container, stats)

    def _create_financial_bars(self, parent, stats):
        """Create financial comparison bars."""
        max_value = max(stats["income"], stats["expenses"]) if max(stats["income"], stats["expenses"]) > 0 else 1
        net_profit = stats["income"] - stats["expenses"]
        
        # Income bar
        self._create_financial_bar(
            parent, 0,
            self.arabic("الإيرادات:"),
            stats["income"],
            max_value,
            "#FF9800"
        )
        
        # Expenses bar
        self._create_financial_bar(
            parent, 1,
            self.arabic("المصروفات:"),
            stats["expenses"],
            max_value,
            "#9C27B0"
        )
        
        # Net profit bar
        profit_color = "#4CAF50" if net_profit >= 0 else "#F44336"
        self._create_financial_bar(
            parent, 2,
            self.arabic("صافي الربح:"),
            net_profit,
            max_value,
            profit_color
        )

    def _create_financial_bar(self, parent, row, label_text, value, max_value, color):
        """Create a single financial comparison bar."""
        # Label
        label = CTkLabel(parent, text=label_text, font=("Arial", 16, "bold"))
        label.grid(row=row, column=2, sticky="e", pady=8)
        
        # Progress bar
        progress = CTkProgressBar(parent, width=500, height=30, corner_radius=5)
        progress.grid(row=row, column=1, padx=10, pady=8)
        progress.set(abs(value) / max_value if max_value > 0 else 0)
        progress.configure(progress_color=color)
        
        # Value label
        value_label = CTkLabel(parent, text=f"{value} ج.م", font=("Arial", 16, "bold"))
        value_label.grid(row=row, column=0, sticky="w", pady=8)

    def _create_info_activities_section(self, parent):
        """Create information and activities section."""
        info_activities_frame = CTkFrame(parent, fg_color="transparent")
        info_activities_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        info_activities_frame.grid_columnconfigure(0, weight=1)
        info_activities_frame.grid_columnconfigure(1, weight=1)
        
        # Create information section
        self._create_info_section(info_activities_frame)
        
        # Create activities section
        self._create_activities_section(info_activities_frame)

    def _create_info_section(self, parent):
        """Create the kindergarten information section."""
        info_frame = CTkFrame(parent, fg_color="#f0f0f0", corner_radius=10)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        info_title = CTkLabel(
            info_frame,
            text=self.arabic("اهداف الحضانة"),
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

    def _create_activities_section(self, parent):
        """Create the activities management section."""
        activities_frame = CTkFrame(parent, fg_color="#E3F2FD", corner_radius=10)
        activities_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Activities title
        activities_title = CTkLabel(
            activities_frame,
            text=self.arabic("الأنشطة القادمة"),
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        )
        activities_title.pack(pady=(15, 10), anchor="n")
        
        # Create activity input form
        self._create_activity_input_form(activities_frame)
        
        # Create activities display
        self._create_activities_display(activities_frame)

    def _create_activity_input_form(self, parent):
        """Create the form for adding new activities."""
        input_frame = CTkFrame(parent, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        # Description input
        CTkLabel(input_frame, text=self.arabic("الوصف:"), font=("Arial", 14), anchor="e").grid(row=0, column=1, sticky="e", padx=5)
        self.activity_description_entry = CTkEntry(input_frame, font=("Arial", 14), justify="right")
        self.activity_description_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)

        # Date input
        CTkLabel(input_frame, text=self.arabic("التاريخ:"), font=("Arial", 14), anchor="e").grid(row=2, column=1, sticky="e", padx=5)
        self.activity_date_entry = DateEntry(input_frame, self.arabic)
        self.activity_date_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5)

        # Add activity button
        add_activity_button = CTkButton(
            parent,
            text=self.arabic("إضافة نشاط"),
            font=("Arial", 14, "bold"),
            command=self.add_new_activity
        )
        add_activity_button.pack(pady=(0, 10))

    def _create_activities_display(self, parent):
        """Create the scrollable frame for displaying activities."""
        self.activities_display_frame = CTkScrollableFrame(
            parent,
            fg_color="transparent",
            height=200
        )
        self.activities_display_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.activities_display_frame.grid_columnconfigure(0, weight=1)
        
        self.load_activities()

    def create_stat_card(self, parent, row, col, title, value, color, icon=None):
        """
        Create a statistics card with title, value, and optional icon.
        
        Args:
            parent: Parent widget
            row: Grid row position
            col: Grid column position
            title: Card title
            value: Card value
            color: Card color
            icon: Optional icon to display
        """
        card = CTkFrame(parent, fg_color="white", corner_radius=10)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Configure card grid
        card.grid_rowconfigure(0, weight=0)
        card.grid_rowconfigure(1, weight=0)
        card.grid_rowconfigure(2, weight=1)
        card.grid_columnconfigure(0, weight=1)
        
        # Color bar
        color_bar = CTkFrame(card, fg_color=color, height=8, corner_radius=5)
        color_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        
        # Title
        card_title = CTkLabel(
            card,
            text=title,
            font=("Arial", 18, "bold"),
            text_color="#333"
        )
        card_title.grid(row=0, column=0, pady=(15, 5), sticky="n")
        
        # Icon
        if icon:
            icon_label = CTkLabel(
                card,
                text=icon,
                font=("Arial", 42),
                text_color=color
            )
            icon_label.grid(row=1, column=0, pady=(5, 5), sticky="n")
        
        # Value
        card_value = CTkLabel(
            card,
            text=value,
            font=("Arial", 32, "bold"),
            text_color=color
        )
        card_value.grid(row=2, column=0, pady=(5, 15), sticky="n")

    def setup_ui(self):
        """Set up the main application UI with navigation and content area."""
        # Clear existing widgets
        for widget in self.main.winfo_children():
            widget.destroy()

        # Create main frame
        main_frame = CTkFrame(self.main, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        
        # Configure main frame grid
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0, minsize=150)
        
        # Create sidebar
        self._create_sidebar(main_frame)
        
        # Create content area
        self._create_content_area(main_frame)
        
        # Show dashboard
        self.show_dashboard()

    def _create_sidebar(self, parent):
        """Create the navigation sidebar."""
        sidebar = CTkFrame(parent, fg_color="#4A90E2", corner_radius=0, width=180)
        sidebar.grid(row=0, column=1, sticky="nsew")
        sidebar.grid_propagate(False)
        
        # Configure sidebar grid
        for i in range(7):
            sidebar.grid_rowconfigure(i, weight=0)
        # Configure row 7 to take up available space, pushing subsequent rows down
        sidebar.grid_rowconfigure(7, weight=1)
        # Configure row 8 for the settings button, give it weight 0 so it stays at the bottom
        sidebar.grid_rowconfigure(8, weight=0)
        sidebar.grid_columnconfigure(0, weight=1)
        
        # Logo
        logo_label = CTkLabel(
            sidebar,
            text=self.arabic("      حضانة القدس"),
            font=("Arial Black", 20),
            text_color="white"
        )
        logo_label.grid(row=0, column=0, pady=(20, 30), padx=10, sticky="ne")
        
        # Navigation buttons
        self._create_nav_buttons(sidebar)

    def _create_nav_buttons(self, parent):
        """Create navigation buttons in the sidebar."""
        self.nav_buttons = {}
        
        # Dashboard button
        self.nav_buttons["dashboard"] = self._create_nav_button(
            parent, 1,
            self.arabic("الصفحة الرئيسية"),
            self.show_dashboard,
            icon="🏠", # Home icon
            active_color="#3489f1"
        )
        
        # Register student button
        self.nav_buttons["register_student"] = self._create_nav_button(
            parent, 2,
            self.arabic("تسجيل طالب جديد"),
            self.open_register_student_page,
            icon="➕👨‍🎓" # Add student icon
        )
        
        # Register teacher button
        self.nav_buttons["register_teacher"] = self._create_nav_button(
            parent, 3,
            self.arabic("تسجيل معلمة جديدة"),
            self.open_register_teacher_page,
            icon="➕👩‍🏫" # Add teacher icon
        )
        
        # Search button
        self.nav_buttons["search"] = self._create_nav_button(
            parent, 4,
            self.arabic("البحث عن طالب / معلمة"),
            self.open_search_student_page,
            icon="🔍" # Search icon
        )
        
        # Fees button
        self.nav_buttons["fees"] = self._create_nav_button(
            parent, 5,
            self.arabic("المصروفات والإيرادات"),
            self.open_fees_page,
            icon="💸" # Money icon
        )
        
        # Statistics button
        self.nav_buttons["statistics"] = self._create_nav_button(
            parent, 6,
            self.arabic("الإحصائيات والتقارير"),
            self.open_statistics_page,
            icon="📈" # Chart icon
        )
        
        # Settings button
        self.nav_buttons["settings"] = self._create_nav_button(
            parent, 8, # Changed row to 8
            self.arabic("الإعدادات"),
            self.open_settings_page,
            icon="⚙️" # Settings icon
        )

    def _create_nav_button(self, parent, row, text, command, icon=None, active_color="#3489f1"):
        """Create a navigation button with specified properties, optional icon, and separate text/icon colors."""

        # Simulate hover effect - Define functions first
        def on_enter(event):
            button_frame.configure(fg_color=active_color)

        def on_leave(event):
            # This function is simplified. The active state highlighting is handled
            # by the highlight_active_nav_button method.
            # For simplicity, we reset to default color unless the button is the currently active one.
            # A more robust check for active state here would require passing the active_button_id
            # or storing the button's ID/state in the frame itself.
            # For now, rely on highlight_active_nav_button to set the correct color.
            button_frame.configure(fg_color="#4A90E2")

        # Create a frame to hold the icon and text labels
        button_frame = CTkFrame(
            parent,
            fg_color="#4A90E2", # Default background color
            height=40,
            corner_radius=0
        )
        button_frame.grid(row=row, column=0, padx=10, pady=5, sticky="ew") # Add vertical padding
        button_frame.grid_columnconfigure(0, weight=1) # Allow content to expand

        # Bind click events to the frame and its children to trigger the command
        def on_click(event=None):
            command()

        button_frame.bind("<Button-1>", on_click)

        # Create a frame inside for the icon and text to handle RTL layout
        content_frame = CTkFrame(button_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10)
        content_frame.grid_columnconfigure(0, weight=1) # Text column
        content_frame.grid_columnconfigure(1, weight=0) # Icon column (fixed size)


        # Icon Label (placed on the right in the content_frame grid for RTL)
        if icon:
            icon_label = CTkLabel(
                content_frame,
                text=icon,
                font=("Arial", 16), # Slightly larger font for icon
                text_color="black", # Gray color for the icon
                fg_color="transparent"
            )
            icon_label.grid(row=0, column=1, sticky="e", padx=(0, 5)) # Place icon on the right, add left padding
            icon_label.bind("<Button-1>", on_click) # Bind click event
            icon_label.bind("<Enter>", on_enter) # Bind hover enter event
            icon_label.bind("<Leave>", on_leave) # Bind hover leave event

        # Text Label (placed on the left in the content_frame grid for RTL)
        text_label = CTkLabel(
            content_frame,
            text=(text+" "), # Use the original text
            font=("Arial", 14, "bold"),
            text_color="white", # White color for the text
            fg_color="transparent",
            anchor="e" # Align text to the right
        )
        text_label.grid(row=0, column=0, sticky="ew") # Place text on the left, allow it to expand
        text_label.bind("<Button-1>", on_click) # Bind click event
        text_label.bind("<Enter>", on_enter) # Bind hover enter event
        text_label.bind("<Leave>", on_leave) # Bind hover leave event


        # Bind hover events to the main button frame
        button_frame.bind("<Enter>", on_enter)
        button_frame.bind("<Leave>", on_leave)

        # Store the frame reference
        return button_frame

    def _create_content_area(self, parent):
        """Create the main content area."""
        content_container = CTkFrame(parent, fg_color="#f5f5f5", corner_radius=0)
        content_container.grid(row=0, column=0, sticky="nsew")
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_columnconfigure(0, weight=1)
        
        self.content_frame = CTkScrollableFrame(content_container, fg_color="#f5f5f5")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    # Activity Management Methods
    def load_activities(self):
        """Load and display all activities."""
        # Clear existing activities
        for widget in self.activities_display_frame.winfo_children():
            widget.destroy()

        activities = get_all_activities()

        if not activities:
            CTkLabel(
                self.activities_display_frame,
                text=self.arabic("لا يوجد أنشطة قادمة حاليًا."),
                font=("Arial", 14),
                text_color="#555"
            ).pack(pady=10)
            return

        for activity_id, description, date in activities:
            self._create_activity_display_item(activity_id, description, date)

    def _create_activity_display_item(self, activity_id, description, date):
        """Create a display item for a single activity."""
        activity_frame = CTkFrame(self.activities_display_frame, fg_color="#BBDEFB", corner_radius=8)
        activity_frame.pack(fill="x", pady=4)
        activity_frame.grid_columnconfigure(0, weight=1)
        activity_frame.grid_columnconfigure(1, weight=0)

        # Description and date
        desc_date_frame = CTkFrame(activity_frame, fg_color="transparent")
        desc_date_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        desc_date_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(
            desc_date_frame,
            text=self.arabic(f"الوصف: {description}"),
            font=("Arial", 14),
            anchor="e"
        ).pack(fill="x")
        
        CTkLabel(
            desc_date_frame,
            text=self.arabic(f"التاريخ: {date}"),
            font=("Arial", 12),
            anchor="e",
            text_color="#555"
        ).pack(fill="x")

        # Action buttons
        buttons_frame = CTkFrame(activity_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        # Delete button
        delete_button = CTkButton(
            buttons_frame,
            text="✖",
            width=30,
            height=30,
            fg_color="red",
            text_color="white",
            command=lambda: self.confirm_delete_activity(activity_id)
        )
        delete_button.pack(side="right", padx=5)

        # Edit button
        edit_button = CTkButton(
            buttons_frame,
            text="✎",
            width=30,
            height=30,
            fg_color="orange",
            text_color="white",
            command=lambda: self.open_edit_activity_window(activity_id, description, date)
        )
        edit_button.pack(side="right", padx=5)

    def add_new_activity(self):
        """Add a new activity to the database."""
        description = self.activity_description_entry.get().strip()
        date = self.activity_date_entry.get_date()

        if not description or not date:
            messagebox.showerror(
                ("خطأ"),
                ("يرجى إدخال الوصف والتاريخ للنشاط."),
                parent=self.main
            )
            return

        add_activity(description, date)
        self.activity_description_entry.delete(0, "end")
        self.activity_date_entry.set_date("")
        self.load_activities()

    def confirm_delete_activity(self, activity_id):
        """Confirm and delete an activity."""
        result = messagebox.askyesno(
            ("تأكيد الحذف"),
            ("هل أنت متأكد أنك تريد حذف هذا النشاط؟")
        )
        if result:
            delete_activity(activity_id)
            self.load_activities()

    def open_edit_activity_window(self, activity_id, description, date):
        """Open window for editing an activity."""
        import customtkinter as ctk
        edit_window = ctk.CTkToplevel(self.main)
        edit_window.title(("تعديل النشاط"))
        edit_window.geometry("400x250")
        edit_window.transient(self.main)
        edit_window.grab_set()

        frame = ctk.CTkFrame(edit_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Description input
        CTkLabel(
            frame,
            text=self.arabic("الوصف الجديد:"),
            font=("Arial", 14),
            anchor="e"
        ).grid(row=0, column=1, sticky="e", padx=5, pady=(0,2))
        
        desc_entry = ctk.CTkEntry(frame, font=("Arial", 14), justify="right")
        desc_entry.insert(0, description)
        desc_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0,10))

        # Date input
        CTkLabel(
            frame,
            text=self.arabic("التاريخ الجديد:"),
            font=("Arial", 14),
            anchor="e"
        ).grid(row=2, column=1, sticky="e", padx=5, pady=(0,2))
        
        date_entry_widget = DateEntry(frame, self.arabic)
        date_entry_widget.set_date(date)
        date_entry_widget.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=(0,10))

        def save_edit():
            """Save the edited activity."""
            new_desc = desc_entry.get().strip()
            new_date = date_entry_widget.get_date()

            if not new_desc or not new_date:
                messagebox.showerror(
                    "خطأ",
                    ("يرجى إدخال كل الحقول."),
                    parent=edit_window
                )
                return

            try:
                datetime.strptime(new_date, '%d-%m-%Y')
            except ValueError:
                messagebox.showerror(
                    "خطأ",
                    ("صيغة التاريخ غير صحيحة. يرجى استخدام DD-MM-YYYY."),
                    parent=edit_window
                )
                return

            update_activity(activity_id, new_desc, new_date)
            self.load_activities()
            edit_window.destroy()

        # Save button
        save_button = ctk.CTkButton(
            frame,
            text=self.arabic("حفظ"),
            font=("Arial", 14, "bold"),
            command=save_edit
        )
        save_button.grid(row=4, column=0, sticky="e", padx=5)

        # Cancel button
        cancel_button = ctk.CTkButton(
            frame,
            text=self.arabic("إلغاء"),
            font=("Arial", 14, "bold"),
            command=edit_window.destroy
        )
        cancel_button.grid(row=4, column=1, sticky="w", padx=5)