#IMPORTS
from database import engine, get_db
import db_models
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from data import rewards, reward_redemptions #Fake DBs
from models import UserRegister, UserLogin, ActivityRuleCreate, ActivityRuleChange, ActivitySessionCreate, GoalCreate, RewardCreate
from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


#CREATING APPLICATION
app = FastAPI()
db_models.Base.metadata.create_all(bind=engine) #SQL Alchemy checks models and creates the matching DB tables if they do not already exist!

@app.get("/")
def read_root():
    return {"message" : "Viridian API is running"}

#USER & AUTHENTICATION LOGIC

#Register User and generate Hash
@app.post("/auth/register")
def register_user(
    incoming_user: UserRegister,
    db: Session = Depends(get_db)): #Open DB (connection/Session to Postgres). When it's done, close it.

    #Checking if email exists -> bool
    existing_email = db.query(db_models.User).filter( #Look inside the users table, filter it by email
        db_models.User.email == incoming_user.email).first() #Find the first user where the email matches the incoming email.

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
   
   #Checking if username exists -> bool
    existing_user = db.query(db_models.User).filter(
        db_models.User.username == incoming_user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = hash_password(incoming_user.password)
    
    new_user = db_models.User(
    email=incoming_user.email,
    username=incoming_user.username,
    password_hash=hashed_password
    )

    db.add(new_user) #Add this new user into the database
    db.commit() #save the new user into Postgres
    db.refresh(new_user) #reload this object with the final saved DB row

    return {"id": new_user.id, 
            "email" : new_user.email, 
            "username" : new_user.username
            }


#Authentication Logic
@app.post("/auth/login")
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)):

    existing_user = db.query(db_models.User).filter(
        db_models.User.email == login_data.email).first()
    if existing_user is None:
        raise HTTPException(status_code=401, detail="Invalid Username")
    
    success = verify_password(
                login_data.password, 
                existing_user.password_hash)

    if not success:
        raise HTTPException(status_code=401, detail="Invalid Email or Password.")

    access_token = create_access_token(data={"sub": existing_user.email}) #who the token belongs to
                
    return {
            "access_token" : access_token,
            "token_type" : "bearer",
        }
            

#For Swagger OAuth Testing
@app.post("/auth/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(db_models.User).filter(
        db_models.User.email == form_data.username
    ).first()

    if existing_user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    success = verify_password(
        form_data.password,
        existing_user.password_hash
    )

    if not success:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#Get Current User Information 
@app.get("/users/me")
def read_users_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "username": current_user["username"]
    }
#------------------------------------------------------------------------------

#ACTIVITY RULE LOGIC  [Status: Testing]

@app.post("/activities")
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
@app.get("/activities")
def get_activity_rules(
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    activities = db.query(db_models.ActivityRule).filter(db_models.ActivityRule.user_id == current_user["id"]).all()
    return activities

#Get by Activity ID
@app.get("/activities/{activity_id}")
def get_activity_by_id(
    activity_id :int, 
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):

    target_activity_rule = db.query(db_models.ActivityRule).filter(db_models.ActivityRule.user_id == current_user["id"]).filter(db_models.ActivityRule.id == activity_id).first()
    if target_activity_rule == None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found.")
    
    return target_activity_rule


#Edit Activity By ID
@app.patch("/activities/{activity_id}")
def edit_activity_by_id(
    activity_id :int,
    updated_activity_rule : ActivityRuleChange,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    target_activity_rule = db.query(db_models.ActivityRule).filter(db_models.ActivityRule.user_id == current_user["id"]).filter(db_models.ActivityRule.id == activity_id).first()
    if target_activity_rule == None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found.")
    updated_data = updated_activity_rule.model_dump(exclude_unset=True) #takes out the NONE values and converts to a dict
    for key,value in updated_data.items():
        setattr(target_activity_rule,key,value)
    db.commit()
    db.refresh(target_activity_rule)

    return target_activity_rule

'''
#ARCHIVE: An Activity RULE cannot be physically deleted while Session References it...          

@app.delete("/activities/{activity_id}")
def delete_activity(
    activity_id :int,
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)
    ):
    target_activity_rule = db.query(db_models.ActivityRule).filter(db_models.ActivityRule.user_id == current_user["id"]).filter(db_models.ActivityRule.id == activity_id).first()
    
    if target_activity_rule == None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found.")
    
    db.delete(target_activity_rule)
    db.commit()

    return {
            "message" : "Success."
        }
'''

#------------------------------------------------------------------------------
#SESSION LOGIC 

#create session
@app.post("/sessions")
def create_activity_session(
    incoming_session: ActivitySessionCreate,#take in activity session data
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)):

    '''
    PLEASE NOTE THE DIFFERENCE! 
    ActivityRule is the configurations for the Individual Session based on parameters specified in the ActivityRule Object.
        
    class ActivitySession(Base):
    __tablename__="sessions"
    id = Column(Integer, primary_key = True, index = True)
    activity_rule_id = Column (Integer, index=True, nullable = False)
    user_id = Column(Integer, index=True, nullable = False)
    ...

    '''
    #find the matching activity rule information
    matching_activity_rule = db.query(db_models.ActivityRule).filter(
        db_models.ActivityRule.user_id == current_user["id"]).filter(
        db_models.ActivityRule.id == incoming_session.activity_rule_id
        ).first()

    if matching_activity_rule is None:
        raise HTTPException(status_code=404,detail="Activity Rule Not Found")
    
    if incoming_session.duration_minutes > matching_activity_rule.max_session_minutes : #Prevent 48 hour sessions lol
        raise HTTPException(status_code = 400, detail="Session exceeds max allowed minutes")

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
@app.get("/sessions")
def get_sessions(
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)):
    
    user_sessions = db.query(db_models.ActivitySession).filter(db_models.ActivitySession.user_id==current_user["id"]).all()
    
    return user_sessions
   
    
#Return by Session ID
@app.get("/sessions/{session_id}")
def get_session_by_id(
    session_id :int, 
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    target_session = db.query(db_models.ActivitySession).filter(db_models.ActivitySession.user_id==current_user["id"]).filter(db_models.ActivitySession.id == session_id).first()
    if target_session == None:
        raise HTTPException(status_code=404,detail="Session not found.")
    
    return target_session

#delete session               
@app.delete("/sessions/{session_id}")
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
        "message": f"Successfully deleted Session #{session_id}"
    }

#------------------------------------------------------------------------------
#XP / POINTS LOGIC 

#XP / Point Summary
@app.get("/xp/summary")
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
@app.get("/xp/by-activity")
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
    if target_activity is None:
        raise HTTPException(
            status_code=404,
            detail="No Activity Rules Found."
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
@app.get("/xp/by-activity/{activity_rule_id}")
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
@app.get("/xp/by-session/{session_id}")
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

#------------------------------------------------------------------------------
#GOAL LOGIC  

#Create goal
@app.post("/goals")
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
@app.get("/goals")
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
@app.delete("/goals/{goal_id}")
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

#See All Updated Goal Progress
@app.get("/goals/progress")
def get_goals_progress(
    current_user = Depends(get_current_user),
    db:Session = Depends(get_db)):
    
    goals = update_user_goal_progress(current_user["id"],db)
    
    return goals


#Goal Rewards
@app.get("/goals/rewards-summary")
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
@app.get("/goals/{goal_id}/progress")
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
@app.get("/goals/{goal_id}")
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

#------------------------------------------------------------------------------
#REWARDS STORE LOGIC [Status: Changes Underway]
#HELPER FUNCTIONS 
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

#Create Reward
@app.post("/rewards")
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
@app.get("/rewards")
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
@app.get("/rewards/balance")
def get_reward_balance(
    current_user=Depends(get_current_user),
    db:Session = Depends(get_db)):
    
    user_balance_info = get_user_balance(current_user["id"],db)
    
    return user_balance_info

#Redeem by Reward ID
@app.post("/rewards/{reward_id}/redeem")
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
@app.get("/rewards/{reward_id}")
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
@app.delete("/rewards/{reward_id}")
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