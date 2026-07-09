from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    username: str
    password: str      
    
class UserLogin(BaseModel):
    email: str
    password: str
class ActivityRuleCreate(BaseModel):
    name: str
    difficulty_rank:int
    legal_minutes:int
    legal_points:float
    goal_minutes:int
    goal_points:float
    bonus_interval_minutes :int
    bonus_points : float
    max_session_minutes: int
    default_location: str