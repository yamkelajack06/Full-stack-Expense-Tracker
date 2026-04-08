# Flo — Expense Tracker

Flo is a simple full-stack expense tracker built for learning purposes. The emphasis is on learning the basics of **FastAPI** and how to wire up a REST API to a frontend.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Data Persistence | Local JSON file (`data/data.json`) |

Expenses are saved to a JSON file on disk. Every time an expense is added, edited, or deleted, the file is rewritten with the updated list no database required just yet, but there are plans of adding it in the future.

---

## How It Works

The FastAPI backend exposes a set of REST endpoints that the frontend communicates with via the Fetch API. When you open the app, it loads your expenses from the API and displays them across three views:

- **Dashboard** — an overview of total spending with a breakdown by category
- **Expenses** — a full list where you can add, edit, delete, and search
- **Filter** — lets you slice expenses by category, month/year, or a custom date range

The backend handles all the logic including filtering, searching, and on the other hand, the frontend stays focused on displaying data and handling user interactions.
