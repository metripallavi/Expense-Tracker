# Expense Tracker

A minimal full-stack Expense Tracker built with FastAPI, Jinja templates, vanilla JavaScript, and SQLite.

## Features

- Create a new expense with amount, category, description, and date
- View a list of expenses
- Filter expenses by category
- Sort expenses by date (newest first)
- View the total amount of currently visible expenses
- Retry-safe expense creation using an idempotency key

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- Vanilla JavaScript
- Pytest

## Run Locally

1. Create and activate a virtual environment
2. Install dependencies

```bash
pip install -r requirements.txt