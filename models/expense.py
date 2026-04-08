import uuid
from datetime import datetime as dt

class Expense:
    def __init__(self, name: str, amount: float, category: str):
        self.name = name
        self.amount = amount
        self.date = dt.now()
        self.category = category
        self.id = uuid.uuid4()

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data: dict):
        expense = cls(data["name"], data["amount"], data["category"])
        expense.id = uuid.UUID(data["id"])
        expense.date = dt.strptime(data["date"], "%Y-%m-%d %H:%M:%S")
        return expense

    def read_expense(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "date": self.date,
            "category": self.category,
            "id": self.id
        }

    def update_expense(self, fields_to_update: dict):
        for key, value in fields_to_update.items():
            if key in ["name", "amount", "date", "category"]:
                setattr(self, key, value)
            else:
                raise ValueError("Expense property not found")

    def display_expense(self):
        print(f"Expense: {self.name}")
        print(f"Amount: {self.amount}")
        print(f"Date: {self.date.strftime('%A, %B %d, %Y')}")
        print(f"Time: {self.date.strftime('%H:%M:%S')}")
        print(f"Category: {self.category}")