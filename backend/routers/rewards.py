from database import get_db

import db_models #DB Models

from services.reward_service import get_user_balance

from schemas import (
    RewardCreate) #request/response schemas

from sqlalchemy.orm import Session

from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends)

from auth import get_current_user


#CREATING APPLICATION
router = APIRouter(
    prefix="/rewards",
    tags=["Rewards"]
)

#Create Reward
@router.post("")
def create_reward(
    incoming_reward: RewardCreate,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)):
    if incoming_reward.required_goal_id is not None:
        matching_goal_id = (
            db.query(db_models.Goal)
            .filter(db_models.Goal.user_id == current_user["id"])
            .filter(db_models.Goal.id == incoming_reward.required_goal_id)
            .first()
        )
        if matching_goal_id == None:
            raise HTTPException(status_code=404,detail="Goal not Found.")
    
    if (incoming_reward.is_locked and incoming_reward.required_goal_id is None):
            raise HTTPException(status_code=400, detail="Locked rewards require a goal.")
    
    new_reward = db_models.Reward (
        user_id = current_user["id"],
        **incoming_reward.model_dump()
        )
    
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)

    return new_reward

#See All Rewards
@router.get("")
def get_all_rewards(
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    rewards = (
        db.query(db_models.Reward)
        .filter(db_models.Reward.user_id == current_user["id"])
        .all()
    )
    
    return rewards

#View Reward Balance
@router.get("/balance")
def get_reward_balance(
    current_user=Depends(get_current_user),
    db:Session = Depends(get_db)):
    
    user_balance_info = get_user_balance(current_user["id"],db)
    
    return user_balance_info

#Redeem by Reward ID
@router.post("/{reward_id}/redeem")
def redeem_reward(
    reward_id : int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)):

    reward = (
        db.query(db_models.Reward)
        .filter(db_models.Reward.user_id==current_user["id"])
        .filter(db_models.Reward.id == reward_id)
        .first()
    )
    if reward == None:
        raise HTTPException(status_code=404,detail="Reward Not Found.")

    user_balance_info = get_user_balance(current_user["id"],db)
    if user_balance_info["available_balance"] < reward.point_cost:
        raise HTTPException(status_code = 400, detail="Not Enough Points")
    
    if reward.is_locked:
        required_goal = (
                        db.query(db_models.Goal)
                        .filter(
                            db_models.Goal.user_id == current_user["id"],
                            db_models.Goal.id == reward.required_goal_id
                        )
                        .first()
                    )
        if required_goal is None:
            raise HTTPException(
                status_code=400,
                detail="Required goal is missing."
            )

        if not required_goal.is_completed:
            raise HTTPException(
                status_code=400,
                detail="Required goal is not completed."
            )
        
    new_redemption = db_models.RewardRedemption(
        user_id = current_user["id"],
        reward_id = reward.id,
        reward_name = reward.name,
        point_cost = reward.point_cost
    )

    db.add(new_redemption)
    db.commit()
    db.refresh(new_redemption)

    return new_redemption

#Get by Reward ID
@router.get("/{reward_id}")
def get_reward_by_id(
    reward_id : int,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    reward = (
        db.query(db_models.Reward)
        .filter(db_models.Reward.user_id==current_user["id"])
        .filter(db_models.Reward.id == reward_id)
        .first()
    )
    if reward == None:
        raise HTTPException(status_code=404,detail="Reward Not Found.")

    return reward

# Archive and remove an active reward
@router.delete("/{reward_id}")
def delete_reward(
    reward_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reward = (
        db.query(db_models.Reward)
        .filter(
            db_models.Reward.user_id == current_user["id"],
            db_models.Reward.id == reward_id
        )
        .first()
    )

    if reward is None:
        raise HTTPException(
            status_code=404,
            detail="Reward Not Found."
        )

    archived_reward = db_models.RewardsArchive(
        original_reward_id=reward.id,
        user_id=current_user["id"],

        required_goal_id=reward.required_goal_id,
        required_goal_title=(
            reward.required_goal.title
            if reward.required_goal is not None
            else None
        ),

        name=reward.name,
        description=reward.description,
        tag=reward.tag,
        point_cost=reward.point_cost,
        estimated_cost=reward.estimated_cost,
        is_locked=reward.is_locked,
        image_url=reward.image_url
    )

    db.add(archived_reward)
    db.delete(reward)
    db.commit()
    db.refresh(archived_reward)

    return {
        "message": f"Reward #{reward_id} archived and removed.",
        "archive_id": archived_reward.id
    }