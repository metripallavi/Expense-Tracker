# Expense Tracker

A minimal full-stack Expense Tracker built with FastAPI, Jinja templates, vanilla JavaScript, and SQLite.

---

## Live Demo

https://expense-tracker-8vix.onrender.com

---

## Repository

https://github.com/metripallavi/Expense-Tracker

---

## Features

- Create a new expense with amount, category, description, and date
- View a list of expenses
- Filter expenses by category
- Sort expenses by date (newest first)
- View the total amount of currently visible expenses
- Retry-safe expense creation using an idempotency key

---

## Tech Stack

- FastAPI  
- SQLAlchemy  
- SQLite  
- Jinja2  
- Vanilla JavaScript  
- Pytest  

---

## Run Locally

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate


2. Install dependencies
pip install -r requirements.txt

3. Run the app
uvicorn app.main:app --reload

4. Open in browser
http://127.0.0.1:8000/

Run Tests
PYTHONPATH=. pytest

API Documentation

Once the server is running locally:

http://127.0.0.1:8000/docs
API Endpoints
POST /expenses

Creates a new expense.

Headers
Idempotency-Key: <unique-value>
Request Body
{
  "amount": "100.50",
  "category": "Food",
  "description": "Lunch",
  "date": "2025-04-01"
}
GET /expenses

Optional query parameters:

category
sort=date_desc
Persistence Choice

SQLite was chosen because it is lightweight, requires no setup, and is suitable for a small full-stack application.

Design Decisions
Single FastAPI app for both API and frontend to keep the architecture simple
SQLite for persistence
Idempotency key support to safely handle retries
Server-rendered UI using Jinja templates
Trade-offs
No authentication
No pagination
Only one sort mode implemented (date_desc)
Basic UI styling
Future Improvements
Edit/Delete expenses
Pagination
Category analytics
Authentication
Better UI/UX
Production-grade database (PostgreSQL)


## Contact
Author : Pallavi Metri 
GitHub: https://github.com/metripallavi