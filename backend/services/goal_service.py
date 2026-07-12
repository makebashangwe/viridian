import db_models #DB Models

#HELPER FUCNTIONS:
def calculate_stats(sessions):
    total_xp = 0
    total_sessions = 0
    legal_goals_completed = 0
    main_goals_completed = 0
    bonus_intervals = 0

    for session in sessions:
        total_xp += session.points_earned
        total_sessions += 1
        bonus_intervals += session.bonus_intervals

        if session.legal_goal_completed:
            legal_goals_completed += 1

        if session.main_goal_completed:
            main_goals_completed += 1

    return {
        "total_xp": total_xp,
        "total_sessions": total_sessions,
        "legal_goals_completed": legal_goals_completed,
        "main_goals_completed": main_goals_completed,
        "bonus_intervals": bonus_intervals
    }
def update_user_goal_progress(current_user_id, db):
    activity_sessions = (
        db.query(db_models.ActivitySession)
        .filter(db_models.ActivitySession.user_id==current_user_id
        )
        .all()
    )
    goals = (
        db.query(db_models.Goal)
        .filter(db_models.Goal.user_id == current_user_id,
        )
        .all()
    )

    for goal in goals:
        
        if goal.activity_rule_id is None:
            relevant_sessions = activity_sessions
        else:
            relevant_sessions = [
                session
                for session in activity_sessions
                if session.activity_rule_id == goal.activity_rule_id
            ]
        
        stats = calculate_stats(relevant_sessions)
        target_type = goal.target_type

        if target_type in stats: #Will Be changing this in Phase 7B
            goal.progress_value = stats[target_type]
          
        goal.is_completed = goal.progress_value >= goal.target_value

    db.commit()

    for goal in goals:
        db.refresh(goal)
    
    return goals