# Smart Expense Tracker API

A REST API built with FastAPI for managing personal expenses. The application stores expenses in a local JSON file and supports creating, listing, filtering, deleting, and calculating expense totals.

## Prerequisites

- Python 3.13+
- Git

## Setup

Clone the repository and create a virtual environment.

```powershell
git clone https://github.com/tanmaynag12/smart-expense-tracker
cd smart-expense-tracker

python -m venv venv
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

For macOS/Linux:

```bash
source venv/bin/activate
```

## Running the API

Start the FastAPI development server:

```powershell
uvicorn src.main:app --reload
```

Once the server is running:

- API: http://127.0.0.1:8000
- Interactive API documentation (Swagger): http://127.0.0.1:8000/docs

## Running the Tests

Run the complete test suite:

```powershell
pytest
```

All tests are located in the `tests/` directory.

## API Endpoints

| Method | Endpoint                        | Description                                             |
| ------ | ------------------------------- | ------------------------------------------------------- |
| POST   | `/expenses`                     | Create a new expense                                    |
| GET    | `/expenses`                     | Retrieve all expenses                                   |
| GET    | `/expenses?category={category}` | Filter expenses by category                             |
| GET    | `/expenses/total`               | Return the overall total and totals grouped by category |
| DELETE | `/expenses/{expense_id}`        | Delete an expense by its ID                             |

## Project Structure

```text
smart-expense-tracker/
│
├── src/
│   ├── main.py          # FastAPI routes
│   ├── models.py        # Pydantic models
│   └── storage.py       # JSON storage and CRUD operations
│
├── tests/
│   └── test_expenses.py
│
├── data/
│   └── expenses.json    # Created automatically on first run
│
├── README.md
├── AI_NOTES.md
└── requirements.txt
```

## Notes

- Expense data is stored in `data/expenses.json`.
- The JSON file is created automatically the first time an expense is added.
- Automated tests use a temporary JSON file, so they never modify your real data.
- AI usage, design decisions, and validation steps are documented in `AI_NOTES.md`.
