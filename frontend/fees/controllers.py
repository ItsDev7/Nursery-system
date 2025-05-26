from datetime import datetime
from .models import FeesModel
from .utils import validate_amount, validate_date, show_error_message, show_confirmation_message

class FeesController:
    """Handles the business logic and interactions between the Fees UI and the data model."""

    def __init__(self, view):
        """
        Initializes the FeesController.

        Args:
            view: Reference to the FeesPage view instance.
        """
        self.view = view
        # Instantiate the data model for fees operations
        self.model = FeesModel()

    def add_expense(self, description: str, amount_str: str) -> bool:
        """Handle adding a new expense.

        Validates input, adds the expense to the database, and returns success status.

        Args:
            description: The description of the expense.
            amount_str: The expense amount as a string.

        Returns:
            True if the expense was added successfully, False otherwise.
        """
        # Validate required fields
        if not description or not amount_str:
            show_error_message("يجب إدخال كل من الوصف والمبلغ لإضافة المصروف")
            return False

        # Validate and convert amount
        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            show_error_message("المبلغ يجب أن يكون رقمًا صحيحًا أو عشريًا")
            return False

        # Get current date in YYYY-MM-DD format
        date = datetime.now().strftime("%Y-%m-%d")
        # Add expense to the database
        self.model.add_expense(description, amount, date)
        return True

    def add_income(self, description: str, amount_str: str) -> bool:
        """Handle adding a new income.

        Validates input, adds the income to the database, and returns success status.

        Args:
            description: The description of the income.
            amount_str: The income amount as a string.

        Returns:
            True if the income was added successfully, False otherwise.
        """
        # Validate required fields
        if not description or not amount_str:
            show_error_message("يجب إدخال كل من الوصف والمبلغ لإضافة الإيراد")
            return False

        # Validate and convert amount
        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            show_error_message("المبلغ يجب أن يكون رقمًا صحيحًا أو عشريًا")
            return False

        # Get current date in YYYY-MM-DD format
        date = datetime.now().strftime("%Y-%m-%d")
        # Add income to the database
        self.model.add_income(description, amount, date)
        return True

    def delete_expense(self, expense_id: int) -> bool:
        """Handle deleting an expense.

        Shows a confirmation dialog and deletes the expense from the database if confirmed.

        Args:
            expense_id: The ID of the expense to delete.

        Returns:
            True if the expense was deleted, False otherwise (if cancelled).
        """
        # Show confirmation dialog
        if show_confirmation_message("هل أنت متأكد أنك تريد حذف هذا المصروف؟"):
            # Delete expense from the database
            self.model.delete_expense(expense_id)
            return True
        return False

    def delete_income(self, income_id: int) -> bool:
        """Handle deleting an income.

        Shows a confirmation dialog and deletes the income from the database if confirmed.

        Args:
            income_id: The ID of the income to delete.

        Returns:
            True if the income was deleted, False otherwise (if cancelled).
        """
        # Show confirmation dialog
        if show_confirmation_message("هل أنت متأكد أنك تريد حذف هذا الإيراد؟"):
            # Delete income from the database
            self.model.delete_income(income_id)
            return True
        return False

    def update_expense(self, expense_id: int, description: str, amount_str: str, date_str: str) -> bool:
        """Handle updating an expense.

        Validates input, updates the expense in the database, and returns success status.

        Args:
            expense_id: The ID of the expense to update.
            description: The updated description.
            amount_str: The updated amount as a string.
            date_str: The updated date string (expected DD-MM-YYYY).

        Returns:
            True if the expense was updated successfully, False otherwise.
        """
        # Validate required fields
        if not description or not amount_str or not date_str:
            show_error_message("يجب إدخال كل من الوصف والمبلغ والتاريخ")
            return False

        # Validate and convert amount
        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            show_error_message("المبلغ يجب أن يكون رقمًا")
            return False

        # Validate date format
        if not validate_date(date_str):
            show_error_message("صيغة التاريخ غير صحيحة. يرجى استخدام DD-MM-YYYY.")
            return False

        # Update expense in the database
        self.model.update_expense(expense_id, description, amount, date_str)
        return True

    def update_income(self, income_id: int, description: str, amount_str: str, date_str: str) -> bool:
        """Handle updating an income.

        Validates input, updates the income in the database, and returns success status.

        Args:
            income_id: The ID of the income to update.
            description: The updated description.
            amount_str: The updated amount as a string.
            date_str: The updated date string (expected DD-MM-YYYY).

        Returns:
            True if the income was updated successfully, False otherwise.
        """
        # Validate required fields
        if not description or not amount_str or not date_str:
            show_error_message("يجب إدخال كل من الوصف والمبلغ والتاريخ")
            return False

        # Validate and convert amount
        is_valid, amount = validate_amount(amount_str)
        if not is_valid:
            show_error_message("المبلغ يجب أن يكون رقمًا")
            return False

        # Validate date format
        if not validate_date(date_str):
            show_error_message("صيغة التاريخ غير صحيحة. يرجى استخدام DD-MM-YYYY.")
            return False

        # Update income in the database
        self.model.update_income(income_id, description, amount, date_str)
        return True

    def get_all_expenses(self):
        """Get all expenses.

        Returns:
            A list of all expense records.
        """
        return self.model.get_all_expenses()

    def get_all_income(self):
        """Get all income records.

        Returns:
            A list of all income records.
        """
        return self.model.get_all_income()

    def get_summary(self):
        """Get financial summary.

        Returns:
            A dictionary containing income, expenses, and remaining balance.
        """
        return self.model.get_summary() 