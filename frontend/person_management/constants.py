"""
Constants for the person management package.

This module contains various constants used throughout the person management
related files, including search modes, academic levels, gender options, and UI styles.
"""

# --- Search Modes ---
# Defines the available modes for searching (e.g., Students, Teachers)
SEARCH_MODES = ["الطلاب", "المعلمات"]

# --- Academic Levels ---
# Defines the different academic levels available for students and teachers
ACADEMIC_LEVELS = ["الجميع", "التمهيدي", "الاول المستوى", "الثاني المستوى", "الصغار فصل", "يومي اشتراك"]

# --- Fee Types ---
# Defines the types of fees associated with students
FEE_TYPES = [
    "القسط الأول",
    "القسط الثاني",
    "القسط الثالث",
    "الملابس او القسط الرابع*" # Clothing or Fourth Installment*
]

# --- Gender Options ---
# Maps English keys to Arabic values for gender representation
GENDER_OPTIONS = {
    "male": "ذكر",
    "female": "أنثى"
}

# --- UI Styles ---
# Defines common styling dictionaries for various CTkinter widgets

# Style for back buttons (e.g., on detail or edit pages)
BACK_BUTTON_STYLE = {
    "text": "←",
    "font": ("Arial", 18, "bold"),
    "width": 40,
    "height": 40,
    "fg_color": "#ff3333",
    "text_color": "#000000",
    "hover_color": "#b71c1c",
    "corner_radius": 20
}

# Style for the main search button
SEARCH_BUTTON_STYLE = {
    "width": 80
}

# Default style for action buttons (e.g., View, Edit)
ACTION_BUTTON_STYLE = {
    "width": 50
}

# Style for the teacher salary button
SALARY_BUTTON_STYLE = {
    "width": 70,
    "fg_color": "#E91E63"
}

# Style for table header labels in search results
TABLE_HEADER_STYLE = {
    "font": ("Arial", 16, "bold"),
    "width": 120,
    "anchor": "center"
}

# Default style for labels displaying data in table rows
TABLE_ROW_STYLE = {
    "width": 120
} 