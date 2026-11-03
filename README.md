# Stay Borj - Hotel Operations Management Demo

Stay Borj is an independent, local-first hotel operations management demo developed for portfolio and educational purposes.

The application demonstrates how a hotel team can manage guests, rooms, reservations, check-in and check-out operations, payments, and reports through a clear and responsive interface.

> **Important:** This repository is an independently developed portfolio demonstration. It does not contain the original source code, database, private design, confidential business logic, or customer information of any software previously delivered to a client. All displayed data is fictional.

## Project Background

The idea for Stay Borj was informed by practical experience understanding real business and hotel management workflows.

This public version was designed and developed independently from scratch to demonstrate my software engineering skills without exposing client-owned source code, confidential systems, private databases, employee information, or customer data.

## Main Features

- Operational dashboard with occupancy and revenue indicators
- Guest profile management
- Room inventory, pricing, capacity, floor, and status tracking
- Reservation creation and management
- Reservation date-conflict prevention
- Room capacity and maintenance validation
- Check-in and check-out workflows
- Payment recording and outstanding balance calculation
- Reservation status and booking source tracking
- Recent activity history
- Operational reports
- CSV reservation export
- REST API documentation at `/docs`
- Responsive interface for desktop and mobile
- Fictional demonstration records

## Business Rules

- Check-out must be after check-in.
- A room cannot be reserved for overlapping dates.
- A room under maintenance cannot accept reservations.
- Guest count cannot exceed room capacity.
- A payment cannot exceed the remaining balance.
- Guests linked to reservation history are protected from accidental deletion.
- Check-in and check-out actions update the room status.

These rules are enforced by the backend API, not only by the interface.

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- REST API

### Frontend

- HTML5
- CSS3
- JavaScript
- Responsive Web Design

### Development Tools

- Git
- GitHub
- GitHub Desktop
- Visual Studio Code

## Project Structure

```text
stay-borj-hotel-demo/
|-- main.py
|-- requirements.txt
|-- README.md
|-- .gitignore
`-- static/
    |-- index.html
    |-- style.css
    `-- app.js
```

## Run Locally

```powershell
git clone https://github.com/medoussema2007/stay-borj-hotel-demo.git
cd stay-borj-hotel-demo
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open the application at `http://127.0.0.1:8000`.

Open the API documentation at `http://127.0.0.1:8000/docs`.

## Reset Demo Data

Stop the server with `Ctrl + C`, delete `borjstay.db`, and start the server again. A new local database with fictional demonstration records will be generated automatically.

## Privacy and Confidentiality

This repository does not include:

- Real customer or employee information
- Private hotel records or production databases
- Passwords, credentials, or API keys
- Client-owned source code
- Original commercial designs
- Confidential business rules
- Camera-monitoring functionality
- Private organization workflows

## Public Demo Scope

Stay Borj is a portfolio demonstration, not a production-ready property management system. A production deployment would require secure authentication, password hashing, role-based access control, database migrations, automated backups, PostgreSQL, HTTPS, automated tests, monitoring, audit logs, and documented recovery procedures.

## Development Note

AI-assisted tools were used for brainstorming, debugging, documentation support, and code review. The application structure, feature selection, interface customization, business rules, testing decisions, and final implementation were reviewed and managed by the developer.

## Developer

**Mohamed Oussema Marzougui**

Software Developer focused on full-stack applications, business software, Python backend development, REST APIs, SQL databases, AI integration, and workflow automation.

## License

No license is currently provided. The source code is publicly visible for portfolio review and educational evaluation. Public visibility does not grant permission to copy, redistribute, sell, or reuse the complete project as a commercial product.
