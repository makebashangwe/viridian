Phase 6: Finish Converting DB

Phase 7A — Complete core persistence
    Add SQLAlchemy foreign keys and relationships.
    Rename Sessions to Session or ActivitySession.
    Convert XP routes to database queries.
    Add Goal ORM model.
    Convert goal progress.
    Add Reward and RewardRedemption ORM models.
    Convert reward balance and redemption.
    Remove unused fake-list references.

Phase 7B — Stabilize the contract
Rename models.py to schemas.py.
Add request validation.
Add response schemas.
Standardize route status codes and errors.
Move secrets/configuration into environment settings.
Add .env.example.
Phase 7C — Protect the database
Add pytest.
Test authentication and ownership.
Test scoring boundaries.
Test XP, goal, and reward calculations.
Add Alembic.
Generate the initial migration.
Remove runtime create_all().

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