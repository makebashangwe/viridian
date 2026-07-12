# Viridian Development Journal — July 2026

## July 7, 2026 — Project inception and authentication foundation

- **Changes:** Created the Viridian repository and initial FastAPI backend; added user registration, password hashing, JWT login, request models, and foundational project documentation.
- **Bugs:** Removed an accidentally committed test PDF and reconciled the initial local/remote repository history.
- **Lessons:** Establishing authentication and documenting the intended structure early gives later feature work a stable contract.
- **Current status:** The backend skeleton and in-memory authentication flow are in place.
- **Next step:** Build activity-rule CRUD and the first workout-tracking domain logic.

## July 9, 2026 — Core activity, session, goal, and reward engines

- **Changes:** Implemented activity-rule CRUD, workout-session logging, points/XP aggregation, goal tracking, and the initial rewards engine. Added phase notes and a testing checklist, expanded the API, and prepared the PostgreSQL dependency and container setup.
- **Bugs:** Corrected delete-response status handling, duplicate imports/logic, an `activity_rule` naming error, several typos, and other minor endpoint issues found during testing.
- **Lessons:** Rapid phase-by-phase implementation needs frequent cleanup and route testing to keep shared scoring and aggregation logic consistent.
- **Current status:** Phases 2–5 are implemented and their in-memory flows pass initial tests; database migration is ready to begin.
- **Next step:** Replace the temporary data stores with PostgreSQL-backed models and persistence.

## July 10, 2026 — PostgreSQL-backed authentication

- **Changes:** Added SQLAlchemy database configuration and user ORM models, moved Docker Compose to the project root, updated registration and login to persist and query users in PostgreSQL, and expanded ignore rules and dependencies.
- **Bugs:** Reworked authentication code where the previous in-memory assumptions did not fit database sessions and ORM records.
- **Lessons:** Persistence migration is safest one domain at a time, with API schemas kept separate from database models.
- **Current status:** User authentication is PostgreSQL-backed; the remaining activity, session, goal, XP, and reward domains still need migration.
- **Next step:** Migrate activity rules first, test them, then convert session logic.

## July 11, 2026 — Domain persistence and relational integrity

- **Changes:** Migrated activity rules and workout sessions from fake stores to PostgreSQL, added ORM relationships and foreign keys, and updated phase documentation and test coverage notes.
- **Bugs:** Fixed migration-era route and model mismatches, then verified the converted activity flows and relationship changes with successful tests.
- **Lessons:** Explicit foreign keys and ORM relationships make ownership and cascade behavior clearer than manually coordinated in-memory records.
- **Current status:** Authentication, activities, and sessions are persisted and tested; goals and progress are the next major database-backed area.
- **Next step:** Implement and test Phase 7A goal/progress persistence, then proceed to the remaining engines.

## July 12, 2026 — Goal/reward persistence and backend refactor

- **Changes:** Completed and tested PostgreSQL-backed goal/progress and reward logic, including mathematical and edge-case checks. Refactored the monolithic backend into domain routers, schemas, and service modules; reorganized project notes into `docs`; expanded configuration and README documentation; and established this persistent dev journal.
- **Bugs:** Fixed a fatal `is_active` issue in activity rules and resolved issues uncovered while testing goal/reward routes; all tested routes returned successful results after the refactor.
- **Lessons:** Separating routing, schemas, persistence models, and business services makes a fast-growing API easier to reason about without changing its external behavior.
- **Current status:** The backend is modular, PostgreSQL-backed across the implemented phases, and passing the current route tests. Legacy monolithic files are staged for later removal.
- **Next step:** Complete Phase 7B and the remaining planned backend work, remove verified legacy files, then begin the frontend integration phase.
