import database

def init_database():
    database.create_students_table()
    database.create_general_expenses_table()
    database.create_teachers_table()
    database.create_teacher_salaries_table()
    database.create_income_table()
    

init_database()
