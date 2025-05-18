"""
Constants for the person management package.
"""

# Search modes
SEARCH_MODES = ["الطلاب", "المعلمات"]

# Academic levels
ACADEMIC_LEVELS = ["الجميع", "التمهيدي", "المستوى الأول", "المستوى الثاني", "فصل الصغار", "اشتراك يومي"]

# Fee types
FEE_TYPES = [
    "القسط الأول",
    "القسط الثاني",
    "القسط الثالث",
    "الملابس او القسط الرابع*"
]

# Gender options
GENDER_OPTIONS = {
    "male": "ذكر",
    "female": "أنثى"
}

# UI Constants (similar to registration, can be harmonized later if needed)
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

SEARCH_BUTTON_STYLE = {
    "width": 80
}

ACTION_BUTTON_STYLE = {
    "width": 50
}

SALARY_BUTTON_STYLE = {
    "width": 70,
    "fg_color": "#E91E63"
}

TABLE_HEADER_STYLE = {
    "font": ("Arial", 16, "bold"),
    "width": 120,
    "anchor": "center"
}

TABLE_ROW_STYLE = {
    "width": 120
} 