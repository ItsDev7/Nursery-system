"""Search page implementation.

This module provides the user interface for searching, viewing, editing, and deleting
student and teacher records.
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Dict, Any, List
import tkinter as tk
from ..constants import SEARCH_MODES, ACADEMIC_LEVELS, SEARCH_BUTTON_STYLE, ACTION_BUTTON_STYLE, SALARY_BUTTON_STYLE, TABLE_HEADER_STYLE, TABLE_ROW_STYLE
from ..student_details_popup import StudentDetailsPopup
from ..teacher_details_popup import TeacherDetailsPopup
from ..edit_pages.student_edit import EditStudentPage
from ..edit_pages.teacher_edit import EditTeacherPage
from backend.database import get_all_students, get_all_teachers, delete_student_by_name, delete_teacher_by_id
from ..teacher_salary_popup import TeacherSalaryPopup

class SearchPage(ctk.CTkFrame):
    """Main search interface for finding and managing students and teachers.
    
    Allows switching between student and teacher search modes, applying filters
    by name and academic level, and performing actions like viewing details,
    editing, and deleting records.
    """

    def __init__(self, master, on_back: Callable = None):
        """Initialize the search page.

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
        """Handles potential Arabic text display issues.
        
        Args:
            text: The input string which may contain Arabic characters.
            
        Returns:
            The processed string for display (identity function if no processing needed).
        """
        # Assuming Arabic reshaping/bidi handling is done elsewhere or not needed here
        return text

    def setup_ui(self):
        """Sets up the main UI components for the search page.
        
        Includes the top bar, search filters, and the scrollable results frame.
        """
        # The frame is now 'self' because the class inherits from CTkFrame
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        # Configure grid for layout: top bar, filters, and expandable results area
        self.grid_rowconfigure(0, weight=0) # Top bar (fixed height)
        self.grid_rowconfigure(1, weight=0) # Filters (fixed height)
        self.grid_rowconfigure(2, weight=1) # Scrollable results (expands vertically)
        self.grid_columnconfigure(0, weight=1) # Allow the main column to expand horizontally

        # Set up individual UI sections
        self._setup_top_bar()
        self._setup_filters()
        self._setup_results_frame()

    def _setup_top_bar(self):
        """Sets up the top bar with back button and search mode selector."""
        top_bar = ctk.CTkFrame(self)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        # Configure grid within top_bar for RTL layout: [Back Button] [Title (if any)] [Mode Selector]
        top_bar.grid_columnconfigure(0, weight=0) # Back button column (fixed size)
        top_bar.grid_columnconfigure(1, weight=1) # Title column (expands)
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
            back_icon.grid(row=0, column=0, sticky="w", padx=(0, 10)) # Place on the left

        # Search mode selector (placed on the right for RTL)
        self.mode_var = tk.StringVar(value=SEARCH_MODES[0])
        self.mode_menu = ctk.CTkOptionMenu(
            top_bar,
            values=[self.arabic(mode) for mode in SEARCH_MODES],
            variable=self.mode_var,
            command=self.on_mode_change
        )
        self.mode_menu.grid(row=0, column=2, sticky="e") # Place on the rightmost column

    def _setup_filters(self):
        """Sets up the search filter components."""
        filters_frame = ctk.CTkFrame(self)
        filters_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        # Configure grid within filters_frame for RTL layout: [Academic Level Menu] [Academic Level Label] [Name Entry] [Search Button]
        filters_frame.grid_columnconfigure(0, weight=1) # Academic Level Menu (expands)
        filters_frame.grid_columnconfigure(1, weight=0) # Academic Level Label (fixed size)
        filters_frame.grid_columnconfigure(2, weight=1) # Name Entry (expands more than level menu)
        filters_frame.grid_columnconfigure(3, weight=0) # Search Button (fixed size)

        # Search Button (RTL: Placed on the far right)
        self.search_button = ctk.CTkButton(
            filters_frame,
            text=self.arabic("بحث"), # "Search"
            command=self.search,
            **SEARCH_BUTTON_STYLE
        )
        self.search_button.grid(row=0, column=3, padx=5, sticky="e") # Placed on the right

        # Name filter (RTL: Entry to the left of Search Button)
        self.name_entry = ctk.CTkEntry(filters_frame, width=300, justify="right", 
                                        font=("Arial", 14), placeholder_text=self.arabic("اسم الطالب أو المعلمة")) # "Student or Teacher Name"
        self.name_entry.grid(row=0, column=2, padx=5, sticky="ew") # Placed to the left of Search Button

        # Academic level filter (RTL: Label to the left of Name Entry, Menu to the left of Label)
        ctk.CTkLabel(filters_frame, text=self.arabic(":المستوى الدراسي"), font=("Arial", 14)).grid(row=0, column=1, padx=5, sticky="e") # Label to the right of menu
        # Levels from constants, excluding the "All" option for display in dropdown
        levels = [self.arabic(level) for level in ACADEMIC_LEVELS if level != "الجميع"] # Filter out "All"
        # Reverse levels for RTL display in dropdown if needed (depends on CTkOptionMenu behavior)
        # levels.reverse() # Consider reversing if dropdown order is incorrect
        self.level_var = tk.StringVar(value=self.arabic(ACADEMIC_LEVELS[0])) # Default to "All"
        self.level_menu = ctk.CTkOptionMenu(
            filters_frame,
            values=levels, # Use filtered levels
            variable=self.level_var
        )
        self.level_menu.grid(row=0, column=0, padx=5, sticky="ew") # Menu on the far left

    def _setup_results_frame(self):
        """Sets up the scrollable frame to display search results."""
        # Scrollable frame for results. Height adjusted to fit approx 11 rows.
        self.results_scroll_frame = ctk.CTkScrollableFrame(self, height=385)
        self.results_scroll_frame.grid(row=2, column=0, sticky="nsew") # Place in row 2, expanding to fill space
        # Ensure the inner frame within the scrollable frame expands
        self.results_scroll_frame.grid_columnconfigure(0, weight=1)

    def setup_results_table(self):
        """This method is no longer used for setting up table headers."
        
        Headers are now handled directly within display_student_results and display_teacher_results.
        """
        pass

    def on_mode_change(self, _=None):
        """Handles the event when the search mode (Student/Teacher) is changed.
        
        Triggers a new search based on the selected mode.
        
        Args:
            _: Event data (ignored).
        """
        # No need to call setup_results_table() here anymore
        self.search()

    def search(self):
        """Performs the search operation based on current filters and mode.
        
        Retrieves data from the database and displays the results in the scrollable frame.
        """
        name_filter = self.name_entry.get().strip()
        level_filter = self.level_var.get()
        mode = self.mode_var.get()

        # Clear previous results from the scrollable frame
        for widget in self.results_scroll_frame.winfo_children():
            widget.destroy()

        # Perform search and filter results based on mode
        if mode == self.arabic(SEARCH_MODES[0]):  # Students mode
            all_students = get_all_students()
            # Filter students by name (case-insensitive) and academic level
            results = [s for s in all_students if
                       (not name_filter or name_filter.lower() in s.get("name", "").lower()) and # Search only by name
                       (level_filter == self.arabic(ACADEMIC_LEVELS[0]) or self.arabic(s.get("term", "")) == level_filter)]
            self.display_student_results(results)
        else:  # Teachers mode
            all_teachers = get_all_teachers()
            # Filter teachers by name (case-insensitive) and academic level
            results = [t for t in all_teachers if
                       (not name_filter or name_filter.lower() in t.get("name", "").lower()) and # Search only by name
                       (level_filter == self.arabic(ACADEMIC_LEVELS[0]) or self.arabic(t.get("term", "")) == level_filter)]
            self.display_teacher_results(results)

    def display_student_results(self, students: List[Dict[str, Any]]):
        """Displays the student search results in a table format.
        
        Args:
            students: A list of dictionaries, each representing a student record.
        """
        # Define headers for student results (order adjusted for RTL display)
        headers = ["الإجراءات", "الاسـم", "الفصل", "الرقم التسلسلي"] # Actions | Name | Term | Serial Number
        # Map logical header order to RTL grid column index (0 is leftmost, increases to the right)
        # The physical column index will be from right to left for display
        header_column_map_rtl = {0: 0, 1: 2, 2: 1, 3: 3} # Actions -> Col 0, Name -> Col 2, Term -> Col 1, Serial -> Col 3

        # Create header row frame inside the scrollable frame
        header_frame = ctk.CTkFrame(self.results_scroll_frame, fg_color="gray50") # Add a background color for header
        # Place the header frame within the scrollable frame, spanning the full width
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Configure columns for RTL table layout within the header frame (Action | Term | Name | Serial)
        # Weights adjusted to distribute space more evenly among data columns
        # These weights must match the weights in the data row frames below
        header_frame.grid_columnconfigure(0, weight=0) # Action buttons column (fixed width/minimal weight)
        header_frame.grid_columnconfigure(1, weight=1) # Term column (expands)
        header_frame.grid_columnconfigure(2, weight=2) # Name column (expands more)
        header_frame.grid_columnconfigure(3, weight=0) # Serial Number column (fixed width/minimal weight)

        # Place headers from right to left using the map
        # We iterate through the desired display order of headers and place them in the corresponding RTL grid column
        display_headers_rtl_order = [headers[3], headers[2], headers[1], headers[0]] # Serial, Term, Name, Actions
        display_columns_rtl_order = [3, 2, 1, 0] # Corresponding grid columns from right to left

        for i, header_text in enumerate(display_headers_rtl_order):
             ctk.CTkLabel(
                header_frame,
                text=self.arabic(header_text),
                **TABLE_HEADER_STYLE
            ).grid(row=0, column=display_columns_rtl_order[i], padx=5, sticky="nsew") # Use nsew sticky for better alignment

        # Display student data rows starting from row 1 (after header)
        for i, student in enumerate(students, start=1):
            row_frame = ctk.CTkFrame(self.results_scroll_frame)
            # Place the row frame within the scrollable frame, spanning the full width
            # Ensure row in scrollable frame expands vertically
            self.results_scroll_frame.grid_rowconfigure(i, weight=1)
            row_frame.grid(row=i, column=0, sticky="ew", pady=2)

            # Configure columns for RTL table layout within the row frame (Action | Term | Name | Serial)
            # These weights must match the weights in the header frame
            row_frame.grid_columnconfigure(0, weight=0) # Action buttons column
            row_frame.grid_columnconfigure(1, weight=1) # Term column
            row_frame.grid_columnconfigure(2, weight=2) # Name column
            row_frame.grid_columnconfigure(3, weight=0) # Serial Number column

            # Display Serial Number (far right column in RTL grid)
            ctk.CTkLabel(row_frame, text=str(i), **TABLE_ROW_STYLE).grid(row=0, column=3, padx=5, sticky="nsew")

            # Display Name (reversed for RTL display, placed in the middle-right column)
            original_name = student.get("name", "")
            name_parts = original_name.split()
            reversed_name_parts = name_parts[::-1] # Reverse the list of parts
            reversed_name = " ".join(reversed_name_parts) # Join parts with space
            ctk.CTkLabel(row_frame, text=self.arabic(reversed_name), **TABLE_ROW_STYLE).grid(row=0, column=2, padx=5, sticky="nsew")

            # Display Academic Level (Term) (middle-left column)
            ctk.CTkLabel(row_frame, text=self.arabic(student.get("term", "")),
                         **TABLE_ROW_STYLE).grid(row=0, column=1, padx=5, sticky="nsew")

            # Action buttons (Place on the far left column in RTL grid)
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
        """Displays the teacher search results in a table format.
        
        Args:
            teachers: A list of dictionaries, each representing a teacher record.
        """
        # Define headers for teacher results (order adjusted for RTL display)
        headers = ["الإجراءات", "الاسـم", "الفصل", "الرقم التسلسلي"] # Actions | Name | Term | Serial Number
        # Map logical header order to RTL grid column index (0 is leftmost, increases to the right)
        header_column_map_rtl = {0: 0, 1: 2, 2: 1, 3: 3} # Actions -> Col 0, Name -> Col 2, Term -> Col 1, Serial -> Col 3

        # Create header row frame inside the scrollable frame
        header_frame = ctk.CTkFrame(self.results_scroll_frame, fg_color="gray50") # Add a background color for header
        # Place the header frame within the scrollable frame, spanning the full width
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Configure columns for RTL table layout within the header frame (Action | Term | Name | Serial)
        # Weights adjusted to distribute space more evenly among data columns
        # These weights must match the weights in the data row frames below
        header_frame.grid_columnconfigure(0, weight=0) # Action buttons column (fixed width/minimal weight)
        header_frame.grid_columnconfigure(1, weight=1) # Term column (expands)
        header_frame.grid_columnconfigure(2, weight=2) # Name column (expands more)
        header_frame.grid_columnconfigure(3, weight=0) # Serial Number column (fixed width/minimal weight)

        # Place headers from right to left using the map
        display_headers_rtl_order = [headers[3], headers[2], headers[1], headers[0]] # Serial, Term, Name, Actions
        display_columns_rtl_order = [3, 2, 1, 0] # Corresponding grid columns from right to left

        for i, header_text in enumerate(display_headers_rtl_order):
             ctk.CTkLabel(
                header_frame,
                text=self.arabic(header_text),
                **TABLE_HEADER_STYLE
            ).grid(row=0, column=display_columns_rtl_order[i], padx=5, sticky="nsew") # Use nsew sticky for better alignment

        # Display teacher data rows starting from row 1 (after header)
        for i, teacher in enumerate(teachers, start=1):
            row_frame = ctk.CTkFrame(self.results_scroll_frame)
            # Place the row frame within the scrollable frame, spanning the full width
            # Ensure row in scrollable frame expands vertically
            self.results_scroll_frame.grid_rowconfigure(i, weight=1)
            row_frame.grid(row=i, column=0, sticky="ew", pady=2)

            # Configure columns for RTL table layout within the row frame (Action | Term | Name | Serial)
            # These weights must match the weights in the header frame
            row_frame.grid_columnconfigure(0, weight=0) # Action buttons column
            row_frame.grid_columnconfigure(1, weight=1) # Term column
            row_frame.grid_columnconfigure(2, weight=2) # Name column
            row_frame.grid_columnconfigure(3, weight=0) # Serial Number column

            # Display Serial Number (far right column in RTL grid)
            ctk.CTkLabel(row_frame, text=str(i), **TABLE_ROW_STYLE).grid(row=0, column=3, padx=5, sticky="nsew")

            # Display Name (reversed for RTL display, placed in the middle-right column)
            original_name = teacher.get("name", "")
            name_parts = original_name.split()
            reversed_name_parts = name_parts[::-1] # Reverse the list of parts
            reversed_name = " ".join(reversed_name_parts) # Join parts with space
            ctk.CTkLabel(row_frame, text=self.arabic(reversed_name), **TABLE_ROW_STYLE).grid(row=0, column=2, padx=5, sticky="nsew")

            # Display Academic Level (Term) (middle-left column)
            ctk.CTkLabel(row_frame, text=self.arabic(teacher.get("term", "")),
                         **TABLE_ROW_STYLE).grid(row=0, column=1, padx=5, sticky="nsew")

            # Action buttons (Place on the far left column in RTL grid)
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
        """Shows a popup window with detailed information for a student.
        
        Args:
            student: A dictionary containing the student's data.
        """
        # Pass self.search as on_close callback to refresh results after closing popup
        StudentDetailsPopup(self.master, student, on_close=self.search)

    def show_teacher_details(self, teacher: Dict[str, Any]):
        """Shows a popup window with detailed information for a teacher.
        
        Args:
            teacher: A dictionary containing the teacher's data.
        """
        TeacherDetailsPopup(self.master, teacher, arabic_handler=self.arabic, on_close=self.search)

    def edit_student(self, student: Dict[str, Any]):
        """Navigates to the student edit page.
        
        Args:
            student: A dictionary containing the student's data to be edited.
        """
        # Hide the current search page
        self.grid_forget()
        # Create and show the edit page, passing a callback to return here and refresh
        edit_page = EditStudentPage(self.master, student, on_back=lambda: self._show_search_page_after_edit(edit_page))
        edit_page.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        # Ensure the master grid is configured to allow the new page to expand
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def edit_teacher(self, teacher: Dict[str, Any]):
        """Navigates to the teacher edit page.
        
        Args:
            teacher: A dictionary containing the teacher's data to be edited.
        """
        # Hide the current search page
        self.grid_forget()
        # Create and show the edit page, passing a callback to return here and refresh
        edit_page = EditTeacherPage(self.master, teacher, on_back=lambda: self._show_search_page_after_edit(edit_page))
        edit_page.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        # Ensure the master grid is configured to allow the new page to expand
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def _show_search_page_after_edit(self, edit_page_instance):
        """Destroys the edit page instance and returns to the search page.
        
        Refreshes the search results upon returning.
        
        Args:
            edit_page_instance: The instance of the edit page to destroy.
        """
        if edit_page_instance:
            edit_page_instance.destroy()
        # Show the search page again by re-gridding it
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=20) # Re-grid to its original position
        # Refresh the search results to reflect any changes made in the edit page
        self.search()

    def delete_student(self, student: Dict[str, Any]):
        """Deletes a student record after user confirmation.
        
        Args:
            student: A dictionary containing the student's data to be deleted.
        """
        # Show confirmation dialog in Arabic
        if messagebox.askyesno(self.arabic("تأكيد الحذف"), self.arabic(f"هل أنت متأكد من حذف الطالب {student.get('name', '')}؟")):
            # Call backend function to delete student by name
            delete_student_by_name(student.get('name', ''))
            # Refresh search results after deletion
            self.search()

    def delete_teacher(self, teacher: Dict[str, Any]):
        """Deletes a teacher record after user confirmation.
        
        Args:
            teacher: A dictionary containing the teacher's data to be deleted.
        """
        # Show confirmation dialog in Arabic
        if messagebox.askyesno(self.arabic("تأكيد الحذف"), self.arabic(f"هل أنت متأكد من حذف المعلمة {teacher.get('name', '')}؟")):
            # Assuming teacher has an 'id' field for deletion
            teacher_id = teacher.get('id') # Replace 'id' with the actual field name if different
            if teacher_id:
                # Call backend function to delete teacher by ID
                delete_teacher_by_id(teacher_id)
                # Refresh search results after deletion
                self.search()
            else:
                # Show error message if teacher ID is missing
                messagebox.showerror(self.arabic("خطأ"), self.arabic("لا يمكن حذف المعلمة: معرف المعلمة غير موجود.")) # "Error", "Cannot delete teacher: Teacher ID not found."

    def show_teacher_salary(self, teacher: Dict[str, Any]):
        """Shows a popup window with salary details for a teacher.
        
        Args:
            teacher: A dictionary containing the teacher's data.
        """
        # Pass self.arabic for Arabic handling in the popup and the teacher data
        TeacherSalaryPopup(self.master, teacher, arabic_handler=self.arabic)

    def go_back(self):
        """Navigates back to the previous page using the provided callback."""
        if self.on_back:
            self.on_back()