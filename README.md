# Smart Expense Tracker API

A REST API built with FastAPI to manage personal expenses — add, view, filter by category, calculate totals, and delete expenses. Data is stored in memory (no database required).

## What it does

- Add an expense (title, amount, category, date)
- View all expenses
- Filter expenses by category
- Calculate totals (overall and by category)
- Delete an expense

## Requirements

- Python 3.9+

## Install dependencies

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start the server

```
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

Interactive documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`, where all endpoints can be tested directly in the browser.

## Run the tests

```
python3 -m pytest
```

This runs the test suite in `tests/test_main.py`, covering all 5 endpoints.

## Project structure

```
expense-tracker/
  main.py          # FastAPI app with all endpoints
  requirements.txt # dependencies
  tests/
    test_main.py   # test suite
  AI_NOTES.md       # AI usage notes
  README.md         # this file
```

## Endpoints

| Method | Path                              | Description                        |
|--------|------------------------------------|-------------------------------------|
| POST   | `/expenses`                        | Add a new expense                   |
| GET    | `/expenses`                        | View all expenses                   |
| GET    | `/expenses/category/{category}`    | Filter expenses by category         |
| GET    | `/expenses/total`                  | Get overall total and totals by category |
| DELETE | `/expenses/{expense_id}`           | Delete an expense by id             |
