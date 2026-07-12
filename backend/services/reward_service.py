import db_models #DB Models

from services.goal_service import update_user_goal_progress

#CALCULATE BALANCE
def get_user_balance(current_user_id,db):

    update_user_goal_progress(current_user_id,db)

    reward_redemptions = (
        db.query(db_models.RewardRedemption)
        .filter(db_models.RewardRedemption.user_id == current_user_id)
        .all()
    )
    
    completed_goals = (
        db.query(db_models.Goal)
        .filter(db_models.Goal.user_id ==current_user_id,
                db_models.Goal.is_completed==True
        )
        .all()
    )
    reward_points_earned = 0
    reward_points_spent = 0

    for goal in completed_goals:
        reward_points_earned += goal.reward_points
    
    for redemption in reward_redemptions:
        reward_points_spent += redemption.point_cost
    
    available_balance = reward_points_earned-reward_points_spent
    
    return {
        "user_id" : current_user_id,
        "reward_points_earned" : reward_points_earned,
        "reward_points_spent": reward_points_spent,
        "available_balance" : available_balance
    }