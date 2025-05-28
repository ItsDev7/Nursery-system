"""
Statistics and Reports module for Elnada Kindergarten Management System.
This module handles the display of various statistics and reports including:
- Financial summary
- Teacher statistics
- Student statistics by term
"""

# Standard library imports
from tkinter import messagebox

# Third-party imports
from customtkinter import CTkFrame, CTkLabel, CTkButton
# Local application imports
from backend.database import get_detailed_statistics

class StatisticsPage:
    """
    Handles the statistics and reports page of the application.
    
    This class manages the display of various statistics including:
    - Financial summary (income, expenses, remaining balance)
    - Teacher statistics (count, salaries)
    - Student statistics by term (count, fees)
    """

    def __init__(self, main_window, on_back=None):
        """
        Initialize the statistics page.

        Args:
            main_window: The main application window
            on_back: Callback function to handle back navigation
        """
        self.main = main_window
        self.on_back = on_back
        self.setup_ui()

    def arabic(self, text: str) -> str:
        """
        Format Arabic text for proper display.

        Args:
            text (str): The Arabic text to be displayed

        Returns:
            str: Properly formatted Arabic text
        """
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    def setup_ui(self):
        """Set up the statistics page user interface."""
        self._clear_main_window()
        self._create_main_frame()
        self._create_header()
        self._load_and_display_statistics()

    def _clear_main_window(self):
        """Clear all existing widgets from the main window."""
        for widget in self.main.winfo_children():
            widget.destroy()

    def _create_main_frame(self):
        """Create and configure the main frame with grid layout."""
        # Create main frame
        self.main_frame = CTkFrame(self.main, fg_color=self.main.cget('fg_color'))
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure main window grid
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        # Configure main frame grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)  # Header row
        self.main_frame.grid_rowconfigure(1, weight=0)  # Summary row
        self.main_frame.grid_rowconfigure(2, weight=0)  # Teachers stats row
        self.main_frame.grid_rowconfigure(3, weight=1)  # Students stats row

    def _create_header(self):
        """Create the page header with back button and title."""
        # Back button
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

        # Page title
        title = CTkLabel(
            self.main_frame,
            text=self.arabic("الإحصائيات والتقارير"),
            font=("Arial Black", 30),
            text_color="#2D8CFF"
        )
        title.grid(row=0, column=1, pady=(10, 20), sticky="n")

    def _load_and_display_statistics(self):
        """Load statistics data and display it in the UI."""
        try:
            self.stats = get_detailed_statistics()
            self.display_statistics()
        except Exception as e:
            messagebox.showerror(
                "خطأ",
                f"حدث خطأ أثناء جلب البيانات: {str(e)}"
            )

    def display_statistics(self):
        """Display all statistics sections."""
        self._create_summary_section()
        self._create_teachers_section()
        self._create_students_section()

    def _create_summary_section(self):
        """Create and display the financial summary section."""
        # Create summary frame
        summary_frame = CTkFrame(self.main_frame)
        summary_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        # Configure grid for RTL layout
        summary_frame.grid_columnconfigure(0, weight=1)  # Value column
        summary_frame.grid_columnconfigure(1, weight=1)  # Label column
        
        # Section title
        summary_title = CTkLabel(
            summary_frame,
            text=self.arabic("الملخص العام"),
            font=("Arial", 24, "bold"),
            text_color="#2D8CFF",
            justify="right"
        )
        summary_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="e")
        
        # Display summary data
        summary = self.stats["summary"]
        summary_data = [
            ("إجمالي الإيرادات", f"{summary['income']:.2f}"),
            ("إجمالي المصروفات", f"{summary['expenses']:.2f}"),
            ("الرصيد المتبقي", f"{summary['remaining']:.2f}"),
            ("إجمالي رواتب المعلمات", f"{summary['teacher_salaries']:.2f}")
        ]
        
        self._display_data_grid(summary_frame, summary_data, "#2D8CFF", 1)

    def _create_teachers_section(self):
        """Create and display the teachers statistics section."""
        # Create teachers frame
        teachers_frame = CTkFrame(self.main_frame)
        teachers_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        # Configure grid for RTL layout
        teachers_frame.grid_columnconfigure(0, weight=1)  # Value column
        teachers_frame.grid_columnconfigure(1, weight=1)  # Label column
        
        # Section title
        teachers_title = CTkLabel(
            teachers_frame,
            text=self.arabic("إحصائيات المعلمات"),
            font=("Arial", 24, "bold"),
            text_color="#E91E63",
            justify="right"
        )
        teachers_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="e")
        
        # Display teachers data
        teachers = self.stats["teachers"]
        teachers_data = [
            ("عدد المعلمات", f"{teachers['teacher_count']}"),
            ("إجمالي الرواتب", f"{teachers['total_salaries']:.2f}")
        ]
        
        self._display_data_grid(teachers_frame, teachers_data, "#E91E63", 1)

    def _create_students_section(self):
        """Create and display the students statistics section."""
        # Create students frame
        students_frame = CTkFrame(self.main_frame)
        students_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        # Configure grid for RTL layout
        students_frame.grid_columnconfigure(0, weight=1)  # Fees column
        students_frame.grid_columnconfigure(1, weight=1)  # Count column
        students_frame.grid_columnconfigure(2, weight=1)  # Term column
        
        # Section title
        students_title = CTkLabel(
            students_frame,
            text=self.arabic("إحصائيات الطلاب حسب الفصل"),
            font=("Arial", 24, "bold"),
            text_color="#4CAF50",
            justify="right"
        )
        students_title.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="e")
        
        # Column headers
        headers = ["إجمالي الرسوم:", "عدد الطلاب:", "الفصل:"]
        for col, header in enumerate(headers):
            CTkLabel(
                students_frame,
                text=self.arabic(header),
                font=("Arial", 18, "bold"),
                justify="right",
                text_color="#4CAF50"
            ).grid(row=1, column=col, padx=10, pady=8, sticky="e")
        
        # Display students data
        students_by_term = self.stats["students_by_term"]
        for row_idx, (term, data) in enumerate(students_by_term.items(), start=2):
            # Term name
            CTkLabel(
                students_frame,
                text=self.arabic(term),
                font=("Arial", 20),
                justify="right",
                text_color="#333333"
            ).grid(row=row_idx, column=2, padx=10, pady=8, sticky="e")
            
            # Student count
            CTkLabel(
                students_frame,
                text=str(data["student_count"]),
                font=("Arial", 20),
                justify="right",
                text_color="#333333"
            ).grid(row=row_idx, column=1, padx=10, pady=8, sticky="e")
            
            # Total fees
            CTkLabel(
                students_frame,
                text=f"{data['total_fees']:.2f}",
                font=("Arial", 20),
                justify="right",
                text_color="#333333"
            ).grid(row=row_idx, column=0, padx=10, pady=8, sticky="e")

    def _display_data_grid(self, parent, data, color, start_row):
        """
        Display a grid of data with labels and values.

        Args:
            parent: Parent widget
            data: List of (label, value) tuples
            color: Color for labels
            start_row: Starting row index
        """
        for i, (label, value) in enumerate(data):
            # Label
            CTkLabel(
                parent,
                text=self.arabic(f"{label}:"),
                font=("Arial", 18, "bold"),
                anchor="e",
                justify="right",
                text_color=color
            ).grid(row=i+start_row, column=1, padx=10, pady=8, sticky="e")
            
            # Value
            CTkLabel(
                parent,
                text=self.arabic(value),
                font=("Arial", 20),
                anchor="w",
                justify="left",
                text_color="#333333"
            ).grid(row=i+start_row, column=0, padx=10, pady=8, sticky="w")

    def go_back(self):
        """Handle navigation back to the previous page."""
        try:
            for widget in self.main.winfo_children():
                widget.destroy()

            if self.on_back:
                self.on_back()
        except Exception:
            # Ignore cleanup errors when closing the application
            pass