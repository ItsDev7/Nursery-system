"""
Constants and shared data for the registration system.
"""

# Academic levels
ACADEMIC_LEVELS = [
    "التمهيدي",
    "الاول المستوى",
    "الثاني المستوى",
    "الصغار فصل",
    "يومي اشتراك"
]

# Gender options
GENDER_OPTIONS = {
    "male": "ذكر",
    "female": "أنثى"
}

# Fee types
FEE_TYPES = [
    "القسط الأول",
    "القسط الثاني",
    "القسط الثالث",
    "الملابس او القسط الرابع*"
]

# UI Constants
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

REGISTER_BUTTON_STYLE = {
    "font": ("Arial", 18),
    "height": 40,
    "width": 200
}

LABEL_STYLE = {
    "font": ("Arial", 16, "bold"),
    "anchor": "e",
    "justify": "right"
}

ENTRY_STYLE = {
    "width": 300,
    "justify": "right",
    "font": ("Arial", 14)
}

OPTION_MENU_STYLE = {
    "font": ("Arial", 14)
} 