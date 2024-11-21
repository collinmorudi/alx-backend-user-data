Markdown
# User Authentication Service

This project implements a basic user authentication service with Flask and SQLAlchemy.

## Features

* User registration and login
* Password hashing with bcrypt
* Session management with UUIDs
* Password reset functionality
* API endpoints for user management

## Requirements

* Python 3.7
* Flask
* SQLAlchemy 1.3.x
* bcrypt

## Setup

1. Clone the repository: `git clone https://github.com/your-username/alx-backend-user-data.git`
2. Install dependencies: `pip3 install -r requirements.txt`
3. Create the database: `python3 db.py`
4. Run the Flask app: `python3 app.py`

## API Endpoints

* **POST /users:** Register a new user
* **POST /sessions:** Log in a user
* **DELETE /sessions:** Log out a user
* **GET /profile:** Get user profile
* **POST /reset_password:** Generate a password reset token
* **PUT /reset_password:** Update user password
