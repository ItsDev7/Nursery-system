import sqlite3

def get_connection():
    return sqlite3.connect("students.db")

def create_students_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            nid TEXT,
            term TEXT,
            gender TEXT,
            phone1 TEXT,
            phone2 TEXT,
            fee1 TEXT,
            fee2 TEXT,
            fee3 TEXT,
            fee4 TEXT,
            fee1_date TEXT,
            fee2_date TEXT,
            fee3_date TEXT,
            fee4_date TEXT
        )
    """)

    conn.commit()
    conn.close()

def create_general_expenses_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS general_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()
    
def create_income_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

def create_activities_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            activity_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_student(name, nid, term, gender, phone1, phone2, fees, fee_dates):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (
            name, nid, term, gender, phone1, phone2,
            fee1, fee2, fee3, fee4,
            fee1_date, fee2_date, fee3_date, fee4_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, nid, term, gender, phone1, phone2,
        fees[0], fees[1], fees[2], fees[3],
        fee_dates[0], fee_dates[1], fee_dates[2], fee_dates[3]
    ))
    conn.commit()
    conn.close()


def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return [{
        "id": s[0],
        "name": s[1],
        "nid": s[2],
        "term": s[3],
        "gender": s[4],
        "phone1": s[5],
        "phone2": s[6],
        "fee1": s[7],
        "fee2": s[8],
        "fee3": s[9],
        "fee4": s[10],
        "fee1_date": s[11],
        "fee2_date": s[12],
        "fee3_date": s[13],
        "fee4_date": s[14]
    } for s in students]

def delete_student_by_name(name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def get_all_general_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount, date FROM general_expenses ORDER BY date DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_income():
    conn = get_connection()
    cursor = conn.cursor()
    
    # التحقق من وجود جدول income وإنشاؤه إذا لم يكن موجودًا
    try:
        # محاولة إنشاء الجدول إذا لم يكن موجودًا
        create_income_table()
        
        # استعلام البيانات
        cursor.execute("SELECT id, description, amount, date FROM income ORDER BY date DESC")
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"خطأ في قاعدة البيانات: {e}")
        # إرجاع قائمة فارغة في حالة حدوث خطأ
        data = []
    
    conn.close()
    return data


def get_summary():
    # حساب الإيرادات من رسوم الطلاب
    students = get_all_students()
    student_fees = 0
    for s in students:
        for i in range(1, 5):
            try:
                student_fees += float(s[f"fee{i}"] or 0)
            except:
                pass
    
    # حساب الإيرادات من جدول الإيرادات
    try:
        # التأكد من وجود جدول الإيرادات
        create_income_table()
        income_data = get_all_income()
        income_entries = sum(float(inc[2]) for inc in income_data) if income_data else 0
    except Exception as e:
        print(f"خطأ في حساب الإيرادات: {e}")
        income_entries = 0
    
    # إجمالي الإيرادات
    total_income = student_fees + income_entries
    
    # حساب المصروفات
    try:
        # التأكد من وجود جدول المصروفات
        create_general_expenses_table()
        expenses_data = get_all_general_expenses()
        expenses = sum(float(exp[2]) for exp in expenses_data) if expenses_data else 0
    except Exception as e:
        print(f"خطأ في حساب المصروفات: {e}")
        expenses = 0
        
    try:
        teacher_salaries = get_total_teacher_salaries() or 0
    except Exception as e:
        print(f"خطأ في حساب رواتب المعلمين: {e}")
        teacher_salaries = 0
        
    total_expenses = expenses + teacher_salaries
    
    return {
        "income": total_income,
        "expenses": total_expenses,
        "remaining": total_income - total_expenses,
        "teacher_salaries": teacher_salaries
    }
    
def add_general_expense(description, amount, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO general_expenses (description, amount, date)
        VALUES (?, ?, ?)
    """, (description, amount, date))
    conn.commit()
    conn.close()

def add_income(description, amount, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO income (description, amount, date)
        VALUES (?, ?, ?)
    """, (description, amount, date))
    conn.commit()
    conn.close()
    
def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM general_expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    
def delete_income(income_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
    conn.commit()
    conn.close()
    
def update_student(original_name, name, nid, term, gender, phone1, phone2, fees, fee_dates):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students 
        SET name=?, nid=?, term=?, gender=?, phone1=?, phone2=?, fee1=?, fee2=?, fee3=?, fee4=?, fee1_date=?, fee2_date=?, fee3_date=?, fee4_date=?
        WHERE name=?
    """, (name, nid, term, gender, phone1, phone2, fees[0], fees[1], fees[2], fees[3], fee_dates[0], fee_dates[1], fee_dates[2], fee_dates[3], original_name))
    conn.commit()
    conn.close()    

def update_expense(expense_id, new_desc, new_amount, new_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE general_expenses
        SET description=?, amount=?, date=?
        WHERE id=?
    """, (new_desc, new_amount, new_date, expense_id))
    conn.commit()
    conn.close()

def update_income(income_id, new_desc, new_amount, new_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE income
        SET description=?, amount=?, date=?
        WHERE id=?
    """, (new_desc, new_amount, new_date, income_id))
    conn.commit()
    conn.close()

def create_teachers_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            nid TEXT,
            term TEXT,
            gender TEXT,
            phone1 TEXT,
            phone2 TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_teacher(name, nid, term, gender, phone1, phone2):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO teachers (name, nid, term, gender, phone1, phone2)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, nid, term, gender, phone1, phone2))
    conn.commit()
    conn.close()

def get_all_teachers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    conn.close()
    return [{
        "id": t[0],
        "name": t[1],
        "nid": t[2],
        "term": t[3],
        "gender": t[4],
        "phone1": t[5],
        "phone2": t[6]
    } for t in teachers]    

def create_teacher_salaries_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacher_salaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER,
            amount REAL,
            date TEXT,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    """)
    conn.commit()
    conn.close()

def add_teacher_salary(teacher_id, amount, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO teacher_salaries (teacher_id, amount, date)
        VALUES (?, ?, ?)
    """, (teacher_id, amount, date))
    conn.commit()
    conn.close()

def get_teacher_salaries(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, date FROM teacher_salaries WHERE teacher_id = ? ORDER BY date DESC", (teacher_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def update_teacher_salary(salary_id: int, new_amount: float, new_date: str):
    """
    Update a teacher's salary record.
    
    Args:
        salary_id: The ID of the salary record to update
        new_amount: The new salary amount
        new_date: The new date in DD-MM-YYYY format
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE teacher_salaries
        SET amount = ?, date = ?
        WHERE id = ?
    """, (new_amount, new_date, salary_id))
    conn.commit()
    conn.close()

def get_total_teacher_salaries():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM teacher_salaries")
    total = cursor.fetchone()[0]
    conn.close()
    return total or 0

def get_students_by_term():
    """الحصول على عدد الطلاب وإجمالي الرسوم لكل فصل دراسي"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # الحصول على قائمة الفصول الدراسية المتاحة
    cursor.execute("SELECT DISTINCT term FROM students")
    terms = [term[0] for term in cursor.fetchall()]
    
    result = {}
    for term in terms:
        # عدد الطلاب في هذا الفصل
        cursor.execute("SELECT COUNT(*) FROM students WHERE term = ?", (term,))
        student_count = cursor.fetchone()[0]
        
        # إجمالي الرسوم لهذا الفصل
        cursor.execute("SELECT fee1, fee2, fee3, fee4 FROM students WHERE term = ?", (term,))
        fees_data = cursor.fetchall()
        
        total_fees = 0
        for fees in fees_data:
            for fee in fees:
                try:
                    if fee and fee.strip():
                        total_fees += float(fee)
                except (ValueError, TypeError):
                    pass
        
        result[term] = {
            "student_count": student_count,
            "total_fees": total_fees
        }
    
    conn.close()
    return result

def get_teachers_statistics():
    """الحصول على إحصائيات المعلمات"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # عدد المعلمات
    cursor.execute("SELECT COUNT(*) FROM teachers")
    teacher_count = cursor.fetchone()[0]
    
    # إجمالي الرواتب
    cursor.execute("SELECT SUM(amount) FROM teacher_salaries")
    total_salaries = cursor.fetchone()[0] or 0
    
    conn.close()
    return {
        "teacher_count": teacher_count,
        "total_salaries": total_salaries
    }

def get_detailed_statistics():
    """الحصول على إحصائيات مفصلة للنظام"""
    # إحصائيات الطلاب حسب الفصل
    students_stats = get_students_by_term()
    
    # إحصائيات المعلمات
    teachers_stats = get_teachers_statistics()
    
    # الملخص العام
    summary = get_summary()
    
    return {
        "students_by_term": students_stats,
        "teachers": teachers_stats,
        "summary": summary
    }

def add_activity(description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO activities (description, activity_date)
        VALUES (?, ?)
    """, (description, date))
    conn.commit()
    conn.close()

def get_all_activities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, activity_date FROM activities ORDER BY activity_date ASC")
    data = cursor.fetchall()
    conn.close()
    return data

def update_activity(activity_id, new_desc, new_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE activities
        SET description=?, activity_date=?
        WHERE id=?
    """, (new_desc, new_date, activity_id))
    conn.commit()
    conn.close()

def delete_activity(activity_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
    conn.commit()
    conn.close()

def update_teacher_by_id(teacher_id, name, nid, term, gender, phone1, phone2):
    """
    Update teacher details by teacher ID.

    Args:
        teacher_id: The ID of the teacher to update.
        name: New name.
        nid: New National ID.
        term: New academic term.
        gender: New gender.
        phone1: New primary phone number.
        phone2: New secondary phone number.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE teachers
        SET name=?, nid=?, term=?, gender=?, phone1=?, phone2=?
        WHERE id=?
    """, (name, nid, term, gender, phone1, phone2, teacher_id))
    conn.commit()
    conn.close()

def delete_teacher_by_name(name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def delete_teacher_by_id(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
    conn.commit()
    conn.close()