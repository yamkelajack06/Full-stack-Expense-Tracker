from pathlib import Path
import json

BASE_DIR = Path(__file__).parent.parent
FILE_PATH = BASE_DIR / "data" / "data.json"

def read_expenses_data() -> list:
    FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not FILE_PATH.exists() or FILE_PATH.stat().st_size == 0:
        FILE_PATH.write_text("[]")
    
    with open(FILE_PATH, "r") as file:
        return json.load(file)

def update_expenses_data(expenses: list) -> None:
    FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(FILE_PATH, "w") as file:
        json.dump([expense.to_dict() for expense in expenses], file, indent=4)