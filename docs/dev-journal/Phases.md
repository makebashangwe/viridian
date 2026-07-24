# Phase 6: Finish Converting DB [STATUS: COMPLETE]

# Phase 7 [STATUS: COMPLETE]

    Phase 7A — Complete core persistence [STATUS: COMPLETE]
        Add SQLAlchemy foreign keys and relationships.
        Rename Sessions to Session or ActivitySession.
        Convert XP routes to database queries.
        Add Goal ORM model.
        Convert goal progress.
        Add Reward and RewardRedemption ORM models.
        Convert reward balance and redemption.
        Remove unused fake-list references.

    Phase 7B — Stabilize the contract [STATUS: COMPLETE]
    [/]Rename models.py to schemas.py.
    [/]Add request validation 
    [/]Add response schemas 
    [/]Standardize route status codes and errors.
    [/] Move secrets/configuration into environment settings.
    [/]Add .env.example

    Phase 7C — Protect the database [STATUS: COMPLETE]

    7C.1 — Automated tests
    [/] Add pytest
    [/] Create isolated test database setup
    [/] Test auth
    [/] Test activities
    [/] Test sessions and scoring [IN PROGRESS]
    [/] Test XP
    [/] Test goals
    [/] Test rewards and redemptions

    77 passed in 33.88s


    7C.2 — Database migrations
    [/] Add Alembic
    [/] Create initial migration
    [/] Remove runtime create_all()

    install Alembic
        → initialize Alembic
        → connect it to Viridian config
        → import SQLAlchemy metadata
        → generate initial migration
        → inspect migration
        → apply it to a fresh database
        → verify tests
        → remove Base.metadata.create_all(...)

    prove 
        empty database
            → alembic upgrade head
            → complete Viridian schema
            → 77 tests still pass

====================================================== 
# Phase 8 : Frontend foundation and API integration


## Phase 8A — Frontend shell [STATUS: IN PROGRESS]
    Goal: Create a responsive React application that can run beside the FastAPI backend.

    [/] Verify Node.js and npm
    [/] Create React + TypeScript frontend with Vite
    [/] Remove starter demo content
    [/] Establish frontend folders
    [/] Add global design tokens
    [/] Create basic application shell
    [/] Add placeholder routes
    [/] Confirm production build succeeds

We are using React + TypeScript + Vite. React officially supports starting a React app with a build tool such as Vite, and Vite provides a react-ts template.

Phase 8B — API and authentication
    [ ] Add environment-based API URL
    [ ] Configure FastAPI CORS
    [ ] Create centralized API client
    [ ] Add login
    [ ] Add registration
    [ ] Add current-user loading
    [ ] Add logout
    [ ] Add protected routes
    [ ] Handle expired and invalid sessions

Phase 8C — Lightweight check-in
    [ ] Load active activities
    [ ] Select an activity
    [ ] Enter session duration
    [ ] Use default or selected location
    [ ] Add optional note
    [ ] Submit session
    [ ] Display calm success confirmation
    [ ] Handle validation errors accessibly

    This is the most important frontend workflow:

    log in
    → choose activity
    → record check-in
    → “Saved.”
    → return to life

Phase 8D — Calm review
    [ ] Show recent sessions
    [ ] Show simple XP summary
    [ ] Show active goal progress
    [ ] Show reward balance
    [ ] Add useful empty states
    [ ] Avoid dense dashboards

Phase 8E — Management screens
    [ ] Create and edit activities
    [ ] Archive and restore activities
    [ ] Create and view goals
    [ ] Create rewards
    [ ] Redeem rewards
    [ ] Archive rewards

=====================================================
Phase 9 : Deployment, Observability, and real-world hardening

[ ] Containerize backend and frontend
[ ] Add production environment configuration
[ ] Deploy PostgreSQL
[ ] Deploy FastAPI
[ ] Deploy frontend
[ ] Configure HTTPS and domains
[ ] Add CI/CD
[ ] Add structured logging
[ ] Add health checks
[ ] Add error monitoring
[ ] Add backup and restore procedures
[ ] Add privacy and data-export foundations
[ ] Run a small private beta

Target Completion Date for phase 9: August 
    First half: deployment and hardening [TARGET: AUGUST 15TH ]
        production database
        deployed backend
        deployed frontend
        CORS and environment configuration
        GitHub Actions
        migrations in deployment
        HTTPS
        logs and health checks
        backups
        account/data privacy basics
    Second half: actual usage [TARGET: SEPTEMBER 5]
        use Viridian myself
        have one trusted person test it 
        record friction and bugs
        fix only the issues that interfere with ordinary use
        document setup, architecture, screenshots, and deployment
====================================================
 
* Then Phase 10 could focus on product learning and refinement: accessibility testing, onboarding improvements, notification design, user-controlled reviews, and deciding which deeper features are actually justified by real behavior.