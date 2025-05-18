from datetime import datetime
from backend.database import (
    get_all_students,
    add_general_expense,
    get_all_general_expenses,
    get_summary,
    add_income,
    get_all_income,
    delete_income,
    update_income,
    delete_expense,
    update_expense
)

class FeesModel:
    @staticmethod
    def add_expense(description: str, amount: float, date: str) -> None:
        """Add a new expense to the database."""
        add_general_expense(description, amount, date)

    @staticmethod
    def get_all_expenses():
        """Get all expenses from the database."""
        return get_all_general_expenses()

    @staticmethod
    def delete_expense(expense_id: int) -> None:
        """Delete an expense from the database."""
        delete_expense(expense_id)

    @staticmethod
    def update_expense(expense_id: int, description: str, amount: float, date: str) -> None:
        """Update an existing expense in the database."""
        update_expense(expense_id, description, amount, date)

    @staticmethod
    def add_income(description: str, amount: float, date: str) -> None:
        """Add a new income to the database."""
        add_income(description, amount, date)

    @staticmethod
    def get_all_income():
        """Get all income records from the database."""
        return get_all_income()

    @staticmethod
    def delete_income(income_id: int) -> None:
        """Delete an income record from the database."""
        delete_income(income_id)

    @staticmethod
    def update_income(income_id: int, description: str, amount: float, date: str) -> None:
        """Update an existing income record in the database."""
        update_income(income_id, description, amount, date)

    @staticmethod
    def get_summary():
        """Get the financial summary from the database."""
        return get_summary() 