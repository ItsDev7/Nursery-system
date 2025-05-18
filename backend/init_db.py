import sqlite3
from .database import create_students_table, create_general_expenses_table, create_teachers_table, create_teacher_salaries_table, create_income_table, create_activities_table

def init_database():
    """تهيئة جميع جداول قاعدة البيانات المطلوبة للتطبيق"""
    # إنشاء جميع الجداول المطلوبة
    create_students_table()
    create_general_expenses_table()
    create_teachers_table()
    create_teacher_salaries_table()
    create_income_table()
    create_activities_table()
    
    print("تم تهيئة قاعدة البيانات بنجاح")