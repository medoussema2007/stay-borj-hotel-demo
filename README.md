Stay Borj - Hotel Operations Management Demo
Stay Borj is an independent, local-first hotel operations management demo developed for portfolio and educational purposes.

The application demonstrates how a hotel team can manage guests, rooms, reservations, check-in and check-out operations, payments, and reports through a clear and responsive interface.

Important: This repository is an independently developed portfolio demonstration. It does not contain the original source code, database, private design, confidential business logic, or customer information of any software previously delivered to a client. All displayed data is fictional.

Project Background
The idea for Stay Borj was informed by practical experience understanding real business and hotel management workflows.

This public version was designed and developed independently from scratch to demonstrate my software engineering skills without exposing any client-owned source code, confidential system, private database, employee information, or customer data.

Main Features
Operational dashboard with occupancy and revenue indicators
Guest profile management
Room inventory management
Room type, capacity, floor, price, and status tracking
Reservation creation and management
Reservation date conflict prevention
Room capacity validation
Maintenance room validation
Check-in and check-out workflow
Payment recording
Outstanding balance calculation
Reservation status tracking
Booking source tracking
Recent activity history
Reports by reservation status
Reports by booking source
CSV reservation export
REST API documentation
Responsive interface for desktop and mobile
Fictional demonstration records
Business Rules
The application includes backend validation for important hotel operations:

A reservation check-out date must be after the check-in date.
A room cannot be reserved for overlapping dates.
A room under maintenance cannot accept new reservations.
The number of guests cannot exceed the room capacity.
A payment cannot exceed the remaining reservation balance.
Guest records linked to reservation history are protected from accidental deletion.
Check-in and check-out actions automatically update the operational status.
These rules are enforced by the backend API and not only by the user interface.

Technology Stack
Backend
Python
FastAPI
SQLAlchemy
Pydantic
SQLite
REST API
Frontend
HTML5
CSS3
JavaScript
Responsive Web Design
Development Tools
Git
GitHub
GitHub Desktop
Visual Studio Code
Architecture
The project follows a simple and maintainable structure:

stay-borj-hotel-demo/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── static/
    ├── index.html
    ├── style.css
    └── app.js
