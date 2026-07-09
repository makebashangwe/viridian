from fastapi import FastAPI, HTTPException, Depends
from data import users, activity_rules, activity_sessions, goals, rewards #Fake DBs
from models import UserRegister, UserLogin, ActivityRuleCreate, ActivityRuleChange, ActivitySessionCreate, GoalCreate
from auth import hash_password, verify_password, create_access_token, get_current_user

app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "Viridian API is running"}

#Register User and generate Hash
@app.post("/auth/register")
def register_user(incoming_user: UserRegister):
    for existing_user in users:
        if existing_user["email"] == incoming_user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
        if existing_user["username"] == incoming_user.username:
            raise HTTPException(status_code=400, detail="Username already exists")

    new_id = len(users)+1
    hashed_password = hash_password(incoming_user.password)
    new_user = {
        "id" : new_id,
        "email": incoming_user.email,
        "username": incoming_user.username,
        "password_hash": hashed_password
    }
    users.append(new_user)
    return {"id": new_user["id"], 
            "email" : new_user["email"], 
            "username" : new_user["username"]
            }


#Authentication Logic
@app.post("/auth/login")
def login_user(login_data: UserLogin):
    for existing_user in users:
        if existing_user["email"] == login_data.email:
            success = verify_password(
                login_data.password, 
                existing_user["password_hash"])
            if success:
                access_token = create_access_token(
                    data={"sub": existing_user["email"]} #who the token belongs to
                )
    
                return {
                    "access_token" : access_token,
                    "token_type" : "bearer",
                }
            
            raise HTTPException(status_code=401, detail="Invalid email or password")
    
    raise HTTPException(status_code=401, detail="Invalid email or password")

#Get information about the current user 
@app.get("/users/me")
def read_users_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "username": current_user["username"]
    }

#!!!Needs Testing!!!

#Creating Activity Rules
@app.post("/activities")
def create_activity_rule(
    incoming_activity_rule: ActivityRuleCreate,#accept activity rule data
    current_user = Depends(get_current_user)):#require the current logged-in user
    
    #create the new activity id
    activity_id = len(activity_rules)+1
    #add the current user's id as the user_id
    user_id = current_user["id"]

    #save the activity rule to the list
    new_activity = {
        "id" : activity_id,
        "user_id" : user_id,
        **incoming_activity_rule.model_dump()
    }
    activity_rules.append(new_activity)
    #return the new rule
    return new_activity

#Get Activity Rules
@app.get("/activities")
def get_activity_rules(current_user = Depends(get_current_user)):
    user_activity_rules = []
    for activity in activity_rules:
        if activity["user_id"] == current_user["id"]:
            user_activity_rules.append(activity)
    return user_activity_rules

#Return by Activity ID
@app.get("/activities/{activity_id}")
def get_activity_by_id(
    activity_id :int, 
    current_user = Depends(get_current_user)):
    for activity in activity_rules:
        if (activity["user_id"] == current_user["id"]) and (activity["id"] == activity_id):
            return activity
    raise HTTPException(status_code=404,detail="Activity not found.")

#Edit Activity By ID
@app.patch("/activities/{activity_id}")
def edit_activity_by_id(
    activity_id :int,
    updated_activity_rule : ActivityRuleChange,
    current_user = Depends(get_current_user)):
    for activity in activity_rules:
        if (activity["user_id"] == current_user["id"]) and (activity["id"] == activity_id):
            updated_data = updated_activity_rule.model_dump(exclude_unset=True) #takes out the NONE values
            activity.update(updated_data)
            return activity
    raise HTTPException(status_code=404,detail="Activity not found.")

 #delete activity               
@app.delete("/activities/{activity_id}")
def delete_activity(
    activity_id :int, 
    current_user = Depends(get_current_user)):
    for activity in activity_rules:
        if (activity["user_id"] == current_user["id"]) and (activity["id"] == activity_id):
            activity_rules.remove(activity)
            return {
                "message" : "Success."
            }
    raise HTTPException(status_code=404,detail="Activity not found.")

#create session
@app.post("/sessions")
def create_activity_session(
    incoming_session: ActivitySessionCreate,#take in activity session data
    current_user = Depends(get_current_user)):#require the current logged-in user

    matching_activity = None
    
    for activity in activity_rules:
        if (activity["user_id"] == current_user["id"]) and (activity["id"] == incoming_session.activity_id):
            matching_activity = activity
            break
    if matching_activity is None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found")
    
    if incoming_session.duration_minutes > matching_activity["max_session_minutes"]: #Prevent 48 hour sessions lol
        raise HTTPException(status_code = "400", detail="Session exceeds max allowed minutes")

    #Point logic
    points_earned = 0
    legal_goal_completed = False
    main_goal_completed = False
    bonus_intervals = 0

    if incoming_session.duration_minutes >= matching_activity["legal_minutes"]:
        legal_goal_completed = True
        points_earned += matching_activity["legal_points"]

    if incoming_session.duration_minutes >= matching_activity["goal_minutes"]:
        main_goal_completed = True
        points_earned += matching_activity["goal_points"]
    
    if incoming_session.duration_minutes > matching_activity["goal_minutes"]:
        extra_minutes = incoming_session.duration_minutes - matching_activity["goal_minutes"]
        bonus_intervals = extra_minutes // matching_activity["bonus_interval_minutes"]
        points_earned += bonus_intervals * matching_activity["bonus_points"]
    new_session = {
        "id" : len(activity_sessions) +1,
        "user_id" : current_user["id"],
        "activity_id" : matching_activity["id"],
        "activity_name" : matching_activity["name"],
        "duration_minutes" : incoming_session.duration_minutes,
        "location" : incoming_session.location,
        "points_earned" : points_earned,
        "legal_goal_completed": legal_goal_completed,
        "main_goal_completed": main_goal_completed,
        "bonus_intervals": bonus_intervals,
        "notes": incoming_session.notes
    }
    
    activity_sessions.append(new_session)
    return new_session

#See All Sessions
@app.get("/sessions")
def get_sessions(current_user = Depends(get_current_user)):#require the current logged-in user
    user_sessions = []
    
    for session in activity_sessions:
        if (session["user_id"] == current_user["id"]):
            user_sessions.append(session)

    return user_sessions
    
#Return by Session ID
@app.get("/sessions/{session_id}")
def get_session_by_id(
    session_id :int, 
    current_user = Depends(get_current_user)):
    for session in activity_sessions:
        if (session["user_id"] == current_user["id"]) and (session["id"] == session_id):
            return session
    raise HTTPException(status_code=404,detail="Session not found.")

#delete session               
@app.delete("/sessions/{session_id}")
def delete_session(
    session_id :int, 
    current_user = Depends(get_current_user)):
    for session in activity_sessions:
        if (session["user_id"] == current_user["id"]) and (session["id"] == session_id):
            activity_sessions.remove(session)
            return {
                "message" : "Success."
            }
    raise HTTPException(status_code=404,detail="Session not found.")

#XP / Point Summary
@app.get("/xp/summary")
def get_xp_summary(
    current_user = Depends(get_current_user)):

    total_points = 0
    total_sessions = 0

    bonus_intervals_total = 0
    main_goal_completed_total = 0
    legal_goal_completed_total = 0

    for session in activity_sessions:
        if (session["user_id"] == current_user["id"]):
            total_points += session["points_earned"]
            total_sessions +=1
            if session["legal_goal_completed"]:
                legal_goal_completed_total+=1
            if session["main_goal_completed"]:
                main_goal_completed_total +=1
            if session ["bonus_intervals"]:
                bonus_intervals_total += session["bonus_intervals"]

    return {
        "user_id" : current_user["id"],
        "total_points" : total_points,
        "total_sessions" : total_sessions,
        "legal_goal_completed_total": legal_goal_completed_total,
        "main_goal_completed_total": main_goal_completed_total,
        "bonus_intervals_total" : bonus_intervals_total
    }

#XP / Points by Activity Type
@app.get("/xp/by-activity")
def get_xp_by_activity(
    current_user = Depends(get_current_user)):
    xp_by_activity = {}
    for session in activity_sessions:
        if (session["user_id"] == current_user["id"]):
            if session["activity_name"] in xp_by_activity:
                xp_by_activity[session["activity_name"]] += session["points_earned"]
            else:
                xp_by_activity[session["activity_name"]] = session["points_earned"]
    return {
        "user_id": current_user["id"],
        "xp_by_activity": xp_by_activity
    }

        
#XP / Points by Activity ID
@app.get("/xp/by-activity/{activity_id}")
def get_xp_by_activity_id(
    activity_id:int,
    current_user = Depends(get_current_user)):
    xp_by_activity_id = 0
    for session in activity_sessions:
        if (sessions["user_id"] == current_user["id"]):
            if session["activity_id"] == activity_id:
                xp_by_activity_id+=session["points_earned"]
    return {
        "user_id": current_user["id"],
        "activity_id": activity_id,
        "total_points": xp_by_activity_id
    }

#Create goal
@app.post("/goals")
def create_goal(
    incoming_goal_data: GoalCreate,
    current_user = Depends(get_current_user)):
    
    new_goal = {
        "id" : len(goals)+1,
        "user_id" : current_user["id"],
        "progress_value": 0,
        "is_completed" : False,

        **incoming_goal_data.model_dump()
    }
    goals.append(new_goal)

    return new_goal
    
#See all goals
@app.get("/goals")
def get_goals(current_user = Depends(get_current_user)):#require the current logged-in user
    user_goals = []
    
    for goal in goals:
        if (goal["user_id"] == current_user["id"]):
            user_goals.append(goal)

    return user_goals


#Delete Goal
@app.delete("/goals/{goal_id}")
def delete_goal(
    goal_id : int,
    current_user = Depends(get_current_user)):
    for goal in goals:
        if goal["user_id"] == current_user["id"] and goal["id"] == goal_id:
            goals.remove(goal)
            return {
                "message": "Success."
            }
    raise HTTPException(status_code=404,detail="Goal Not Found.")



#See All progress
@app.get("/goals/progress")
def get_goals_progress(current_user = Depends(get_current_user)):
    total_xp = 0
    total_sessions = 0
    legal_goals_completed = 0
    main_goals_completed = 0
    bonus_intervals = 0

    for session in activity_sessions:
        if (session["user_id"] == current_user["id"]):
            total_xp += session["points_earned"]
            total_sessions +=1

            if session["legal_goal_completed"]:
                legal_goals_completed+=1

            if session["main_goal_completed"]:
                main_goals_completed +=1

            bonus_intervals += session["bonus_intervals"]
    stats = {
        "total_xp" : total_xp,
        "total_sessions" : total_sessions,
        "legal_goals_completed": legal_goals_completed,
        "main_goals_completed": main_goals_completed,
        "bonus_intervals" : bonus_intervals
    }

    updated_goals = []
    for goal in goals:
        if goal["user_id"] == current_user["id"]:
            target_type = goal["target_type"]
            if target_type in stats:
                goal["progress_value"] = stats[target_type]
            if goal["progress_value"] >= goal["target_value"]:
                goal["is_completed"] = True
            else:
                goal["is_completed"] = False
            updated_goals.append(goal)

    return updated_goals



#Goal Rewards
@app.get("/goals/rewards-summary")
def get_rewards_summary(current_user = Depends(get_current_user)):
    completed_goal_count = 0
    reward_points_earned = 0
    completed_goals = []

    for goal in goals:
        if goal["user_id"] == current_user["id"]:
            if goal["is_completed"]:
                completed_goal_count+=1
                rewards_points_earned += goal["rewards_points"]
                completed_goals.append(goal)
    return {
        "user_id" : current_user["id"],
        "completed_goals" : completed_goals,
        "reward_points_earned": reward_points_earned,
        "completed_goal_count": completed_goal_count
    }

            
#Goal Progress by ID

@app.get("goals/{goals_id}/progress")
def get_goal_progress_by_id(goal_id: int,
    current_user = Depends(get_current_user)):
    for goal in goals:
        if goal["user_id"] == current_user["id"] and goal["id"] == goal_id:
            return {
                "goal_id": goal["id"],
                "title": goal["title"],
                "progress_value" : goal["progress_value"],
                "target_value": goal["target_value"],
                "is_completed": goal["is_completed"]
            }

    raise HTTPException(status_code=404,detail="Goal Not Found.")

#Find Goal by ID
@app.get("/goals/{goal_id}")
def get_goals_by_id(
    goal_id: int,
    current_user = Depends(get_current_user)):
    for goal in goals:
        if goal["user_id"] == current_user["id"] and goal["id"] == goal_id:
            return goal
    raise HTTPException(status_code=404,detail="Goal Not Found.")

#PHASE 5: REWARDS STORE
#@app.post("/rewards")
#def create_reward

#get reward by id

# delete reward

# rewards balance

#redeem reward


#PHASE 5.5 TESTING EVERYTHING I COULDNT TEST LOL