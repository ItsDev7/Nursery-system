"""Utility functions and custom widgets for person management.

This module contains helper functions for tasks like Arabic text normalization
and date handling, as well as custom Tkinter widgets like a DateEntry with
a calendar popup.
"""
import unicodedata
from typing import List, Tuple, Callable, Optional
import customtkinter as ctk
import tkinter as tk
from datetime import datetime, date
import calendar
import re

def normalize_arabic(text: str) -> str:
    """Normalize Arabic text for consistent searching.
    
    Removes diacritics and other presentation forms to simplify comparison.
    
    Args:
        text: The input Arabic string.
        
    Returns:
        The normalized string.
    """
    # Convert the text to a normalized form (NFKD) and encode/decode to remove diacritics.
    # This helps in searching for Arabic names regardless of diacritics.
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

def get_fee_dates(fee_date_widgets: List[Tuple]) -> List[str]:
    """Format fee dates from the date entry widgets.
    
    Takes a list of widget tuples (day, month, year) and returns a list of formatted
    date strings (DD/MM/YYYY). Returns an empty string for incomplete dates.
    
    Args:
        fee_date_widgets: List of tuples containing (day_entry, month_entry, year_entry) for each fee.
        
    Returns:
        List of formatted date strings in DD/MM/YYYY format.
    """
    dates = []
    # Iterate through each set of day, month, year entry widgets
    for day_entry, month_entry, year_entry in fee_date_widgets:
        day = day_entry.get().strip()
        month = month_entry.get().strip()
        year = year_entry.get().strip()
        
        # If any part of the date is missing, add an empty string to the list
        if not all([day, month, year]):
            dates.append("")
            continue
            
        # Otherwise, format the date as DD/MM/YYYY and add it to the list
        dates.append(f"{day}/{month}/{year}")
    
    return dates 

class DateEntry(ctk.CTkFrame):
    """A custom date entry widget with calendar popup and smart formatting.
    
    Provides an entry field for date input, a button to open a calendar popup
    for selection, and includes basic formatting and validation.
    """
    
    def __init__(self, master, arabic_handler: Callable, **kwargs):
        """Initialize the DateEntry widget.
        
        Args:
            master: The parent widget.
            arabic_handler: Function to handle Arabic text display.
            **kwargs: Arbitrary keyword arguments for CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.arabic_handler = arabic_handler
        
        # Configure grid layout for the frame (1 row, 2 columns)
        self.grid_columnconfigure(0, weight=1) # Entry field column (expands)
        self.grid_columnconfigure(1, weight=0) # Button column (fixed size)
        
        # --- Create Entry Field ---
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=self.arabic_handler("التاريخ (يوم-شهر-سنة)"), # "Date (day-month-year)"
            justify="right" # Right-align text for RTL input
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # --- Create Calendar Button ---
        self.cal_button = ctk.CTkButton(
            self,
            text="📅", # Calendar icon character
            width=30,
            command=self.show_calendar # Bind button click to show_calendar method
        )
        self.cal_button.grid(row=0, column=1, sticky="e")
        
        # --- Bind Events ---
        # Bind key release event for real-time formatting as user types
        self.entry.bind('<KeyRelease>', self._on_key_release)
        # Bind focus out event for final validation and formatting
        self.entry.bind('<FocusOut>', self._on_focus_out)
        
        # Initialize calendar popup attribute
        self.cal_popup = None
        
    def _on_key_release(self, event):
        """Handles key release events in the entry field for smart formatting.
        
        Args:
            event: The Tkinter event object.
        """
        text = self.entry.get()
        
        # Remove any non-digit characters from the input text
        digits = re.sub(r'\D', '', text)
        
        # Apply formatting based on the number of digits entered (up to 8 for DDMMYYYY)
        if len(digits) <= 8:
            formatted = self._format_date(digits)
            # If the formatted text is different, update the entry
            if formatted != text:
                # Store the current cursor position before updating
                cursor_pos = self.entry.index(tk.INSERT)
                # Delete current text and insert the newly formatted text
                self.entry.delete(0, tk.END)
                self.entry.insert(0, formatted)
                # Restore the cursor position, adjusting for added hyphens
                # (Simple approach: just set to the original cursor pos) - More complex logic might be needed for perfect cursor placement
                self.entry.icursor(cursor_pos)
    
    def _format_date(self, digits: str) -> str:
        """Formats a string of digits into DD-MM-YYYY format.
        
        Args:
            digits: A string containing only digits.
            
        Returns:
            The formatted date string with hyphens.
        """
        if not digits:
            return "" # Return empty string if no digits
            
        # Format as DD-MM-YYYY if enough digits are available
        if len(digits) >= 8:
            return f"{digits[:2]}-{digits[2:4]}-{digits[4:8]}"
        # Format as DD-MM if enough digits are available
        elif len(digits) >= 4:
            return f"{digits[:2]}-{digits[2:4]}"
        # Format as DD if enough digits are available
        elif len(digits) >= 2:
            return f"{digits[:2]}"
        # Return digits as is if less than 2
        return digits
    
    def _on_focus_out(self, event):
        """Validates and formats the date when the entry loses focus.
        
        Tries to parse the date and formats it consistently or clears the entry if invalid.
        
        Args:
            event: The Tkinter event object.
        """
        text = self.entry.get()
        if text: # Only process if the entry is not empty
            try:
                # Attempt to parse the date string
                date = self._parse_date(text)
                if date: # If parsing is successful
                    # Format the date to a consistent DD-MM-YYYY string
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, date.strftime("%d-%m-%Y"))
                else: # If parsing failed but text was present
                     self.entry.delete(0, tk.END) # Clear the entry for invalid format
            except ValueError:
                # If a ValueError occurs during parsing (e.g., invalid date values)
                self.entry.delete(0, tk.END) # Clear the entry
    
    def _parse_date(self, text: str) -> Optional[datetime]:
        """Parses a date string from various possible formats.
        
        Currently supports DDMMYYYY (as digits) and DD-MM-YYYY formats.
        
        Args:
            text: The date string from the entry field.
            
        Returns:
            A datetime object if parsing is successful, otherwise None.
        """
        # Remove any non-digit characters for initial check
        digits = re.sub(r'\D', '', text)
        
        if len(digits) == 8:
            # Try parsing as DDMMYYYY
            try:
                return datetime.strptime(f"{digits[:2]}-{digits[2:4]}-{digits[4:8]}", "%d-%m-%Y")
            except ValueError:
                pass # Continue to next format if parsing fails
        
        # If text contains hyphens, try parsing as DD-MM-YYYY
        if '-' in text:
            try:
                return datetime.strptime(text, "%d-%m-%Y")
            except ValueError:
                pass # Continue if parsing fails
                
        return None # Return None if no valid format found
    
    def show_calendar(self):
        """Creates and displays the calendar popup window.
        
        Ensures only one calendar popup is open at a time.
        """
        # Check if a calendar popup already exists and is visible
        if self.cal_popup is None or not self.cal_popup.winfo_exists():
            # Create a new CalendarPopup instance, passing self as parent
            self.cal_popup = CalendarPopup(self, self.arabic_handler)
        else:
            # If popup exists, bring it to the front
            self.cal_popup.lift()
    
    def get_date(self) -> Optional[str]:
        """Gets the date from the entry field in DD-MM-YYYY format.
        
        Validates the date format before returning.
        
        Returns:
            The formatted date string (DD-MM-YYYY) or None if the date is invalid.
        """
        text = self.entry.get()
        try:
            # Parse the date using the internal parser
            date = self._parse_date(text)
            # Return formatted date if valid, otherwise None
            return date.strftime("%d-%m-%Y") if date else None
        except ValueError:
            return None # Return None if parsing fails (should be handled by _parse_date, but for safety)
    
    def set_date(self, date_str: str):
        """Sets the date in the entry field using DD-MM-YYYY format.
        
        Args:
            date_str: The date string to set (expected DD-MM-YYYY).
        """
        try:
            # Attempt to parse the input date string
            date = datetime.strptime(date_str, "%d-%m-%Y")
            # Clear the entry and insert the parsed and formatted date
            self.entry.delete(0, tk.END)
            self.entry.insert(0, date.strftime("%d-%m-%Y")) # Ensure consistent format
        except ValueError:
            # If the input string format is incorrect, do nothing or handle error
            pass # Silently fail if format is wrong, keeping existing text or clearing

class CalendarPopup(tk.Toplevel):
    """A custom calendar popup for date selection.
    
    Displays a month view and allows selecting a specific day.
    Updates the parent DateEntry widget with the selected date.
    """
    
    def __init__(self, parent: DateEntry, arabic_handler: Callable):
        """Initialize the CalendarPopup.
        
        Args:
            parent: The parent DateEntry widget instance.
            arabic_handler: Function to handle Arabic text display.
        """
        super().__init__(parent)
        self.parent = parent
        self.arabic_handler = arabic_handler
        
        # --- Configure Window ---
        self.title(("اختر التاريخ")) # "Select Date"
        self.geometry("300x350") # Set initial size
        self.transient(parent) # Make popup appear on top of parent
        self.grab_set() # Make popup modal
        
        # --- Position the Popup ---
        # Position below the parent DateEntry widget
        self.update_idletasks() # Update geometry to get accurate parent position
        x = parent.winfo_rootx() # Get parent's root x coordinate
        y = parent.winfo_rooty() + parent.winfo_height() # Position below parent
        self.geometry(f"+{x}+{y}") # Set window position using +x+y format
        
        # Get today's date to initialize the calendar view
        today = date.today()
        self.current_date = today
        
        # --- Create Main Frame ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Create Header with Month/Year and Navigation ---
        header_frame = ctk.CTkFrame(main_frame) # Frame for month/year and navigation buttons
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Previous month button
        prev_btn = ctk.CTkButton(
            header_frame,
            text="◀", # Left arrow character
            width=30,
            command=self._prev_month # Bind to previous month method
        )
        prev_btn.pack(side="left", padx=5)
        
        # Month/Year label (will be updated)
        self.header_label = ctk.CTkLabel(
            header_frame,
            text=self._get_month_year_text(), # Initial text (current month/year)
            font=("Arial", 14, "bold")
        )
        self.header_label.pack(side="left", expand=True) # Place in center and expand
        
        # Next month button
        next_btn = ctk.CTkButton(
            header_frame,
            text="▶", # Right arrow character
            width=30,
            command=self._next_month # Bind to next month method
        )
        next_btn.pack(side="right", padx=5) # Place on the right
        
        # --- Create Calendar Grid Frame ---
        self.cal_frame = ctk.CTkFrame(main_frame) # Frame to hold the calendar day buttons
        self.cal_frame.pack(fill="both", expand=True)
        
        # Configure grid for the calendar frame (7 columns for days, dynamic rows)
        for i in range(7):
            self.cal_frame.grid_columnconfigure(i, weight=1) # Equal weight for columns
        # Grid rows will be configured dynamically as buttons are created
        for i in range(7): # Configure up to 7 rows (for header + max 6 weeks)
            self.cal_frame.grid_rowconfigure(i, weight=1) # Equal weight for rows
        
        # --- Add Weekday Headers ---
        weekdays = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"] # Arabic weekday names
        # Place weekday labels in the first row of the calendar frame
        for i, day in enumerate(weekdays):
            label = ctk.CTkLabel(
                self.cal_frame,
                text=self.arabic_handler(day), # Display Arabic weekday name
                font=("Arial", 12, "bold")
            )
            label.grid(row=0, column=i, padx=2, pady=2) # Place in row 0, columns 0-6
        
        # --- Create Calendar Day Buttons ---
        self._create_calendar_buttons() # Generate and place day buttons for the current month
        
        # --- Handle Window Closing ---
        # Bind the window closing protocol (clicking the X button) to destroy the window
        self.protocol("WM_DELETE_WINDOW", self.destroy)
    
    def _get_month_year_text(self) -> str:
        """Gets the current month and year text in Arabic.
        
        Returns:
            A formatted string like "[Arabic Month Name] YYYY".
        """
        # List of Arabic month names
        month_names = [
            "يناير", # January
            "فبراير", # February
            "مارس", # March
            "إبريل", # April
            "مايو", # May
            "يونيو", # June
            "يوليو", # July
            "أغسطس", # August
            "سبتمبر", # September
            "أكتوبر", # October
            "نوفمبر", # November
            "ديسمبر" # December
        ]
        # Format and return the text using the arabic handler
        return f"{self.arabic_handler(month_names[self.current_date.month - 1])} {self.current_date.year}"
    
    def _create_calendar_buttons(self):
        """Generates and places the calendar day buttons for the current month view.
        
        Clears existing buttons and creates new ones based on the monthcalendar data.
        """
        # Clear all existing widgets in the calendar frame (except headers if any)
        for widget in self.cal_frame.winfo_children():
            # Ensure we don't accidentally delete the weekday labels in row 0
            if isinstance(widget, ctk.CTkButton): # Only destroy buttons
                widget.destroy()
        
        # Get the calendar data for the current month (list of weeks, each is a list of days)
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Create buttons for each day in the calendar view
        for week_num, week in enumerate(cal): # Iterate through weeks
            for day_num, day in enumerate(week): # Iterate through days in the week
                if day != 0: # Only create a button if the day is valid (not 0 for padding)
                    btn = ctk.CTkButton(
                        self.cal_frame,
                        text=str(day), # Display the day number
                        width=30,
                        height=30,
                        # Command to select the date when clicked
                        command=lambda d=day: self._select_date(d)
                    )
                    # Place the button in the grid (row + 1 to account for header row)
                    btn.grid(row=week_num + 1, column=day_num, padx=2, pady=2)
    
    def _prev_month(self):
        """Navigates the calendar view to the previous month.
        
        Updates the displayed month/year header and regenerates the day buttons.
        """
        # Calculate the previous month and year
        if self.current_date.month == 1: # If currently January
            # Go to December of the previous year
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            # Go to the previous month in the same year
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        
        # Update the header label and regenerate calendar buttons
        self.header_label.configure(text=self._get_month_year_text())
        self._create_calendar_buttons()
    
    def _next_month(self):
        """Navigates the calendar view to the next month.
        
        Updates the displayed month/year header and regenerates the day buttons.
        """
        # Calculate the next month and year
        if self.current_date.month == 12: # If currently December
            # Go to January of the next year
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            # Go to the next month in the same year
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        
        # Update the header label and regenerate calendar buttons
        self.header_label.configure(text=self._get_month_year_text())
        self._create_calendar_buttons()
    
    def _select_date(self, day: int):
        """Handles the selection of a day from the calendar.
        
        Formats the selected date and sets it in the parent DateEntry widget,
        then closes the calendar popup.
        
        Args:
            day: The day number selected (integer).
        """
        # Create a date object for the selected date
        selected_date = date(
            self.current_date.year,
            self.current_date.month,
            day
        )
        # Format the selected date as DD-MM-YYYY string
        formatted_date = selected_date.strftime("%d-%m-%Y")
        
        # Update the date in the parent DateEntry widget
        self.parent.set_date(formatted_date)
        
        # Close the calendar popup window
        self.destroy() 