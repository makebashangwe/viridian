Phase 0-4 : Complete (July 4-9) Building Viridian Concept & Planning, Completing CRUD + APIs for basic functionality of the MVP. Defining scope, etc.etc...

Phase 5 & 6: Completed (July 11) Finish Reward Center API + API Testing... (MVP) | Clean fake-list backend/ stabilize (in-memory complete)

Phase 7: SQLite / SQLAlchemy DB [current]
    - Finish Fake DB Conversion to Postgre SQL
    - Migrate simple ID logic to SQL Foreign Key / Primary Key Relationships (session.user,user.sessions)

    - Add Response Models (PYDANTIC)
    - Add Service/Helper functions to break up lengthy routes

    -Replace create_all with Alembic migrations so I can change tables without wiping Docker volumes.

Phase 8: Front End Conection  
    - WEB FRONT END : REACT
    - MOBILE APP : REACT NATIVE / EXPO

    1. Build responsive web app
    2. Make it mobile-friendly in browser
    3. Then build real mobile app later with React Native / Expo

Phase 9: Containerization (DOCKER) 
    - Backend Container
    - Frontend Container
    - Postgres / DB Container

[MAJOR  MILESTONE]

Phase 10: DB in AWS (FAST API -> PostgreSQL)
Postgres → AWS RDS
Backend → ECS/Fargate or EC2
Frontend → S3/CloudFront or Amplify
Secrets → AWS Secrets Manager
Logs → CloudWatch


Phase 11: Finish Clean for Portfolio.
