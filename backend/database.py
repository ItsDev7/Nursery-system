import sqlite3

# --- Database Connection ---

def get_connection():
    """Establishes and returns a connection to the students.db SQLite database."""
    return sqlite3.connect("students.db")

# --- Table Creation ---

def create_students_table():
    """Creates the students table if it doesn't already exist."""
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
    """Creates the general_expenses table if it doesn't already exist."""
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
    """Creates the income table if it doesn't already exist."""
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
    """Creates the activities table if it doesn't already exist."""
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

def create_teachers_table():
    """Creates the teachers table if it doesn't already exist."""
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

def create_teacher_salaries_table():
    """Creates the teacher_salaries table if it doesn't already exist."""
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

def create_settings_table():
    """Creates the settings table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Data Insertion ---

def add_student(name, nid, term, gender, phone1, phone2, fees, fee_dates):
    """Adds a new student record to the students table."""
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

def add_general_expense(description, amount, date):
    """Adds a new general expense record to the general_expenses table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Attempt to convert amount to float before inserting
        amount_float = float(amount) if amount is not None and str(amount).strip() != '' else 0.0
        cursor.execute("""
            INSERT INTO general_expenses (description, amount, date)
            VALUES (?, ?, ?)
        """, (description, amount_float, date))
        conn.commit()
    except (ValueError, TypeError) as e:
        print(f"Error adding general expense: Invalid amount '{amount}'. Error: {e}")
        conn.rollback()
    except sqlite3.Error as e:
        print(f"Database error adding general expense: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_income(description, amount, date):
    """Adds a new income record to the income table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Attempt to convert amount to float before inserting
        amount_float = float(amount) if amount is not None and str(amount).strip() != '' else 0.0
        cursor.execute("""
            INSERT INTO income (description, amount, date)
            VALUES (?, ?, ?)
        """, (description, amount_float, date))
        conn.commit()
    except (ValueError, TypeError) as e:
        print(f"Error adding income: Invalid amount '{amount}'. Error: {e}")
        conn.rollback() # Rollback the transaction on error
    except sqlite3.Error as e:
        print(f"Database error adding income: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_teacher(name, nid, term, gender, phone1, phone2):
    """Adds a new teacher record to the teachers table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO teachers (name, nid, term, gender, phone1, phone2)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, nid, term, gender, phone1, phone2))
    conn.commit()
    conn.close()

def add_teacher_salary(teacher_id, amount, date):
    """Adds a new teacher salary record to the teacher_salaries table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO teacher_salaries (teacher_id, amount, date)
        VALUES (?, ?, ?)
    """, (teacher_id, amount, date))
    conn.commit()
    conn.close()

def add_activity(description, date):
    """Adds a new activity record to the activities table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO activities (description, activity_date)
        VALUES (?, ?)
    """, (description, date))
    conn.commit()
    conn.close()

def save_setting(key, value):
    """Saves a key-value pair setting into the settings table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        create_settings_table() # Ensure table exists
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error saving setting '{key}': {e}")
        conn.rollback()
    finally:
        conn.close()

# --- Data Retrieval ---

def get_all_students():
    """Retrieves all student records from the students table."""
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

def get_all_general_expenses():
    """Retrieves all general expense records from the general_expenses table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        create_general_expenses_table()  # Ensure table exists
        cursor.execute("SELECT id, description, amount, date FROM general_expenses ORDER BY date DESC")
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error in get_all_general_expenses: {e}")
        data = []
    finally:
        conn.close()
    return data

def get_all_income():
    """Retrieves all income records from the income table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        create_income_table()  # Ensure table exists
        cursor.execute("SELECT id, description, amount, date FROM income ORDER BY date DESC")
        data = []
        for row in cursor.fetchall():
            try:
                # Attempt to convert amount to float, handle errors
                amount = float(row[2]) if row[2] is not None and str(row[2]).strip() != '' else 0.0
                data.append((row[0], row[1], amount, row[3]))
            except (ValueError, TypeError, IndexError) as e:
                print(f"Error converting income amount for row {row}: {e}")
                data.append((row[0], row[1], 0.0, row[3]))
    except sqlite3.Error as e:
        print(f"Database error in get_all_income: {e}")
        data = []
    finally:
        conn.close()
    return data

def get_all_teachers():
    """Retrieves all teacher records from the teachers table."""
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

def get_teacher_salaries(teacher_id):
    """Retrieves salary records for a specific teacher."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, date FROM teacher_salaries WHERE teacher_id = ? ORDER BY date DESC", (teacher_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_activities():
    """Retrieves all activity records from the activities table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, activity_date FROM activities ORDER BY activity_date ASC")
    data = cursor.fetchall()
    conn.close()
    return data

def get_students_by_term():
    """Gets the count of students and total fees per academic term."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT term FROM students")
    terms = [term[0] for term in cursor.fetchall() if term[0] is not None and str(term[0]).strip() != ''] # Filter out None or empty terms
    result = {}
    for term in terms:
        # Student count for this term
        cursor.execute("SELECT COUNT(*) FROM students WHERE term = ?", (term,))
        student_count = cursor.fetchone()[0] or 0
        # Total fees for this term
        cursor.execute("SELECT fee1, fee2, fee3, fee4 FROM students WHERE term = ?", (term,))
        fees_data = cursor.fetchall()
        total_fees = 0
        for fees in fees_data:
            for fee in fees:
                try:
                    if fee is not None and str(fee).strip() != '':
                        total_fees += float(fee)
                except (ValueError, TypeError):
                    # Handle cases where fee value is not a valid number
                    print(f"Error converting fee value '{fee}' to float for term {term}")
                    pass # Skip invalid fee values
        result[term] = {
            "student_count": student_count,
            "total_fees": total_fees
        }
    conn.close()
    return result

def get_teachers_statistics():
    """Gets overall teacher statistics (count and total salaries)."""
    conn = get_connection()
    cursor = conn.cursor()
    # Teacher count
    cursor.execute("SELECT COUNT(*) FROM teachers")
    teacher_count = cursor.fetchone()[0] or 0
    # Total salaries
    cursor.execute("SELECT SUM(amount) FROM teacher_salaries")
    total_salaries = cursor.fetchone()[0] or 0
    conn.close()
    return {
        "teacher_count": teacher_count,
        "total_salaries": total_salaries
    }

def get_total_teacher_salaries():
    """Calculates the total amount of all teacher salaries."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM teacher_salaries")
    total = cursor.fetchone()[0]
    conn.close()
    return total or 0

def get_setting(key):
    """Retrieves the value for a given setting key from the settings table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        create_settings_table() # Ensure table exists
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Database error getting setting '{key}': {e}")
        return None
    finally:
        conn.close()

# --- Statistical Summaries ---

def get_summary():
    """Calculates a financial summary including total income, expenses, and remaining balance."""
    # Calculate income from student fees
    students = get_all_students()
    student_fees = 0
    for s in students:
        # s is a dictionary from get_all_students
        for i in range(1, 5): # Iterate through fees 1 to 4
            fee_key = f"fee{i}"
            try:
                fee_value = s.get(fee_key) # Use .get() for safety
                if fee_value is not None and str(fee_value).strip() != '':
                     student_fees += float(fee_value)
            except (ValueError, TypeError):
                # Handle cases where fee value is not a valid number
                pass # Skip invalid fee values

    # Calculate income from the income table
    try:
        income_data = get_all_income()
        # Ensure income_entries is calculated from the correct amount column (index 2)
        income_entries = sum(float(inc[2]) for inc in income_data if inc and len(inc) > 2 and inc[2] is not None and str(inc[2]).strip()) if income_data else 0
    except Exception as e:
        print(f"Error calculating income from Income table: {e}")
        income_entries = 0

    # Total income
    total_income = student_fees + income_entries

    # Calculate general expenses
    try:
        # Ensure table exists
        create_general_expenses_table()
        expenses_data = get_all_general_expenses()
        expenses = sum(float(exp[2]) for exp in expenses_data) if expenses_data else 0
    except Exception as e:
        print(f"Error calculating general expenses: {e}")
        expenses = 0

    # Calculate teacher salaries
    try:
        teacher_salaries = get_total_teacher_salaries() or 0
    except Exception as e:
        print(f"Error calculating teacher salaries: {e}")
        teacher_salaries = 0

    # Total expenses
    total_expenses = expenses + teacher_salaries

    return {
        "income": total_income,
        "expenses": total_expenses,
        "remaining": total_income - total_expenses,
        "teacher_salaries": teacher_salaries
    }

def get_detailed_statistics():
    """Gets detailed statistics including student stats by term, teacher stats, and overall financial summary."""
    # Student stats by term
    students_stats = get_students_by_term()
    # Teacher stats
    teachers_stats = get_teachers_statistics()
    # Overall summary
    summary = get_summary()
    return {
        "students_by_term": students_stats,
        "teachers": teachers_stats,
        "summary": summary
    }

# --- Data Update ---

def update_student(original_name, name, nid, term, gender, phone1, phone2, fees, fee_dates):
    """Updates an existing student record based on the original name."""
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
    """Updates an existing general expense record."""
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
    """Updates an existing income record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE income
        SET description=?, amount=?, date=?
        WHERE id=?
    """, (new_desc, new_amount, new_date, income_id))
    conn.commit()
    conn.close()

def update_teacher_salary(salary_id: int, new_amount: float, new_date: str):
    """Updates a teacher's salary record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE teacher_salaries
        SET amount = ?, date = ?
        WHERE id = ?
    """, (new_amount, new_date, salary_id))
    conn.commit()
    conn.close()

def update_activity(activity_id, new_desc, new_date):
    """Updates an existing activity record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE activities
        SET description=?, activity_date=?
        WHERE id=?
    """, (new_desc, new_date, activity_id))
    conn.commit()
    conn.close()

def update_teacher_by_id(teacher_id, name, nid, term, gender, phone1, phone2):
    """Updates teacher details by teacher ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE teachers
        SET name=?, nid=?, term=?, gender=?, phone1=?, phone2=?
        WHERE id=?
    """, (name, nid, term, gender, phone1, phone2, teacher_id))
    conn.commit()
    conn.close()

# --- Data Deletion ---

def delete_student_by_name(name: str):
    """Deletes a student record based on the name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    """Deletes a general expense record by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM general_expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def delete_income(income_id):
    """Deletes an income record by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
    conn.commit()
    conn.close()

def delete_activity(activity_id):
    """Deletes an activity record by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
    conn.commit()
    conn.close()

def delete_teacher_by_name(name: str):
    """Deletes a teacher record based on the name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def delete_teacher_by_id(teacher_id):
    """Deletes a teacher record by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
    conn.commit()
    conn.close()