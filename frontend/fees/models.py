from backend.database import (
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
    """Represents the data access layer for fees-related operations."""
    @staticmethod
    def add_expense(description: str, amount: float, date: str) -> None:
        """Adds a new general expense record to the database.

        Args:
            description: The description of the expense.
            amount: The amount of the expense.
            date: The date of the expense (string, format depends on backend).
        """
        # Calls the backend function to add a general expense
        add_general_expense(description, amount, date)

    @staticmethod
    def get_all_expenses():
        """Retrieves all general expense records from the database.

        Returns:
            A list of all general expense records.
        """
        # Calls the backend function to get all general expenses
        return get_all_general_expenses()

    @staticmethod
    def delete_expense(expense_id: int) -> None:
        """Deletes a general expense record from the database by its ID.

        Args:
            expense_id: The ID of the expense to delete.
        """
        # Calls the backend function to delete an expense
        delete_expense(expense_id)

    @staticmethod
    def update_expense(expense_id: int, description: str, amount: float, date: str) -> None:
        """Updates an existing general expense record in the database.

        Args:
            expense_id: The ID of the expense to update.
            description: The updated description.
            amount: The updated amount.
            date: The updated date.
        """
        # Calls the backend function to update an expense
        update_expense(expense_id, description, amount, date)

    @staticmethod
    def add_income(description: str, amount: float, date: str) -> None:
        """Adds a new income record to the database.

        Args:
            description: The description of the income.
            amount: The amount of the income.
            date: The date of the income.
        """
        # Calls the backend function to add income
        add_income(description, amount, date)

    @staticmethod
    def get_all_income():
        """Retrieves all income records from the database.

        Returns:
            A list of all income records.
        """
        # Calls the backend function to get all income records
        return get_all_income()

    @staticmethod
    def delete_income(income_id: int) -> None:
        """Deletes an income record from the database by its ID.

        Args:
            income_id: The ID of the income to delete.
        """
        # Calls the backend function to delete income
        delete_income(income_id)

    @staticmethod
    def update_income(income_id: int, description: str, amount: float, date: str) -> None:
        """Updates an existing income record in the database.

        Args:
            income_id: The ID of the income to update.
            description: The updated description.
            amount: The updated amount.
            date: The updated date.
        """
        # Calls the backend function to update income
        update_income(income_id, description, amount, date)

    @staticmethod
    def get_summary():
        """Retrieves the financial summary from the database.

        Returns:
            A dictionary containing the financial summary.
        """
        # Calls the backend function to get the financial summary
        return get_summary() 