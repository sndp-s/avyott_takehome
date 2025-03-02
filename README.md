> **Note:** This assignment is incomplete. Only the Books API is implemented with search/filter features pending.

# Library API
Take-home assignment for [Avyott](https://www.avyott.com/a), detailed [here](https://docs.google.com/document/d/1j63SoZPrucUFlJExgtPX7SfLqkLZvUTUDG_d-WvHYG8/edit?usp=gmail).

## Tech Stack
- **Python**
- **FastAPI**
- **Pydantic**
- **PostgreSQL**

## How to Run
1. Clone this repo (backend app dir: `repo/app`)
2. Create a Python virtual environment
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL and create a database
5. Apply `schemas.sql` to the database
6. Rename `sample.env` to `.env` and update values as needed
7. Run the app:
   ```sh
   uvicorn app.main:app --reload
   ```
8. Open API docs in your browser at: [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## VS Code Debug Config
```json
{
  "configurations": [
    {
      "name": "Library API",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload"
      ],
      "jinja": true
    }
  ]
}
```
