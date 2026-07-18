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
[ ] Add pytest
[ ] Create isolated test database setup
[ ] Test auth
[ ] Test activities
[ ] Test sessions and scoring
[ ] Test XP
[ ] Test goals
[ ] Test rewards and redemptions

7C.2 — Database migrations
[ ] Add Alembic
[ ] Create initial migration
[ ] Remove runtime create_all()

Phase 8 — Backend organization and frontend connection
Split routes into routers.
Extract only meaningful reusable calculations into services.
Add CORS configuration.
Establish the frontend API client.
Build the lightweight check-in experience first.
Keep analytics and elaborate dashboards secondary.

Phase 9 — Delivery engineering
Backend Dockerfile.
Complete Compose stack.
GitHub Actions for tests and linting.
Staging deployment.
Production secrets and managed PostgreSQL.
Logging, monitoring, backup, and recovery planning.