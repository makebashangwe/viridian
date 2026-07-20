# Viridian

Viridian is a calm personal life system for recording lightweight check-ins, recognizing meaningful patterns, and supporting intentional growth without turning everyday life into a constant optimization exercise.

The project uses game-inspired structures—activities, sessions, goals, XP, and personal rewards—but its purpose is not to pressure users into maintaining streaks or maximizing every metric.

Viridian is designed around a simpler rhythm:

> Live your life. Record a small signal. Return later to understand the pattern.

---

## Project Status

**Completed:** Phase 7 — Backend stabilization, automated testing, and database migrations  
**Current milestone:** Phase 8 — Frontend foundation and API integration

The backend MVP is complete and currently includes:

- PostgreSQL persistence
- SQLAlchemy ORM models and relationships
- FastAPI domain routers
- Pydantic request and response schemas
- JWT authentication
- service-layer business logic
- Alembic database migrations
- 77 passing automated tests

Runtime table creation has been removed from the FastAPI application. Database schema changes are now managed through Alembic migrations.

---

## Product Philosophy

Viridian is not intended to become an obsessive productivity tracker or a universal score for a person's value.

Its design principles are:

- **Lightweight check-ins:** Recording an experience should take less attention than living it.
- **Reflection over surveillance:** Viridian stores deliberate signals rather than constantly monitoring users.
- **Meaningful review:** Patterns become useful when reviewed later, not when every moment is interrupted by feedback.
- **User-defined value:** Users decide which activities, goals, and rewards matter to them.
- **Calm motivation:** Progress systems should encourage awareness without creating guilt, pressure, or dependency.
- **Privacy-conscious design:** Viridian should collect only the information necessary to serve its purpose.

---

## Current Architecture

Viridian is currently implemented as a modular monolith.

```text
Client
  |
  v
FastAPI application
  |
  +-- Authentication and authorization
  |
  +-- Domain routers
  |     +-- auth
  |     +-- activities
  |     +-- sessions
  |     +-- xp
  |     +-- goals
  |     +-- rewards
  |
  +-- Shared services
  |     +-- goal progress calculation
  |     +-- reward balance calculation
  |
  +-- Pydantic schemas
  |
  +-- SQLAlchemy ORM models
  |
  +-- PostgreSQL
```

This structure keeps the system understandable and maintainable while the product model is still evolving. Distributed services or more complex infrastructure will only be introduced when there is a demonstrated operational need.

---

## Repository Structure

```text
viridian/
├── alembic.ini
├── requirements.txt
├── .env.example
├── README.md
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── db_models.py
│   ├── schemas.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth_route.py
│   │   ├── activities.py
│   │   ├── sessions.py
│   │   ├── xp.py
│   │   ├── goals.py
│   │   └── rewards.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── goal_service.py
│   │   └── reward_service.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_activities.py
│   │   ├── test_sessions.py
│   │   ├── test_xp.py
│   │   ├── test_goals.py
│   │   └── test_rewards.py
│   │
│   └── alembic/
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
│           └── 1773ad942e12_initial_schema.py
│
└── docs/
    ├── dev-journal/
    └── drafts/
```

---

## Implemented Features

### Authentication and User Access

- User registration
- Duplicate email protection
- Duplicate username protection
- Secure password hashing
- Email and password login
- JWT bearer authentication
- OAuth2-compatible token route
- Protected current-user endpoint
- User-owned resource filtering
- Cross-user access protection

### Activity Rules

Users define how an activity should be evaluated.

Supported operations include:

- Create an activity rule
- List active activity rules
- Retrieve an activity rule by ID
- Partially update an activity rule
- Archive an activity rule
- Restore an archived activity rule
- Prevent archived activities from receiving new sessions

Activity rules can configure:

- difficulty rank
- legal minimum duration
- legal completion points
- primary goal duration
- primary goal points
- bonus interval duration
- bonus points
- maximum session duration
- default location

Viridian does not decide that one type of activity is inherently more valuable than another.

### Activity Sessions

- Record an activity session
- Validate activity ownership
- Reject sessions for missing or archived activities
- Reject sessions exceeding the configured maximum duration
- Store activity-name snapshots
- Store scoring-result snapshots
- List sessions
- Retrieve a session by ID
- Delete an incorrect session

Session scoring includes:

- legal-goal completion
- main-goal completion
- bonus intervals
- total XP earned

Historical sessions preserve their original scoring results even when an activity rule is edited later.

### XP and Progress Summaries

- Total XP
- Total session count
- Legal-goal completion count
- Main-goal completion count
- Bonus-interval count
- XP grouped by activity
- XP for a specific activity rule
- XP for a specific session

XP is a reflective summary of completed actions. It is not intended to measure a user's worth, discipline, health, or productivity.

### Goals

- Create global goals
- Create activity-specific goals
- List goals
- Retrieve a goal by ID
- Delete goals
- Calculate progress for all goals
- Calculate progress for an individual goal
- Mark goals complete when targets are reached
- Award reward points for completed goals
- Prevent another user's activity from being assigned to a goal

Supported goal targets include:

- total XP
- total sessions
- completed legal goals
- completed main goals
- bonus intervals

Goal progress is derived from recorded sessions rather than requiring users to maintain duplicate information manually.

### Rewards

- Create personal rewards
- Create rewards tied to required goals
- List rewards
- Retrieve a reward by ID
- View earned reward points
- View spent reward points
- View available reward balance
- Redeem rewards
- Prevent redemption when balance is insufficient
- Lock rewards behind goal completion
- Archive rewards
- Preserve redemption history after reward removal

Reward redemptions store immutable snapshots of:

- reward name
- point cost
- redemption timestamp

Rewards are chosen by the user. Viridian provides a structure for intentional celebration rather than prescribing what a good reward should be.

---

## Database and Migration Management

Viridian uses:

- PostgreSQL
- SQLAlchemy 2
- Alembic

The application does not create tables automatically at startup.

Schema creation and changes are managed through migrations:

```bash
py -m alembic upgrade head
```

The initial migration creates:

```text
users
activity_rules
sessions
goals
rewards
reward_redemptions
rewards_archive
```

To inspect the current database revision:

```bash
py -m alembic current
```

To view migration history:

```bash
py -m alembic history
```

To verify that ORM models and the database schema remain synchronized:

```bash
py -m alembic check
```

Expected result:

```text
No new upgrade operations detected.
```

---

## Automated Testing

Viridian currently has **77 passing backend tests**.

Tested areas include:

- registration and login
- JWT authentication
- OAuth2 token behavior
- request validation
- activity CRUD behavior
- activity archive and restore behavior
- session creation and scoring
- scoring thresholds and bonus intervals
- XP aggregation
- goal creation and progress
- activity-specific goal filtering
- reward creation and balance calculation
- locked reward behavior
- reward redemption
- reward archiving
- missing-resource responses
- cross-user ownership protection

Run the complete test suite:

```bash
py -m pytest ./backend/tests -v
```

Run the concise version:

```bash
py -m pytest ./backend/tests -q
```

Expected result:

```text
77 passed
```

The test suite uses a separate PostgreSQL database configured through `TEST_DATABASE_URL`.

---

## Local Development Setup

### Prerequisites

Install:

- Python 3.12 or newer
- PostgreSQL or Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone https://github.com/makebashangwe/viridian.git
cd viridian
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` into a new `.env` file.

```env
DATABASE_URL=postgresql://viridian_user:replace_me@localhost:5432/viridian
TEST_DATABASE_URL=postgresql://viridian_user:replace_me@localhost:5432/viridian_test

JWT_SECRET_KEY=replace_with_a_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Do not commit the real `.env` file.

### 5. Create the databases

Create two PostgreSQL databases:

```text
viridian
viridian_test
```

The first is used for local development. The second is reserved for automated testing.

### 6. Apply database migrations

```bash
py -m alembic upgrade head
```

### 7. Start the API

From the repository root:

```bash
py -m uvicorn backend.main:app --reload
```

Depending on your local import configuration, you may instead run from the backend directory:

```bash
cd backend
py -m uvicorn main:app --reload
```

### 8. Open the API documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

---

## Environment Variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Development PostgreSQL connection |
| `TEST_DATABASE_URL` | Automated test PostgreSQL connection |
| `JWT_SECRET_KEY` | Secret used to sign authentication tokens |
| `JWT_ALGORITHM` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime |

Production credentials should be supplied through a managed secret store rather than committed files.

---

## API Domains

The current backend exposes routes under:

```text
/auth
/activities
/sessions
/xp
/goals
/rewards
```

Interactive endpoint details are available through Swagger UI while the application is running.

---

## Current Limitations

The current release is backend-focused.

Not yet implemented:

- production frontend
- mobile application
- production deployment
- CI/CD pipeline
- account deletion
- user data export
- production monitoring
- production backup and recovery workflow
- advanced accessibility testing
- AI-assisted reflection
- Vivarium Lens integration

Known technical-debt items include:

- replacing timezone-naive `datetime.utcnow()` defaults
- resolving the current TestClient dependency deprecation warning
- reviewing redundant indexes on primary-key columns
- adding transaction rollback handling for unexpected database failures
- defining deletion policy for goals referenced by rewards

---

## Roadmap

### Phase 8 — Frontend Foundation and API Integration

Planned work:

- Configure environment-based CORS
- Create the frontend application shell
- Establish a centralized API client
- Connect registration, login, logout, and current-user access
- Build the lightweight check-in workflow
- Add recent-session review
- Add calm progress summaries
- Add activity, goal, and reward management
- Establish responsive and accessible UI foundations
- Keep advanced analytics secondary

The first frontend experience should support:

```text
log in
→ choose an activity
→ record a lightweight check-in
→ receive a calm confirmation
→ return to life
```

### Phase 9 — Deployment and Real-World Hardening

Planned work:

- Containerize application components
- Configure production environments
- Deploy PostgreSQL
- Deploy the FastAPI backend
- Deploy the frontend
- Configure HTTPS and domains
- Add CI/CD
- Add structured logging
- Add health checks
- Add error monitoring
- Establish backup and restore procedures
- Add privacy and data-management foundations
- Run a small private beta

### Future Direction

Potential later work includes:

- user-controlled weekly and monthly reviews
- reflection capture
- accessibility refinement
- carefully scoped AI-assisted pattern interpretation
- mobile packaging
- integration with Vivarium Lens and Brilliant Halo glasses

AI features should summarize and support deliberate reflection rather than constantly judge, interrupt, or optimize the user.

---

## Companion Project: Vivarium Lens

Vivarium Lens is a planned wearable client for Viridian using Brilliant Halo glasses.

The Lens will act as another interface to the same Viridian backend rather than duplicating its business logic.

```text
Viridian web client
Viridian mobile client
Vivarium Lens
        |
        v
Viridian API
        |
        v
PostgreSQL
```

Initial Lens goals include:

- quick activity check-ins
- glanceable progress retrieval
- short reflection capture
- intentional voice or button-driven commands
- privacy-conscious wearable interactions

The wearable experience will preserve the same philosophy:

> Record what matters quickly, then return attention to real life.

---

## Engineering Priorities

Technical decisions are evaluated against:

1. usability
2. privacy
3. accessibility
4. automation
5. maintainability
6. operational reliability

Viridian intentionally avoids unnecessary architectural complexity. New infrastructure should solve demonstrated problems rather than exist only to make the system appear more sophisticated.

---

## License

A license has not yet been selected.

Until a license is added, the source code remains publicly viewable but is not automatically granted an open-source usage license.

---

## Author

Created by **Makeba Shangwe** as a full-stack software engineering project exploring calm technology, backend architecture, wearable interfaces, and privacy-conscious personal software.