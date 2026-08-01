# AI_NOTES.md

## Project Setup

### AI Assistance

- Discussed which tech stack to use before starting. I decided to build the project using Python and FastAPI.
- AI suggested creating a simple root (`/`) endpoint first so I could verify that the project and server were set up correctly before implementing the required API.

### What I Validated or Changed

- I created the project structure, virtual environment, Git repository, and GitHub repository myself.
- After the initial setup, I started the server and verified that the Swagger UI was working before continuing.

### Suggestions I Didn't Use

- None.

---

## Models (`src/models.py`)

### AI Assistance

- AI drafted the initial Pydantic models and explained why separating `ExpenseCreate` and `Expense` was useful.

### What I Validated or Changed

- Before using the code, I asked for a walkthrough so I understood what each model was responsible for.
- I wasn't familiar with `Field(...)`, so I asked what the `...` argument meant before using it.
- I also questioned whether two models were necessary and kept the approach after understanding the benefits.

### Suggestions I Didn't Use

- AI initially suggested using UUIDs for expense IDs. I chose incrementing integer IDs because they were simpler for a JSON-file based application.
- AI also suggested using an Enum for categories, but I kept `category` as a normal string since the assignment doesn't define a fixed list of valid categories.

---

## Storage (`src/storage.py`)

### AI Assistance

- AI helped draft the initial storage layer and explained the purpose of each function.

### What I Validated or Changed

- We discussed reading the JSON file on every request versus keeping everything in memory. I chose to read from disk each time because the file is small and the JSON file remains the single source of truth.
- Before using the code, I reviewed each function to make sure it wasn't adding unnecessary complexity.
- While implementing the bonus feature, I refactored the storage layer by replacing separate `get_all()` and `get_by_category()` functions with a single `get_expenses()` function that supports optional category filtering and title searching.

### Suggestions I Didn't Use

- Considered loading all expenses into memory after startup but decided it wasn't necessary for this assignment.
- AI suggested a few optional implementation ideas, but I only kept the ones that improved clarity without increasing complexity.

---

## API Routes (`src/main.py`)

### AI Assistance

- AI helped draft the API routes and explained why each endpoint was structured the way it was.

### What I Validated or Changed

- I asked why the POST endpoint converts the Pydantic model into a dictionary before passing it to the storage layer.
- We discussed whether `storage.py` should receive the `ExpenseCreate` object directly or only plain data. I kept the current approach because it keeps the storage layer focused on data rather than request models.
- I also reviewed the response models, status codes, and query parameters to understand why each one was used.
- For the bonus feature, I extended the existing `GET /expenses` endpoint with an optional `q` query parameter instead of creating a separate search endpoint.

### Suggestions I Didn't Use

- Considered passing the `ExpenseCreate` object directly to `storage.py`, but decided against it after discussing the tradeoffs. Keeping the conversion in the route made the separation between the API layer and storage layer clearer.

---

## Tests (`tests/test_expenses.py`)

### AI Assistance

- AI helped plan the test scenarios before I started writing the test file.

### What I Validated or Changed

- Split the tests into two groups:
  - Storage-level tests for `storage.py`
  - API-level tests using FastAPI's `TestClient`
- Learned how pytest fixtures work to isolate tests by redirecting the storage path to a temporary JSON file.
- After refactoring for the bonus feature, I reran the existing tests first to confirm the behavior hadn't changed before adding new search tests.
- Added five additional tests covering the search functionality, including case-insensitive search, partial matches, no-match scenarios, and combined category + search filtering.

### Suggestions I Didn't Use

- Initially wrote a test for ID reuse after deleting all expenses. After reviewing it, I removed the test because the assignment doesn't specify that behavior and I wanted the test suite to focus on the required functionality rather than implementation details.

---

## Bonus Feature

### AI Assistance

- AI suggested several bonus feature options and explained the tradeoffs between them.

### What I Validated or Changed

- I chose to implement the optional search feature because it fit naturally with the existing API.
- Instead of adding a new endpoint, I extended the existing `GET /expenses` endpoint with an optional `q` query parameter so search and category filtering could be combined.

### Suggestions I Didn't Use

- Considered implementing sorting as a bonus feature, but chose not to because it wasn't one of the options listed in the assignment.
- Also considered Docker and monthly summaries, but decided that search provided the most value while keeping the implementation simple and consistent with the existing design.
