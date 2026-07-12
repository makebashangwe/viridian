from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException)

from sqlalchemy.orm import Session

import db_models
from database import get_db

from auth import get_current_user

from schemas import (
    ActivityRuleCreate,
    ActivityRuleChange,
    ActivityRuleResponse
)

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)

@router.post(
    "",
    response_model=ActivityRuleResponse,
    status_code=201
)
def create_activity_rule(
    incoming_activity_rule: ActivityRuleCreate,#accept activity rule data,
    current_user = Depends(get_current_user), #Require current user
    db: Session=Depends(get_db)): #Access DB

    new_activity = db_models.ActivityRule( #IN the DB model Activity rule, create a new_activity
        user_id=current_user["id"], #appending necessary params
        **incoming_activity_rule.model_dump()
    )

    db.add(new_activity) #add the new activity
    db.commit() #commit changes
    db.refresh(new_activity)

    return new_activity

#Get Activity Rules
@router.get(
    "",
    response_model=list[ActivityRuleResponse]
)
def get_activity_rules(
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    activities = (
        db.query(db_models.ActivityRule)
        .filter(db_models.ActivityRule.user_id == current_user["id"])
        .filter(db_models.ActivityRule.is_active==True)
        .all()
    )

    return activities

#Get by Activity ID
@router.get(
    "/{activity_id}",
    response_model=ActivityRuleResponse
)
def get_activity_by_id(
    activity_id :int, 
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):

    target_activity_rule = (
        db.query(db_models.ActivityRule)
        .filter(db_models.ActivityRule.user_id == current_user["id"])
        .filter(db_models.ActivityRule.id == activity_id)
        .filter(db_models.ActivityRule.is_active==True)
        .first()
    )
    if target_activity_rule == None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found.")
    
    return target_activity_rule


#Edit Activity By ID
@router.patch(
    "/{activity_id}",
    response_model=ActivityRuleResponse
)
def edit_activity_by_id(
    activity_id :int,
    updated_activity_rule : ActivityRuleChange,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    target_activity_rule = (
        db.query(db_models.ActivityRule)
        .filter(db_models.ActivityRule.user_id == current_user["id"])
        .filter(db_models.ActivityRule.id == activity_id)
        .filter(db_models.ActivityRule.is_active==True)
        .first()
    )

    if target_activity_rule == None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found.")
    
    updated_data = updated_activity_rule.model_dump(exclude_unset=True) #takes out the NONE values and converts to a dict
    
    for key,value in updated_data.items():
        setattr(target_activity_rule,key,value)
    
    db.commit()
    db.refresh(target_activity_rule)

    return target_activity_rule

@router.patch(
        "/{activity_id}/archive",
        response_model=ActivityRuleResponse)
def archive_activity(
    activity_id :int,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    
    target_activity_rule = (
        db.query(db_models.ActivityRule)
        .filter(db_models.ActivityRule.user_id == current_user["id"])
        .filter(db_models.ActivityRule.id == activity_id)
        .first()
    )

    if target_activity_rule == None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found.")
    
    target_activity_rule.is_active = False

    db.commit()
    db.refresh(target_activity_rule)

    return target_activity_rule
     
@router.patch(
        "/{activity_id}/restore",
        response_model=ActivityRuleResponse)
def restore_activity(
    activity_id :int,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    target_activity_rule = (
        db.query(db_models.ActivityRule)
        .filter(db_models.ActivityRule.user_id == current_user["id"])
        .filter(db_models.ActivityRule.id == activity_id)
        .first()
    )

    if target_activity_rule == None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found.")
    target_activity_rule.is_active = True
    
    db.commit()
    db.refresh(target_activity_rule)

    return target_activity_rule