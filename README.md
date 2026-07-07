# Viridian

Viridian is a life progression app that turns fitness, career, school, finance, scheduling, and rewards into a personal RPG-style growth system.

The current MVP is focused on the backend foundation for user accounts, authentication, and future user-specific fitness tracking.

## Current Status

Phase completed:

- FastAPI backend setup
- User registration
- Password hashing
- Login with password verification
- JWT access token creation
- Protected current-user route foundation
- In-memory fake database for early development

## Tech Stack

- Python
- FastAPI
- Pydantic
- Passlib
- bcrypt
- python-jose
- Uvicorn

## Project Structure

```text
viridian/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── auth.py
│   ├── data.py
│   └── requirements.txt
└── frontend/

