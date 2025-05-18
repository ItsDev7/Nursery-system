from datetime import datetime
from .models import FeesModel
from .utils import validate_amount, validate_date, show_error_message, show_confirmation_message

class FeesController:
    def __init__(self, view):
        self.view = view
        self.model = FeesModel()

    def add_expense(self, description: str, amount_str: str) -> bool:
        """Handle adding a new expense."""
        if not description or not amount_str:
            show_error_message("يجب إدخال كل من الوصف والمبلغ لإضافة المصروف")
            return False

        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            show_error_message("المبلغ يجب أن يكون رقمًا صحيحًا أو عشريًا")
            return False

        date = datetime.now().strftime("%Y-%m-%d")
        self.model.add_expense(description, amount, date)
        return True

    def add_income(self, description: str, amount_str: str) -> bool:
        """Handle adding a new income."""
        if not description or not amount_str:
            show_error_message("يجب إدخال كل من الوصف والمبلغ لإضافة الإيراد")
            return False

        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            show_error_message("المبلغ يجب أن يكون رقمًا صحيحًا أو عشريًا")
            return False

        date = datetime.now().strftime("%Y-%m-%d")
        self.model.add_income(description, amount, date)
        return True

    def delete_expense(self, expense_id: int) -> bool:
        """Handle deleting an expense."""
        if show_confirmation_message("هل أنت متأكد أنك تريد حذف هذا المصروف؟"):
            self.model.delete_expense(expense_id)
            return True
        return False

    def delete_income(self, income_id: int) -> bool:
        """Handle deleting an income."""
        if show_confirmation_message("هل أنت متأكد أنك تريد حذف هذا الإيراد؟"):
            self.model.delete_income(income_id)
            return True
        return False

    def update_expense(self, expense_id: int, description: str, amount_str: str, date_str: str) -> bool:
        """Handle updating an expense."""
        if not description or not amount_str or not date_str:
            show_error_message("يجب إدخال كل من الوصف والمبلغ والتاريخ")
            return False

        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            show_error_message("المبلغ يجب أن يكون رقمًا")
            return False

        if not validate_date(date_str):
            show_error_message("صيغة التاريخ غير صحيحة. يرجى استخدام DD-MM-YYYY.")
            return False

        self.model.update_expense(expense_id, description, amount, date_str)
        return True

    def update_income(self, income_id: int, description: str, amount_str: str, date_str: str) -> bool:
        """Handle updating an income."""
        if not description or not amount_str or not date_str:
            show_error_message("يجب إدخال كل من الوصف والمبلغ والتاريخ")
            return False

        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            show_error_message("المبلغ يجب أن يكون رقمًا")
            return False

        if not validate_date(date_str):
            show_error_message("صيغة التاريخ غير صحيحة. يرجى استخدام DD-MM-YYYY.")
            return False

        self.model.update_income(income_id, description, amount, date_str)
        return True

    def get_all_expenses(self):
        """Get all expenses."""
        return self.model.get_all_expenses()

    def get_all_income(self):
        """Get all income records."""
        return self.model.get_all_income()

    def get_summary(self):
        """Get financial summary."""
        return self.model.get_summary() 