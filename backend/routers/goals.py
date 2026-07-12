from database import get_db

import db_models #DB Models

from services.goal_service import update_user_goal_progress

from schemas import (
    GoalCreate) #request/response schemas

from sqlalchemy.orm import Session

from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends)

from auth import get_current_user


#CREATING APPLICATION
router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)

#GOAL LOGIC  

#Create goal
@router.post("")
def create_goal(
    incoming_goal_data: GoalCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)):
    
    if incoming_goal_data.activity_rule_id is not None:
        matching_activity_rule = (
            db.query(db_models.ActivityRule)
            .filter(
                db_models.ActivityRule.user_id == current_user["id"],
                db_models.ActivityRule.id==incoming_goal_data.activity_rule_id
                )
            .first()
        )
        if matching_activity_rule == None:
            raise HTTPException(status_code=404,detail="Activity Rule not Found")
    
    
    new_goal = db_models.Goal(
        user_id = current_user["id"],
        **incoming_goal_data.model_dump()
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal

    
#See all goals
@router.get("")
def get_goals(
    current_user = Depends(get_current_user),
    db:Session= Depends(get_db)):
    goals = (
        db.query(db_models.Goal)
        .filter(db_models.Goal.user_id ==current_user["id"],
        )
        .all()
    )
    return goals


#Delete Goal
@router.delete("/{goal_id}")
def delete_goal(
    goal_id : int,
    current_user = Depends(get_current_user),
    db:Session= Depends(get_db)):
    
    target_goal = (
        db.query(db_models.Goal)
        .filter(db_models.Goal.user_id ==current_user["id"],
                db_models.Goal.id == goal_id
        )
        .first()
    )

    if target_goal == None:
        raise HTTPException(status_code=404,detail="Goal Not Found")

    db.delete(target_goal)
    db.commit()

    return {
                "message": "Success."
            }

#-----------------------------------------------------------------------------
#GOAL PROGRESS LOGIC



#See All Updated Goal Progress
@router.get("/progress")
def get_goals_progress(
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    
    goals = update_user_goal_progress(current_user["id"],db)
    
    return goals


#Goal Rewards
@router.get("/rewards-summary")
def get_rewards_summary(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)):
    
    update_user_goal_progress(current_user["id"],db)
    
    completed_goals = (
        db.query(db_models.Goal)
        .filter(db_models.Goal.user_id ==current_user["id"],
                db_models.Goal.is_completed==True
        )
        .all()
    )

    reward_points_earned = 0

    for goal in completed_goals:
        reward_points_earned += goal.reward_points

    return {
        "user_id" : current_user["id"],
        "completed_goals" : completed_goals,
        "reward_points_earned": reward_points_earned,
        "completed_goal_count": len(completed_goals)
    }

            
#Goal Progress by ID
@router.get("/{goal_id}/progress")
def get_goal_progress_by_id(
    goal_id: int,
    current_user = Depends(get_current_user),
    db:Session=Depends(get_db)):
    
    update_user_goal_progress(current_user["id"],db)
    
    goal = (
        db.query(db_models.Goal)
        .filter(db_models.Goal.user_id ==current_user["id"],
                db_models.Goal.id == goal_id
        )
        .first()
    )
    if goal == None:
        raise HTTPException(status_code=404,detail="Goal Not Found.")
    
    return {
            "goal_id": goal.id,
            "title" : goal.title,
            "progress_value" : goal.progress_value,
            "target_value" : goal.target_value,
            "is_completed" : goal.is_completed
        }


#Find Goal by ID
@router.get("/{goal_id}")
def get_goals_by_id(
    goal_id: int,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    goal = (
        db.query(db_models.Goal)
        .filter(db_models.Goal.user_id ==current_user["id"],
                db_models.Goal.id == goal_id
        )
        .first()
    )
    
    if goal == None:
        raise HTTPException(status_code=404,detail="Goal Not Found.")
    

    return goal