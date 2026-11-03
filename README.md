# BorjStay 2.0 - Hotel Operations System

A portfolio-grade, local-first hotel management application. The interface was deliberately designed to feel calm and human rather than like a generic admin template.

## Product scope
- Operational dashboard with occupancy, movement, revenue and activity trail
- Guest directory with protected reservation history
- Room inventory, nightly pricing, capacity and maintenance status
- Reservation workflow with date-overlap prevention and capacity validation
- Check-in and check-out actions
- Payment recording and outstanding balance tracking
- Reports by status and booking source
- CSV export
- REST API documentation at `/docs`
- Responsive interface and fictional seed data

## Architecture
- `main.py`: FastAPI routes, business rules and SQLAlchemy models
- `static/app.js`: page controllers, API client and UI state
- `static/style.css`: responsive design system
- `static/index.html`: application shell
- `borjstay.db`: local SQLite database, generated on first run

## Run
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```
Open `http://127.0.0.1:8000`.

## Reset demo data
Stop the server, delete `borjstay.db`, then start the server again.

## Maintenance rules used
- One source of truth for business rules in the API
- No real hotel or guest data in the public demo
- Room overlap is blocked at the backend, not only in the interface
- Records with reservation history are protected from accidental deletion
- Room capacity and maintenance state are validated before booking

## Portfolio description
Designed and developed BorjStay, a local-first hotel operations system using Python, FastAPI, SQLAlchemy, SQLite and vanilla JavaScript. The product manages guests, rooms, reservations, check-in and check-out workflows, payments, reporting and CSV exports. I implemented backend validation for room availability, date conflicts, capacity limits and financial balances, then created a responsive interface focused on clarity for front-desk staff.
