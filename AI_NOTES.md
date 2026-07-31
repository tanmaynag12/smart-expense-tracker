# AI_NOTES.md

## Project Setup

### AI Assistance
- Discussed which tech stack to use before starting. I decided to go with Python and FastAPI.
- AI suggested creating a simple root (`/`) endpoint first so I could check that the project and server were set up correctly before writing the actual API.

### What I Validated or Changed
- I created the project structure, virtual environment, Git repository and GitHub repository myself.
- After the setup was done, I ran the server and checked the Swagger UI to make sure everything was working before moving on.

### Suggestions I Didn't Use
- None.

---

## Models (`src/models.py`)

### AI Assistance
- AI drafted the initial models and explained why it separated `ExpenseCreate` and `Expense`.

### What I Validated or Changed
- Before using the code, I asked for a walkthrough so I understood what each part was doing instead of just copying it.
- I wasn't familiar with `Field(...)`, so I asked what the `...` meant before using it.
- I also checked whether using two models was actually necessary and kept that approach after understanding why.

### Suggestions I Didn't Use
- AI first suggested using UUIDs for the expense ID. After discussing the tradeoffs, I decided to use incrementing integer IDs since they felt simpler for a JSON-file project.
- AI also mentioned using an Enum for categories, but I left `category` as a normal string because the assignment doesn't define a fixed list of categories.

---

## Storage (`src/storage.py`)

### AI Assistance
- AI drafted the first version of the storage layer and explained what each function was responsible for.

### What I Validated or Changed
- We discussed reading the JSON file on every request versus loading everything into memory once. I chose to read it on every request because the file is small and it keeps the JSON file as the single source of truth.
- Before using the code, I asked if any part of it was unnecessary or overkill for this assignment. Most of the structure stayed the same because each function had a clear purpose.

### Suggestions I Didn't Use
- Considered keeping all expenses in memory after startup, but decided against it since it wasn't really needed for this assignment.
- AI pointed out a couple of optional implementation details. I only kept the ones that made the code a little safer or easier to understand without adding unnecessary complexity.