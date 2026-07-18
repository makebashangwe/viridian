Phase 6: Finish Converting DB [STATUS: COMPLETE]

Phase 7A — Complete core persistence [STATUS: COMPLETE]
    Add SQLAlchemy foreign keys and relationships.
    Rename Sessions to Session or ActivitySession.
    Convert XP routes to database queries.
    Add Goal ORM model.
    Convert goal progress.
    Add Reward and RewardRedemption ORM models.
    Convert reward balance and redemption.
    Remove unused fake-list references.

Phase 7B — Stabilize the contract [STATUS: IN  PROGRESS]
[/]Rename models.py to schemas.py.
[/]Add request validation 
[/]Add response schemas 
[/]Standardize route status codes and errors.
[/] Move secrets/configuration into environment settings.
[/]Add .env.example

Phase 7C — Protect the database

7C.1 — Automated tests
[/] Add pytest
[/] Create isolated test database setup
[/] Test auth
[/] Test activities
[ ] Test sessions and scoring [IN PROGRESS]
[ ] Test XP
[ ] Test goals
[ ] Test rewards and redemptions

7C.2 — Database migrations
[ ] Add Alembic
[ ] Create initial migration
[ ] Remove runtime create_all()

======================================================
Phase 8 : Frontend foundation and API integration

[ ] Configure environment-based CORS.
[ ] Create the frontend application shell.
[ ] Establish a centralized API client.
[ ] Connect registration, login, logout, and current-user flows.
[ ] Build the lightweight activity check-in experience first.
[ ] Add recent-session and calm progress-review views.
[ ] Add activity, goal, and reward management.
[ ] Implement responsive and accessible interaction patterns.
[ ] Keep advanced analytics and elaborate dashboards secondary.

*The VIRIDIAN EXPERIENCE:
    open app
    → log in
    → choose an activity
    → record a lightweight check-in
    → see a calm confirmation
    → leave
=====================================================

8A — Frontend shell

Build:
    navigation
    theme variables
    responsive layout
    API base URL configuration
    shared loading and error components

This gives the frontend a stable structure before business features are added.

8B — Authentication connection

Build:
    registration
    login
    logout
    current-user request
    protected-route behavior
    token storage and expiration handling

This proves the frontend can communicate with the backend securely.

8C — Core check-in experience

Build the most important user flow first:
    active activity list
    select activity
    enter duration
    optional location and note
    submit session
    show earned points and simple confirmation

This should feel fast and low-pressure. A check in screen should probably take seconds, not feel like filling out a report.

8D — Lightweight review

Add:
    recent sessions
    XP summary
    progress toward goals
    available reward balance


8E — Configuration screens

Add:
    create/edit/archive/restore activities
    create goals
    create rewards
    redeem rewards


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

====================================================
 
* Then Phase 10 could focus on product learning and refinement: accessibility testing, onboarding improvements, notification design, user-controlled reviews, and deciding which deeper features are actually justified by real behavior.