#IMPORTS
from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends)

from database import get_db

import db_models #DB Models

from schemas import (
    ActivitySessionCreate,
    ActivitySessionResponse,
    MessageResponse) #request/response schemas

from sqlalchemy.orm import Session

from auth import get_current_user



router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

#create session
@router.post(
    "",
    response_model=ActivitySessionResponse,
    status_code=201)
def create_activity_session(
    incoming_session: ActivitySessionCreate,#take in activity session data
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)):

    #find the matching activity rule information
    matching_activity_rule = (
        db.query(db_models.ActivityRule)
        .filter(db_models.ActivityRule.user_id == current_user["id"])
        .filter(db_models.ActivityRule.is_active.is_(True))
        .filter(db_models.ActivityRule.id == incoming_session.activity_rule_id)
        .first()
    )

    if matching_activity_rule is None:
        raise HTTPException(status_code=404,detail="Active activity rule not found.")
    
    if incoming_session.duration_minutes > matching_activity_rule.max_session_minutes : #Prevent 48 hour sessions lol
        raise HTTPException(status_code = 400, detail="Session exceeds max allowed minutes.")

    #Point logic
    points_earned = 0
    legal_goal_completed = False
    main_goal_completed = False
    bonus_intervals = 0

    if incoming_session.duration_minutes >= matching_activity_rule.legal_minutes:
        legal_goal_completed = True
        points_earned += matching_activity_rule.legal_points

    if incoming_session.duration_minutes >= matching_activity_rule.goal_minutes:
        main_goal_completed = True
        points_earned += matching_activity_rule.goal_points
    
    if incoming_session.duration_minutes > matching_activity_rule.goal_minutes:
        extra_minutes = incoming_session.duration_minutes - matching_activity_rule.goal_minutes
        bonus_intervals = extra_minutes // matching_activity_rule.bonus_interval_minutes
        points_earned += bonus_intervals * matching_activity_rule.bonus_points

    new_session = db_models.ActivitySession(
        user_id = current_user["id"],
        activity_rule_id = matching_activity_rule.id,
        
        activity_name = matching_activity_rule.name,
        duration_minutes = incoming_session.duration_minutes,
        location = incoming_session.location,
        
        points_earned = points_earned,
        legal_goal_completed = legal_goal_completed,
        main_goal_completed = main_goal_completed,
        bonus_intervals = bonus_intervals,
        
        notes = incoming_session.notes
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

#See All Sessions
@router.get("",
            response_model=list[ActivitySessionResponse],
)
def get_sessions(
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)):
    
    user_sessions = db.query(db_models.ActivitySession).filter(db_models.ActivitySession.user_id==current_user["id"]).all()
    
    return user_sessions
   
    
#Return by Session ID
@router.get(
    "/{session_id}",
    response_model=ActivitySessionResponse)
def get_session_by_id(
    session_id :int, 
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    target_session = db.query(db_models.ActivitySession).filter(db_models.ActivitySession.user_id==current_user["id"]).filter(db_models.ActivitySession.id == session_id).first()
    if target_session == None:
        raise HTTPException(status_code=404,detail="Session not found.")
    
    return target_session

#delete session               
@router.delete("/{session_id}",
                response_model=MessageResponse)
def delete_session(
    session_id :int,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    target_session = db.query(db_models.ActivitySession).filter(db_models.ActivitySession.user_id==current_user["id"]).filter(db_models.ActivitySession.id == session_id).first()
    
    if target_session == None:
        raise HTTPException(status_code=404,detail="Session not found.")
    
    db.delete(target_session)
    db.commit()
    
    return {
        "message": f"Successfully deleted Session #{session_id}."
    }
