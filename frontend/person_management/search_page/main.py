"""
Main search page implementation.
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Dict, Any, Optional, List
import tkinter as tk
from ..constants import SEARCH_MODES, ACADEMIC_LEVELS, GENDER_OPTIONS, BACK_BUTTON_STYLE, SEARCH_BUTTON_STYLE, ACTION_BUTTON_STYLE, SALARY_BUTTON_STYLE, TABLE_HEADER_STYLE, TABLE_ROW_STYLE
from ..student_details_popup import StudentDetailsPopup
from ..teacher_details_popup import TeacherDetailsPopup
from ..edit_pages.student_edit import EditStudentPage
from ..edit_pages.teacher_edit import EditTeacherPage
from backend.database import get_all_students, get_all_teachers, delete_student_by_name, delete_teacher_by_id
from ..teacher_salary_popup import TeacherSalaryPopup

class SearchPage(ctk.CTkFrame):
    """Main search interface for finding and managing students and teachers."""

    def __init__(self, master, on_back: Callable = None):
        """
        Initialize the search page.

        Args:
            master: The parent widget.
            on_back: Callback function to return to the previous page.
        """
        super().__init__(master)
        self.master = master
        self.on_back = on_back
        self.setup_ui()
        # Trigger initial search after a short delay to ensure UI is ready
        self.after(100, self.search)

    def arabic(self, text: str) -> str:
        # Assuming Arabic reshaping/bidi handling is done elsewhere or not needed here
        return text

    def setup_ui(self):
        """Set up the UI components for the search page."""
        # The frame is now 'self' because the class inherits from CTkFrame
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        # Configure rows for top bar, filters, fixed header, and scrollable results
        self.grid_rowconfigure(0, weight=0) # Top bar
        self.grid_rowconfigure(1, weight=0) # Filters
        self.grid_rowconfigure(2, weight=1) # Scrollable results (expandable)
        self.grid_columnconfigure(0, weight=1) # Make the main column expandable

        # Top bar with back button and search mode
        top_bar = ctk.CTkFrame(self)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top_bar.grid_columnconfigure(0, weight=0) # Back button column
        top_bar.grid_columnconfigure(1, weight=1) # Title column (if any), allow it to expand
        top_bar.grid_columnconfigure(2, weight=0) # Mode selector column (fixed size)

        # Back button
        if self.on_back:
            back_icon = ctk.CTkButton(
                top_bar,
                text="←",
                font=("Arial", 18, "bold"),
                width=40,
                height=40,
                fg_color="#ff3333",
                text_color="#000000",
                hover_color="#b71c1c",
                corner_radius=20,
                command=self.go_back
            )
            back_icon.grid(row=0, column=0, sticky="w", padx=(0, 10))

        # Search mode selector (placed on the right)
        self.mode_var = tk.StringVar(value=SEARCH_MODES[0])
        self.mode_menu = ctk.CTkOptionMenu(
            top_bar,
            values=[self.arabic(mode) for mode in SEARCH_MODES],
            variable=self.mode_var,
            command=self.on_mode_change
        )
        self.mode_menu.grid(row=0, column=2, sticky="e") # Placed on the rightmost column

        # Search filters
        filters_frame = ctk.CTkFrame(self)
        filters_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        # Configure columns for RTL (Academic Level Label | Academic Level Menu | Name Entry | Search Button)
        filters_frame.grid_columnconfigure(0, weight=0) # Academic Level Label (fixed size)
        filters_frame.grid_columnconfigure(1, weight=1) # Academic Level Menu (expands)
        filters_frame.grid_columnconfigure(2, weight=1) # Name Entry (expands more)
        filters_frame.grid_columnconfigure(3, weight=0) # Search Button (fixed size)

        # Search Button (RTL: Placed on the far right)
        self.search_button = ctk.CTkButton(
            filters_frame,
            text=self.arabic("بحث"),
            command=self.search,
            **SEARCH_BUTTON_STYLE
        )
        self.search_button.grid(row=0, column=3, padx=5, sticky="e") # Placed on the right

        # Name filter (RTL: Entry to the left of Search Button)
        self.name_entry = ctk.CTkEntry(filters_frame, width=300, justify="right", font=("Arial", 14), placeholder_text=self.arabic("اسم الطالب أو المعلمة")) # Updated placeholder
        self.name_entry.grid(row=0, column=2, padx=5, sticky="ew") # Placed to the left of Search Button

        # Academic level filter (RTL: Label to the left of Name Entry, Menu to the left of Label)
        ctk.CTkLabel(filters_frame, text=self.arabic(":المستوى الدراسي"), font=("Arial", 14)).grid(row=0, column=1, padx=5, sticky="e") # Label to the right of menu
        self.level_var = tk.StringVar(value=ACADEMIC_LEVELS[0])
        self.level_menu = ctk.CTkOptionMenu(
            filters_frame,
            values=[self.arabic(level) for level in ACADEMIC_LEVELS],
            variable=self.level_var
        )
        self.level_menu.grid(row=0, column=0, padx=5, sticky="ew") # Menu on the far left

        # Scrollable results frame
        self.results_scroll_frame = ctk.CTkScrollableFrame(self, height=385) # Set height to show approx 11 rows (11 * 35)
        self.results_scroll_frame.grid(row=2, column=0, sticky="nsew") # Placed in row 2 now
        # Ensure the inner frame within the scrollable frame expands
        self.results_scroll_frame.grid_columnconfigure(0, weight=1)

    def setup_results_table(self):
        """Set up the results table headers."""
        # Headers will now be added directly in the display methods (display_student_results, display_teacher_results)
        pass # This method is no longer needed for fixed headers

    def on_mode_change(self, _=None):
        """Handle search mode change."""
        # No need to call setup_results_table() here anymore
        self.search()

    def search(self):
        """Perform search based on current filters."""
        name = self.name_entry.get().strip()
        level = self.level_var.get()
        mode = self.mode_var.get()

        # Clear previous results from the scrollable frame
        for widget in self.results_scroll_frame.winfo_children():
            widget.destroy()

        # Perform search and filter results
        if mode == self.arabic(SEARCH_MODES[0]):  # Students
            all_students = get_all_students()
            results = [s for s in all_students if
                       (not name or name.lower() in s.get("name", "").lower()) and # Search only by name
                       (level == self.arabic(ACADEMIC_LEVELS[0]) or self.arabic(s.get("term", "")) == level)]
            self.display_student_results(results)
        else:  # Teachers
            all_teachers = get_all_teachers()
            results = [t for t in all_teachers if
                       (not name or name.lower() in t.get("name", "").lower()) and # Search only by name
                       (level == self.arabic(ACADEMIC_LEVELS[0]) or self.arabic(t.get("term", "")) == level)]
            self.display_teacher_results(results)

    def display_student_results(self, students: List[Dict[str, Any]]):
        """Display student search results with headers inside the scrollable frame."""
        # Define headers for student results (order changed)
        headers = ["الإجراءات", "الاسـم", "الفصل", "الرقم التسلسلي"]
        # Map header index to RTL grid column index (adjusted indices)
        header_column_map_rtl = {0: 0, 1: 2, 2: 1, 3: 3}

        # Create header row frame inside the scrollable frame
        header_frame = ctk.CTkFrame(self.results_scroll_frame, fg_color="gray50") # Add a background color for header
        # Place the header frame within the scrollable frame
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Configure columns for RTL (Action | Name | Term | Serial)
        # Weights adjusted to distribute space more evenly among data columns
        # These weights must match the weights in the row frames below
        header_frame.grid_columnconfigure(0, weight=0) # Action buttons column (fixed width/minimal weight)
        header_frame.grid_columnconfigure(1, weight=1) # Term
        header_frame.grid_columnconfigure(2, weight=2) # Name (Name usually takes more space)
        header_frame.grid_columnconfigure(3, weight=0) # Serial Number (fixed width/minimal weight)

        # Place headers from right to left using the map
        for i, header in enumerate(headers):
            col_index = header_column_map_rtl[i]
            ctk.CTkLabel(
                header_frame,
                text=self.arabic(header),
                **TABLE_HEADER_STYLE
            ).grid(row=0, column=col_index, padx=5, sticky="nsew") # Use nsew sticky for better alignment

        # Start row index for data from 1 (after header row)
        for i, student in enumerate(students, start=1):
            row_frame = ctk.CTkFrame(self.results_scroll_frame)
            # Place the row frame within the scrollable frame, spanning the full width
            # Ensure row in scrollable frame expands vertically
            self.results_scroll_frame.grid_rowconfigure(i, weight=1)
            row_frame.grid(row=i, column=0, sticky="ew", pady=2)

            # Configure columns for RTL (Action | Name | Term | Serial)
            # These weights must match the weights in the header frame
            row_frame.grid_columnconfigure(0, weight=0) # Action buttons column (fixed width/minimal weight)
            row_frame.grid_columnconfigure(1, weight=1) # Term
            row_frame.grid_columnconfigure(2, weight=2) # Name (Name usually takes more space)
            row_frame.grid_columnconfigure(3, weight=0) # Serial Number (fixed width/minimal weight)

            # Student data (Place from right to left - Name, Term) + Serial (far right) + Actions (far left)
            data_order = ["name", "term"]
            # The order to display data fields corresponding to columns from left to right (Serial, Name, Term)
            display_order = [3, 2, 1] # Adjusted column indices for Serial, Name, Term

            # Display Serial Number
            ctk.CTkLabel(row_frame, text=str(i), **TABLE_ROW_STYLE).grid(row=0, column=3, padx=5, sticky="nsew")

            # Display data fields (Name, Term)
            # Adjusted placement for Name and Term based on new display_order
            ctk.CTkLabel(row_frame, text=self.arabic(student.get("name", "")), **TABLE_ROW_STYLE).grid(row=0, column=2, padx=5, sticky="nsew")
            ctk.CTkLabel(row_frame, text=self.arabic(student.get("term", "")), **TABLE_ROW_STYLE).grid(row=0, column=1, padx=5, sticky="nsew")

            # Action buttons (Place on the left)
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=0, padx=5, sticky="w") # Action buttons on the left, aligned west

            # View details button
            details_button = ctk.CTkButton(
                actions_frame,
                text=self.arabic("عرض"), # View
                command=lambda s=student: self.show_student_details(s),
                **ACTION_BUTTON_STYLE
            )
            details_button.pack(side="left", padx=2) # Pack to the left within actions_frame

            # Edit button
            edit_button = ctk.CTkButton(
                actions_frame,
                text=self.arabic("تعديل"), # Edit
                command=lambda s=student: self.edit_student(s),
                **ACTION_BUTTON_STYLE
            )
            edit_button.pack(side="left", padx=2) # Pack to the left within actions_frame

            # Delete button
            delete_button = ctk.CTkButton(
                actions_frame,
                text=self.arabic("حذف"), # Delete
                command=lambda s=student: self.delete_student(s),
                fg_color="red",
                hover_color="darkred",
                **ACTION_BUTTON_STYLE
            )
            delete_button.pack(side="left", padx=2) # Pack to the left within actions_frame

    def display_teacher_results(self, teachers: List[Dict[str, Any]]):
        """Display teacher search results with headers inside the scrollable frame."""
        # Define headers for teacher results (order changed)
        headers = ["الإجراءات", "الاسـم", "الفصل", "الرقم التسلسلي"]
        # Map header index to RTL grid column index (adjusted indices)
        header_column_map_rtl = {0: 0, 1: 2, 2: 1, 3: 3}

        # Create header row frame inside the scrollable frame
        header_frame = ctk.CTkFrame(self.results_scroll_frame, fg_color="gray50") # Add a background color for header
        # Place the header frame within the scrollable frame
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Configure columns for RTL (Action | Name | Term | Serial)
        # Weights adjusted to distribute space more evenly among data columns
        # These weights must match the weights in the row frames below
        header_frame.grid_columnconfigure(0, weight=0) # Action buttons column (fixed width/minimal weight)
        header_frame.grid_columnconfigure(1, weight=1) # Term
        header_frame.grid_columnconfigure(2, weight=2) # Name (Name usually takes more space)
        header_frame.grid_columnconfigure(3, weight=0) # Serial Number (fixed width/minimal weight)

        # Place headers from right to left using the map
        for i, header in enumerate(headers):
            col_index = header_column_map_rtl[i]
            ctk.CTkLabel(
                header_frame,
                text=self.arabic(header),
                **TABLE_HEADER_STYLE
            ).grid(row=0, column=col_index, padx=5, sticky="nsew") # Use nsew sticky for better alignment

        # Start row index for data from 1 (after header row)
        for i, teacher in enumerate(teachers, start=1):
            row_frame = ctk.CTkFrame(self.results_scroll_frame)
            # Place the row frame within the scrollable frame, spanning the full width
            # Ensure row in scrollable frame expands vertically
            self.results_scroll_frame.grid_rowconfigure(i, weight=1)
            row_frame.grid(row=i, column=0, sticky="ew", pady=2)

            # Configure columns for RTL (Action | Name | Term | Serial)
            # These weights must match the weights in the header frame
            row_frame.grid_columnconfigure(0, weight=0) # Action buttons column (fixed width/minimal weight)
            row_frame.grid_columnconfigure(1, weight=1) # Term
            row_frame.grid_columnconfigure(2, weight=2) # Name (Name usually takes more space)
            row_frame.grid_columnconfigure(3, weight=0) # Serial Number (fixed width/minimal weight)

            # Teacher data (Place from right to left - Name, Term) + Serial (far right) + Actions (far left)
            data_order = ["name", "term"]
            # The order to display data fields corresponding to columns from left to right (Serial, Name, Term)
            display_order = [3, 2, 1] # Adjusted column indices for Serial, Name, Term

            # Display Serial Number
            ctk.CTkLabel(row_frame, text=str(i), **TABLE_ROW_STYLE).grid(row=0, column=3, padx=5, sticky="nsew")

            # Display data fields (Name, Term)
            # Adjusted placement for Name and Term based on new display_order
            ctk.CTkLabel(row_frame, text=self.arabic(teacher.get("name", "")), **TABLE_ROW_STYLE).grid(row=0, column=2, padx=5, sticky="nsew")
            ctk.CTkLabel(row_frame, text=self.arabic(teacher.get("term", "")), **TABLE_ROW_STYLE).grid(row=0, column=1, padx=5, sticky="nsew")

            # Action buttons (Place on the left)
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=0, padx=5, sticky="w") # Action buttons on the left, aligned west

            # View details button
            details_button = ctk.CTkButton(
                actions_frame,
                text=self.arabic("عرض"), # View
                command=lambda t=teacher: self.show_teacher_details(t),
                **ACTION_BUTTON_STYLE
            )
            details_button.pack(side="left", padx=2) # Pack to the left within actions_frame

            # Edit button
            edit_button = ctk.CTkButton(
                actions_frame,
                text=self.arabic("تعديل"), # Edit
                command=lambda t=teacher: self.edit_teacher(t),
                **ACTION_BUTTON_STYLE
            )
            edit_button.pack(side="left", padx=2) # Pack to the left within actions_frame

            # Delete button
            delete_button = ctk.CTkButton(
                actions_frame,
                text=self.arabic("حذف"), # Delete
                command=lambda t=teacher: self.delete_teacher(t),
                fg_color="red",
                hover_color="darkred",
                **ACTION_BUTTON_STYLE
            )
            delete_button.pack(side="left", padx=2) # Pack to the left within actions_frame

            # Show Salary button (only for teachers)
            salary_button = ctk.CTkButton(
                actions_frame,
                text=self.arabic("الرواتب"), # Salaries
                command=lambda t=teacher: self.show_teacher_salary(t),
                **SALARY_BUTTON_STYLE
            )
            salary_button.pack(side="left", padx=2) # Pack to the left within actions_frame

    def show_student_details(self, student: Dict[str, Any]):
        """Show student details popup."""
        StudentDetailsPopup(self.master, student, on_close=self.search) # Pass self.search as on_close callback

    def show_teacher_details(self, teacher: Dict[str, Any]):
        """Show teacher details popup."""
        TeacherDetailsPopup(self.master, teacher, arabic_handler=self.arabic, on_close=self.search)

    def edit_student(self, student: Dict[str, Any]):
        """Navigate to the student edit page."""
        if self.master and hasattr(self.master, 'show_edit_student_page'):
            self.master.show_edit_student_page(student, on_save=self.search, on_cancel=self.search)

    def edit_teacher(self, teacher: Dict[str, Any]):
        """Navigate to the teacher edit page."""
        if self.master and hasattr(self.master, 'show_edit_teacher_page'):
            self.master.show_edit_teacher_page(teacher, on_save=self.search, on_cancel=self.search)

    def delete_student(self, student: Dict[str, Any]):
        """Delete a student after confirmation."""
        if messagebox.askyesno(self.arabic("تأكيد الحذف"), self.arabic(f"هل أنت متأكد من حذف الطالب {student.get('name', '')}؟")):
            delete_student_by_name(student.get('name', ''))
            self.search() # Refresh results after deletion

    def delete_teacher(self, teacher: Dict[str, Any]):
        """Delete a teacher after confirmation."""
        if messagebox.askyesno(self.arabic("تأكيد الحذف"), self.arabic(f"هل أنت متأكد من حذف المعلمة {teacher.get('name', '')}؟")):
            # Assuming teacher has an 'id' field for deletion
            teacher_id = teacher.get('id') # Replace 'id' with the actual field name if different
            if teacher_id:
                delete_teacher_by_id(teacher_id)
                self.search() # Refresh results after deletion
            else:
                messagebox.showerror(self.arabic("خطأ"), self.arabic("لا يمكن حذف المعلمة: معرف المعلمة غير موجود."))

    def show_teacher_salary(self, teacher: Dict[str, Any]):
        """Show teacher salary details popup."""
        TeacherSalaryPopup(self.master, teacher, arabic_handler=self.arabic) # Pass self.arabic for Arabic handling

    def go_back(self):
        """Navigate back to the previous page."""
        if self.on_back:
            self.on_back()