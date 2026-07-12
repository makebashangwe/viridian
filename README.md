# Viridian

Viridian is a calm personal life system for recording lightweight check-ins, recognizing meaningful patterns, and supporting intentional growth without turning everyday life into a constant optimization exercise.

The project uses game-inspired structure—activities, sessions, goals, XP, and personal rewards—but its purpose is not to pressure users into maintaining streaks or maximizing every metric. Viridian is designed around a simpler rhythm:

> Live your life. Record a small signal. Return later to understand the pattern.

## Project Status

**Current milestone:** Phase 7B — API contract and backend stabilization  
**Recently completed:** Phase 7A — PostgreSQL persistence and router/service refactor

The backend MVP now uses a persistent relational database for its primary domains and is organized into focused FastAPI routers rather than one large application file.

## Current Backend Architecture

```text
Client / Swagger UI
        |
        v
FastAPI application
        |
        +-- Authentication dependency
        |
        +-- Domain routers
        |     +-- auth
        |     +-- activities
        |     +-- sessions
        |     +-- xp
        |     +-- goals
        |     +-- rewards
        |
        +-- Shared service functions
        |     +-- goal progress calculation
        |     +-- reward balance calculation
        |
        +-- Pydantic request/response schemas
        |
        +-- SQLAlchemy ORM models
        |
        +-- PostgreSQL
```

### Backend Responsibilities

- **`main.py`** creates the FastAPI application, initializes the current database tables, and registers domain routers.
- **`routers/`** contains HTTP-facing endpoint logic grouped by feature.
- **`services.py`** contains shared business operations used by more than one router.
- **`schemas.py`** defines Pydantic request and response contracts.
- **`db_models.py`** defines SQLAlchemy ORM entities and relationships.
- **`database.py`** configures the SQLAlchemy engine, session factory, and request-scoped database dependency.
- **`auth.py`** handles password hashing, JWT creation, and current-user resolution.

The application is currently a modular monolith. This keeps the system understandable and maintainable while the product model is still evolving. Separate services or distributed infrastructure will only be introduced when the product has a real operational need for them.

## Implemented Features

### Authentication and User Access

- User registration
- Duplicate email and username protection
- Password hashing
- Email/password login
- JWT bearer authentication
- OAuth2-compatible token route for Swagger authorization
- Protected current-user access
- User-owned resource filtering

### Activity Rules

Users can define how a meaningful activity should be evaluated.

Implemented behavior includes:

- Create an activity rule
- List active activity rules
- Retrieve an activity rule by ID
- Partially update an activity rule
- Archive an activity rule
- Configure:
  - legal minimum duration
  - primary goal duration
  - maximum session duration
  - base points
  - goal points
  - bonus intervals
  - bonus points

Activity rules are intentionally user-defined. Viridian does not decide that one kind of life activity is inherently more valuable than another.

### Activity Sessions

- Record an activity session
- Validate that the referenced activity belongs to the authenticated user
- Prevent sessions that exceed the configured maximum duration
- Calculate:
  - legal-goal completion
  - main-goal completion
  - bonus intervals
  - total XP earned
- Store an activity-name snapshot with the session
- List a user’s sessions
- Retrieve a session by ID
- Remove or archive sessions according to the current route behavior

### XP and Progress Summaries

- Total XP summary
- Total session count
- Legal-goal completion count
- Main-goal completion count
- Bonus-interval count
- XP grouped by activity
- XP for a specific activity rule
- XP for a specific session

XP is used as a reflective summary of completed actions. It is not intended to become a universal score for the user’s worth, discipline, health, or productivity.

### Goals

- Create goals
- List goals
- Retrieve a goal by ID
- Calculate progress for all goals
- Calculate progress for an individual goal
- Mark goals complete when their target is reached
- Award reward points for completed goals
- Delete or archive goals according to the current route behavior
- Support goal targets based on metrics such as:
  - total XP
  - total sessions
  - completed main goals
  - activity-specific progress

Goal progress is derived from recorded sessions rather than requiring the user to manually maintain multiple copies of the same information.

### Rewards

- Create personal rewards
- List rewards
- Retrieve rewards by ID
- View earned, spent, and available reward-point balances
- Redeem a reward
- Record reward-redemption history
- Lock a reward behind a required goal
- Validate that locked rewards reference a real user-owned goal
- Prevent redemption when:
  - the user lacks enough points
  - the required goal is incomplete
- Archive rewards while preserving historical information

Rewards are chosen by the user. Viridian provides structure for intentional celebration rather than prescribing what a “good” reward should be.

## Persistence Model

The active backend uses PostgreSQL through SQLAlchemy.

Current persisted domains include:

- users
- activity rules
- activity sessions
- goals
- rewards
- reward redemptions
- archived reward records

The application now uses database-backed information for XP summaries, goal progress, reward balances, and redemption checks. This removes the earlier split between PostgreSQL records and process-local Python lists.

## API Organization

The backend is separated into domain routers:

```text
backend/
├── main.py
├── auth.py
├── database.py
├── db_models.py
├── schemas.py
├── services.py
├── requirements.txt
└── routers/
    ├── __init__.py
    ├── auth.py
    ├── activities.py
    ├── sessions.py
    ├── xp.py
    ├── goals.py
    └── rewards.py
```

Shared calculations that affect multiple domains are being moved into the service layer. Examples include updating goal progress and calculating a user’s available reward balance.

This refactor reduces duplication and keeps route handlers focused on:

1. accepting and validating HTTP input,
2. resolving the authenticated user,
3. calling business or persistence logic,
4. returning a stable API response.

## Local Development Setup

### Prerequisites

Install:

- Python 3.12 or newer
- Docker Desktop or another Docker-compatible runtime
- Git

### 1. Clone the repository

```bash
git clone https://github.com/makebashangwe/viridian.git
cd viridian
```

### 2. Create and activate a virtual environment

From the repository root:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

The current Compose configuration starts the local PostgreSQL service and preserves its data in a named Docker volume.

### 5. Configure environment variables

Create a `.env` file for local development.

Example:

```env
DATABASE_URL=postgresql://viridian:viridian@localhost:5432/viridian
SECRET_KEY=replace-with-a-local-development-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use values that match the current `docker-compose.yml`.

Do not commit `.env` or reuse local-development credentials in a deployed environment.

### 6. Run the API

From the repository root:

```bash
uvicorn backend.main:app --reload
```

Depending on the active import configuration, the backend can also be launched from inside the `backend` directory:

```bash
uvicorn main:app --reload
```

The repository is being standardized around the root-level command so module imports behave consistently.

### 7. Open the API documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health route: `http://127.0.0.1:8000/`

### 8. Stop the local database

```bash
docker compose down
```

To also remove the local database volume:

```bash
docker compose down -v
```

The second command permanently removes locally stored Viridian development data.

## Manual API Test Coverage

The current backend has been exercised through FastAPI’s Swagger UI.

### Authentication

- Register a new user
- Reject duplicate email addresses
- Reject duplicate usernames
- Log in with valid credentials
- Reject invalid credentials
- Generate an OAuth2 bearer token through `/auth/token`
- Authorize protected routes through Swagger
- Retrieve the authenticated user

### Activity Rules

- Create an activity rule
- List user-owned active rules
- Retrieve a rule by ID
- Update selected fields
- Archive a rule
- Reject access to missing or non-owned rules

### Sessions and Scoring

- Create sessions below, at, and above configured thresholds
- Calculate legal-goal points
- Calculate main-goal points
- Calculate bonus intervals
- Reject sessions above the configured maximum
- List sessions
- Retrieve individual sessions
- Verify session ownership boundaries

### XP

- Calculate total XP and session counts
- Count legal and main goal completions
- Count bonus intervals
- Group XP by activity
- Retrieve XP for one activity
- Retrieve XP for one session

### Goals

- Create supported goal types
- Retrieve all goals and individual goals
- Calculate live progress from stored sessions
- Mark completed goals
- Return incomplete goals without falsely completing them
- Return `404` for missing goals
- Verify activity-specific progress

### Rewards

- Create unlocked rewards
- Create goal-locked rewards
- Reject locked rewards without a required goal
- Reject references to missing or non-owned goals
- Calculate earned, spent, and available reward points
- Reject unaffordable redemptions
- Reject redemptions for incomplete locked goals
- Record successful redemptions
- Archive rewards while preserving a historical snapshot

Manual testing confirms the intended MVP behavior, but it does not replace an automated regression suite.

## Phase 7 Milestones

### Phase 7A — Persistent Domain Model and Structural Refactor

**Status: Complete**

Completed work:

- Replaced the original in-memory persistence path with PostgreSQL-backed domain records
- Added SQLAlchemy models for the core MVP domains
- Added user ownership fields and database relationships
- Migrated XP calculations to database sessions
- Migrated goal progress to database queries
- Migrated reward balances and redemptions to persisted records
- Added archive behavior for selected records
- Renamed and expanded Pydantic schema definitions
- Split the original large `main.py` into domain-specific routers
- Registered routers through the FastAPI application entry point
- Extracted shared goal and reward calculations into service functions
- Re-tested core API flows through Swagger

### Phase 7B — API Contracts and Backend Stabilization

**Status: In progress**

Current work:

- Complete response models for every endpoint
- Apply explicit response models to remaining routes
- Normalize status codes and response shapes
- Improve validation for:
  - positive durations and point values
  - ordered activity thresholds
  - nonzero bonus intervals
  - supported goal target types
  - valid reward costs
- Standardize package imports so the API launches reliably from the repository root
- Remove unused imports and legacy references
- Verify router prefixes, path parameters, and route ordering
- Keep route handlers thin by moving reusable calculations into services
- Review archive and deletion semantics for historical safety
- Add an `.env.example`
- Move JWT configuration fully into environment-backed settings
- Document all local commands and API behavior

The goal of Phase 7B is not to add more product surface area. It is to make the completed backend behavior predictable, readable, and safe to build on.

### Phase 7C — Migrations, Automated Tests, and Deployment Readiness

**Status: Remaining**

Planned tasks:

- Add Alembic
- Create a baseline database migration
- Replace normal startup-time `Base.metadata.create_all()` usage
- Add automated tests with `pytest`
- Configure FastAPI dependency overrides for test databases
- Test authentication and user isolation
- Test activity scoring boundaries
- Test goal completion behavior
- Test reward accounting and redemption rules
- Add regression tests for archive behavior
- Add database constraint tests
- Add a backend Dockerfile
- Expand Docker Compose to run both the API and PostgreSQL
- Add service health checks and dependency ordering
- Add structured configuration management
- Remove tracked generated files such as `__pycache__`
- Add linting and formatting configuration
- Add a basic GitHub Actions workflow
- Run tests automatically on pushes and pull requests
- Confirm database persistence across container restarts
- Perform a final Phase 7 end-to-end verification

Phase 7 is complete when a new developer can clone the repository, configure the environment, run migrations, start the stack, execute the automated tests, and reproduce the documented behavior without relying on hidden local state.

## Design Principles

Viridian’s technical decisions are evaluated against five long-term concerns.

### Calm usability

The system should require only enough input to preserve meaning. It should not punish missed days, manufacture urgency, or make users feel watched by their own data.

### Privacy

Personal check-ins can reveal routines, health patterns, relationships, locations, and emotional context. Data collection should remain intentional, transparent, minimal, and user-controlled.

### Accessibility

The future interface should support keyboard navigation, screen readers, reduced motion, readable contrast, flexible text sizing, and low-cognitive-load interactions.

### Automation with consent

Viridian may eventually import signals or generate summaries, but automation should reduce effort without silently deciding what matters to the user.

### Maintainability

The project favors clear domain boundaries, ordinary technologies, explicit data models, and incremental evolution over premature complexity.

## Technology Stack

### Current

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- JWT bearer authentication
- Passlib/password hashing
- Docker Compose
- Swagger/OpenAPI

### Planned

- Alembic
- Pytest
- Backend containerization
- GitHub Actions
- Responsive web frontend
- Privacy-aware review and insight features

## Product Direction

The backend currently models activities, sessions, XP, goals, and rewards because they provide a useful foundation for testing user-owned data, derived progress, and personal feedback loops.

The longer-term product will emphasize:

- quick check-ins
- optional context
- weekly and monthly reflection
- user-controlled patterns and summaries
- accessible visual progress
- gentle celebration
- clear privacy controls
- fewer notifications, not more

Viridian should help users notice their lives—not disappear into managing them.

## License

A license has not yet been selected.