# Phase 5.5 Testing Checklist

## Auth
- Register user
- Login user
- Copy token
- Authorize in Swagger
- Test /users/me

## Activities
- POST /activities
- GET /activities
- GET /activities/{activity_id}
- PATCH /activities/{activity_id}
- DELETE /activities/{activity_id}

## Sessions
- POST /sessions
- GET /sessions
- GET /sessions/{session_id}
- DELETE /sessions/{session_id}

## XP
- GET /xp/summary
- GET /xp/by-activity
- GET /xp/by-activity/{activity_id}

## Goals
- POST /goals
- GET /goals
- GET /goals/progress
- GET /goals/rewards-summary
- GET /goals/{goal_id}/progress
- GET /goals/{goal_id}
- DELETE /goals/{goal_id}

## Rewards
- POST /rewards
- GET /rewards
- GET /rewards/balance
- GET /rewards/{reward_id}
- POST /rewards/{reward_id}/redeem
- DELETE /rewards/{reward_id}