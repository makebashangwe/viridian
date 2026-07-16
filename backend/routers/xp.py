from database import get_db
import db_models #DB Models

from schemas import (
    XPByActivityIdResponse,
    XPByActivityResponse,
    XPSummaryResponse,
    XPBySessionIdResponse
)

from sqlalchemy.orm import Session

from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends)

from auth import get_current_user


router = APIRouter(
    prefix="/xp",
    tags=["XP"]
)

#XP / POINTS LOGIC 

#XP / Point Summary
@router.get("/summary",
            response_model=XPSummaryResponse)
def get_xp_summary(
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)):

    
    total_points = 0
    total_sessions = 0

    bonus_intervals_total = 0
    main_goal_completed_total = 0
    legal_goal_completed_total = 0

    #find session based on user id and calculation logic
    activity_sessions = (
        db.query(db_models.ActivitySession)
        .filter(db_models.ActivitySession.user_id==current_user["id"]
        )
        .all()
    )
    
    for activity_session in activity_sessions:
        total_points += activity_session.points_earned
        total_sessions +=1
        bonus_intervals_total += activity_session.bonus_intervals
        
        if activity_session.legal_goal_completed:
            legal_goal_completed_total+=1
        
        if activity_session.main_goal_completed:
            main_goal_completed_total +=1            

    return {
        "user_id" : current_user["id"],
        "total_points" : total_points,
        "total_sessions" : total_sessions,
        "legal_goal_completed_total": legal_goal_completed_total,
        "main_goal_completed_total": main_goal_completed_total,
        "bonus_intervals_total" : bonus_intervals_total
    }

#XP / Points by Activity Type
@router.get("/by-activity",
            response_model=XPByActivityResponse)
def get_xp_by_activity(
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)):

    target_activity = (
    db.query(db_models.ActivityRule)
    .filter(
        db_models.ActivityRule.user_id == current_user["id"],
    )
    .first()
)
    
    xp_by_activity = {}
    
    #find session based on user id 
    activity_sessions = (
        db.query(db_models.ActivitySession)
        .filter(db_models.ActivitySession.user_id==current_user["id"]
        )
        .all()
    )
    
    for activity_session in activity_sessions:
        if activity_session.activity_name in xp_by_activity:
            xp_by_activity[activity_session.activity_name] += activity_session.points_earned
        else:
            xp_by_activity[activity_session.activity_name] = activity_session.points_earned
            
    return {
        "user_id": current_user["id"],
        "xp_by_activity": xp_by_activity
    }

        
#XP / Points by Activity Rule ID
@router.get("/by-activity/{activity_rule_id}",
            response_model=XPByActivityIdResponse)
def get_xp_by_activity_id(
    activity_rule_id:int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)):
    
    #IF I EXIST:
    activity_sessions = (
        db.query(db_models.ActivitySession)
        .filter(db_models.ActivitySession.user_id==current_user["id"]
        )
        .filter(db_models.ActivitySession.activity_rule_id == activity_rule_id)
        .all()
    )
   
    xp_by_activity_id = 0

    for activity_session in activity_sessions:
        xp_by_activity_id+=activity_session.points_earned
    
    return {
        "user_id": current_user["id"],
        "activity_rule_id": activity_rule_id,
        "total_points": xp_by_activity_id
    }

#XP / Points by Session ID
@router.get("/by-session/{session_id}",
            response_model=XPBySessionIdResponse)
def get_xp_by_session_id(
    session_id:int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)):
    
    activity_session = (
        db.query(db_models.ActivitySession)
        .filter(db_models.ActivitySession.user_id==current_user["id"]
        )
        .filter(db_models.ActivitySession.id == session_id)
        .first()
    )
    
    if activity_session == None:
        raise HTTPException(status_code = 404, detail="Session not found.")

    
    return {
        "user_id": current_user["id"],
        "session_id": session_id,
        "total_points": activity_session.points_earned
    }