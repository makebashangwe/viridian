# Viridian

Viridian is a life progression app that turns fitness, career, school, finance, scheduling, and rewards into a personal RPG-style growth system.

The current MVP is focused on the backend foundation for user accounts, authentication, and future user-specific fitness tracking.

## Current MVP Features:
- User registration and login
- Password hashing
- JWT protected routes
- User-owned activity rules
- Fitness session logging
- XP calculation
- XP summaries
- Goal creation and progress tracking
- Reward point summaries
- Reward creation and redemption
- In-memory fake database for learning/testing

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
│   ├── Notes/
│   ├── main.py
│   ├── models.py
│   ├── auth.py
│   ├── data.py
│   └── requirements.txt

└── frontend/

