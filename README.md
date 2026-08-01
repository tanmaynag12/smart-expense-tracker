# Smart Expense Tracker API

A REST API built with FastAPI for managing personal expenses. Expenses are stored in a local JSON file, and the API supports creating, listing, filtering, searching, deleting, and calculating expense totals.

## Prerequisites

- Python 3.13+
- Git

## Setup

Clone the repository, create a virtual environment, and install the project dependencies.

### Windows (PowerShell)

```powershell
git clone https://github.com/tanmaynag12/smart-expense-tracker
cd smart-expense-tracker

python -m venv venv
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### macOS / Linux

```bash
git clone https://github.com/tanmaynag12/smart-expense-tracker
cd smart-expense-tracker

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Running the API

Start the FastAPI server:

```powershell
uvicorn src.main:app --reload
```

Once the server is running:

- **API:** http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs

## Running the Tests

Run the complete test suite:

```powershell
pytest
```

All automated tests are located in the `tests/` directory.

## API Endpoints

| Method | Endpoint                                 | Description                                             |
| ------ | ---------------------------------------- | ------------------------------------------------------- |
| POST   | `/expenses`                              | Create a new expense                                    |
| GET    | `/expenses`                              | Retrieve all expenses                                   |
| GET    | `/expenses?category={category}`          | Filter expenses by category                             |
| GET    | `/expenses?q={text}`                     | Search expense titles _(bonus feature)_                 |
| GET    | `/expenses?category={category}&q={text}` | Combine category filtering and title search             |
| GET    | `/expenses/total`                        | Return the overall total and totals grouped by category |
| DELETE | `/expenses/{expense_id}`                 | Delete an expense by ID                                 |

## Bonus Feature

Implemented the optional **Search Expenses** feature by extending the existing `GET /expenses` endpoint with the `q` query parameter.

Searches:

- Are case-insensitive
- Support partial title matches
- Can be combined with the `category` filter to further narrow results

Example:

```text
GET /expenses?q=coffee
GET /expenses?category=food&q=coffee
```

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
- Automated tests use a temporary JSON file, so your real expense data is never modified.
- AI-assisted design decisions and implementation details are documented in `AI_NOTES.md`.
