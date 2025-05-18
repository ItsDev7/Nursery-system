"""
Utility functions for the person management package.
"""
import unicodedata
from typing import List, Tuple, Callable, Optional
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
import calendar
import re

def normalize_arabic(text: str) -> str:
    """
    Normalize Arabic text for consistent searching.
    
    Args:
        text: The input Arabic string.
        
    Returns:
        The normalized string.
    """
    # Convert the text to a normalized form (NFKD) and encode/decode to remove diacritics
    # This helps in searching for Arabic names regardless of diacritics.
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

def get_fee_dates(fee_date_widgets: List[Tuple]) -> List[str]:
    """
    Format fee dates from the date entry widgets.
    
    Args:
        fee_date_widgets: List of tuples containing (day_entry, month_entry, year_entry) for each fee.
        
    Returns:
        List of formatted date strings in DD/MM/YYYY format.
    """
    dates = []
    for day_entry, month_entry, year_entry in fee_date_widgets:
        day = day_entry.get().strip()
        month = month_entry.get().strip()
        year = year_entry.get().strip()
        
        # If any part is empty, return empty string
        if not all([day, month, year]):
            dates.append("")
            continue
            
        # Format as DD/MM/YYYY
        dates.append(f"{day}/{month}/{year}")
    
    return dates 

class DateEntry(ctk.CTkFrame):
    """A custom date entry widget with calendar popup and smart formatting."""
    
    def __init__(self, master, arabic_handler: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.arabic_handler = arabic_handler
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        # Create entry field
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=self.arabic_handler("التاريخ (يوم-شهر-سنة)"),
            justify="right"
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Create calendar button
        self.cal_button = ctk.CTkButton(
            self,
            text="📅",
            width=30,
            command=self.show_calendar
        )
        self.cal_button.grid(row=0, column=1, sticky="e")
        
        # Bind events
        self.entry.bind('<KeyRelease>', self._on_key_release)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        
        # Calendar popup
        self.cal_popup = None
        
    def _on_key_release(self, event):
        """Handle key release events for smart formatting."""
        text = self.entry.get()
        
        # Remove any non-digit characters
        digits = re.sub(r'\D', '', text)
        
        # Format as user types
        if len(digits) <= 8:
            formatted = self._format_date(digits)
            if formatted != text:
                # Store cursor position
                cursor_pos = self.entry.index(tk.INSERT)
                # Update text
                self.entry.delete(0, tk.END)
                self.entry.insert(0, formatted)
                # Restore cursor position
                self.entry.icursor(cursor_pos)
    
    def _format_date(self, digits: str) -> str:
        """Format date digits into DD-MM-YYYY format."""
        if not digits:
            return ""
            
        # Handle DDMMYYYY format
        if len(digits) >= 8:
            return f"{digits[:2]}-{digits[2:4]}-{digits[4:8]}"
        # Handle DDMM format
        elif len(digits) >= 4:
            return f"{digits[:2]}-{digits[2:4]}"
        # Handle DD format
        elif len(digits) >= 2:
            return f"{digits[:2]}"
        return digits
    
    def _on_focus_out(self, event):
        """Validate and format date when focus leaves the entry."""
        text = self.entry.get()
        if text:
            try:
                # Try to parse the date
                date = self._parse_date(text)
                if date:
                    # Format it properly
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, date.strftime("%d-%m-%Y"))
            except ValueError:
                # If invalid, clear the entry
                self.entry.delete(0, tk.END)
    
    def _parse_date(self, text: str) -> Optional[datetime]:
        """Parse date from various formats."""
        # Remove any non-digit characters
        digits = re.sub(r'\D', '', text)
        
        if len(digits) == 8:
            # Try DDMMYYYY format
            try:
                return datetime.strptime(f"{digits[:2]}-{digits[2:4]}-{digits[4:8]}", "%d-%m-%Y")
            except ValueError:
                pass
        elif '-' in text:
            # Try DD-MM-YYYY format
            try:
                return datetime.strptime(text, "%d-%m-%Y")
            except ValueError:
                pass
        return None
    
    def show_calendar(self):
        """Show the calendar popup."""
        if self.cal_popup is None or not self.cal_popup.winfo_exists():
            self.cal_popup = CalendarPopup(self, self.arabic_handler)
        else:
            self.cal_popup.lift()
    
    def get_date(self) -> Optional[str]:
        """Get the current date in DD-MM-YYYY format."""
        text = self.entry.get()
        try:
            date = self._parse_date(text)
            return date.strftime("%d-%m-%Y") if date else None
        except ValueError:
            return None
    
    def set_date(self, date_str: str):
        """Set the date in DD-MM-YYYY format."""
        try:
            date = datetime.strptime(date_str, "%d-%m-%Y")
            self.entry.delete(0, tk.END)
            self.entry.insert(0, date.strftime("%d-%m-%Y"))
        except ValueError:
            pass

class CalendarPopup(tk.Toplevel):
    """A custom calendar popup for date selection."""
    
    def __init__(self, parent: DateEntry, arabic_handler: Callable):
        super().__init__(parent)
        self.parent = parent
        self.arabic_handler = arabic_handler
        
        # Configure window
        self.title(self.arabic_handler("اختر التاريخ"))
        self.geometry("300x350")
        self.transient(parent)
        self.grab_set()
        
        # Position the popup
        x = parent.winfo_rootx()
        y = parent.winfo_rooty() + parent.winfo_height()
        self.geometry(f"+{x}+{y}")
        
        # Get current date
        today = date.today()
        self.current_date = today
        
        # Create main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create header with month/year and navigation
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Previous month button
        prev_btn = ctk.CTkButton(
            header_frame,
            text="◀",
            width=30,
            command=self._prev_month
        )
        prev_btn.pack(side="left", padx=5)
        
        # Month/Year label
        self.header_label = ctk.CTkLabel(
            header_frame,
            text=self._get_month_year_text(),
            font=("Arial", 14, "bold")
        )
        self.header_label.pack(side="left", expand=True)
        
        # Next month button
        next_btn = ctk.CTkButton(
            header_frame,
            text="▶",
            width=30,
            command=self._next_month
        )
        next_btn.pack(side="right", padx=5)
        
        # Create calendar grid
        self.cal_frame = ctk.CTkFrame(main_frame)
        self.cal_frame.pack(fill="both", expand=True)
        
        # Configure grid
        for i in range(7):
            self.cal_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.cal_frame.grid_rowconfigure(i, weight=1)
        
        # Add weekday headers
        weekdays = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
        for i, day in enumerate(weekdays):
            label = ctk.CTkLabel(
                self.cal_frame,
                text=self.arabic_handler(day),
                font=("Arial", 12, "bold")
            )
            label.grid(row=0, column=i, padx=2, pady=2)
        
        # Create calendar buttons
        self._create_calendar_buttons()
        
        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.destroy)
    
    def _get_month_year_text(self) -> str:
        """Get the current month and year in Arabic."""
        month_names = [
            "يناير", "فبراير", "مارس", "إبريل", "مايو", "يونيو",
            "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
        ]
        return f"{self.arabic_handler(month_names[self.current_date.month - 1])} {self.current_date.year}"
    
    def _create_calendar_buttons(self):
        """Create the calendar day buttons."""
        # Clear existing buttons
        for widget in self.cal_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        
        # Get the calendar for the current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Create buttons for each day
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    btn = ctk.CTkButton(
                        self.cal_frame,
                        text=str(day),
                        width=30,
                        height=30,
                        command=lambda d=day: self._select_date(d)
                    )
                    btn.grid(row=week_num + 1, column=day_num, padx=2, pady=2)
    
    def _prev_month(self):
        """Go to the previous month."""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.header_label.configure(text=self._get_month_year_text())
        self._create_calendar_buttons()
    
    def _next_month(self):
        """Go to the next month."""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.header_label.configure(text=self._get_month_year_text())
        self._create_calendar_buttons()
    
    def _select_date(self, day: int):
        """Handle date selection."""
        selected_date = date(
            self.current_date.year,
            self.current_date.month,
            day
        )
        # Format as DD-MM-YYYY
        formatted_date = selected_date.strftime("%d-%m-%Y")
        # Update parent entry
        self.parent.set_date(formatted_date)
        # Close popup
        self.destroy() 