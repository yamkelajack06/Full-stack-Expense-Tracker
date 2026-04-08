from models.expense import Expense
from datetime import datetime as dt
from utils.file_handler import read_expenses_data, update_expenses_data
from utils.decoraters import log_action, validate_input, timer


class Expense_Tracker:
    def __init__(self):
        self.expenses: list[Expense] = self.load_expenses_data()
        self.categories: dict = {}

    # load local data
    @log_action
    @timer
    def load_expenses_data(self) -> list:
        data = read_expenses_data()
        if data:
            return [Expense.from_dict(e) for e in data]
        return []

    # crud functions
    @log_action
    @validate_input
    @timer
    def add_expense(self, name: str, amount: float, category: str) -> None:
        new_expense = Expense(name, amount, category)
        self.expenses.append(new_expense)
        update_expenses_data(self.expenses)

    @log_action
    @timer
    def delete_expense(self, expense: Expense) -> None:
        for exp in self.expenses:
            if exp.id == expense.id:
                self.expenses.remove(expense)
                update_expenses_data(self.expenses)

    @log_action
    @timer
    def view_expenses(self) -> None:
        for expense in self.expenses:
            expense.display_expense()

    @log_action
    @validate_input
    @timer
    def update_expenses(self, expense: Expense, fields_to_update: dict) -> None:
        for exp in self.expenses:
            if exp.id == expense.id:
                exp.update_expense(fields_to_update)
                update_expenses_data(self.expenses)

    # filter and search functions
    def filter_expenses(self, condition: str) -> list[Expense]:
        filtered: list[Expense] = []
        match condition:
            case "category":
                filtered = self.filter_by_category()
                return filtered
            case "month and year":
                filtered = self.filter_by_month_and_year()
                return filtered
            case "date range":
                filtered = self.filter_by_date_range()
                return filtered
            case _:
                print("Expense not found")

    @timer
    def filter_by_category(self, category: str) -> list[Expense]:
        filtered: list[Expense] = []
        for expense in self.expenses:
            if category in expense.category:
                filtered.append(expense)
        return filtered

    @timer
    def filter_by_month_and_year(self, month_and_year: dict):
        filtered: list[Expense] = []
        for expense in self.expenses:
            if expense.date.month == month_and_year["month"] and expense.date.year == month_and_year["year"]:
                filtered.append(expense)
        return filtered

    @timer
    def filter_by_date_range(self, start: dt, end: dt):
        filtered: list[Expense] = []
        for expense in self.expenses:
            if self.is_within_range(expense.date, start, end):
                filtered.append(expense)
        return filtered

    # date helper function
    def is_within_range(self, date: dt, start: dt, end: dt) -> bool:
        return start <= date <= end

    @log_action
    @timer
    def search_expense(self, search_query: str) -> list[Expense]:
        found: list[Expense] = []
        for expense in self.expenses:
            if search_query.lower() in expense.name.lower():
                found.append(expense)
        if not found:
            print("Expense not found")
            return []
        return found

    # sorting functions
    def identify_categories(self) -> dict:
        categories: dict = {}
        for expense in self.expenses:
            if expense.category not in categories:
                categories[expense.category] = {"items": [], "items_count": 0}
        self.categories = categories

    def organize_expenses(self) -> None:
        self.identify_categories()
        for expense in self.expenses:
            if expense.category in self.categories:
                self.categories[expense.category]["items"].append(expense)
                self.categories[expense.category]["items_count"] += 1

    @timer
    def calculate_total_spending(self) -> float:
        total: float = 0
        for expense in self.expenses:
            total += expense.amount
        return total

    @timer
    def calculate_spending_by_category(self):
        results: dict[str, float] = {}
        for category, category_data in self.categories.items():
            category_total = 0
            for expense in category_data["items"]:
                category_total += expense.amount
            results[category] = category_total
        return results

    # spending functions
    def display_spending_summary(self) -> dict:
        spending_by_category: dict[str, float] = self.calculate_spending_by_category()
        total_spending: float = self.calculate_total_spending()

        return {
            "spending_by_category": spending_by_category,
            "total": total_spending
        }

class TimeTracker extends C