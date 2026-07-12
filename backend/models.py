from pydantic import BaseModel
from typing import Optional

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

class ActivityRuleChange(BaseModel):
    name: Optional[str] = None
    difficulty_rank:Optional[int] = None
    legal_minutes:Optional[int] = None
    legal_points:Optional[float] = None
    goal_minutes:Optional[int] = None
    goal_points:Optional[float] = None
    bonus_interval_minutes :Optional[int] = None
    bonus_points : Optional[float] = None
    max_session_minutes: Optional[int] = None
    default_location: Optional[str] = None

class ActivitySessionCreate(BaseModel):
    activity_rule_id: int
    duration_minutes: int
    location: str
    notes: str | None = None

class GoalCreate(BaseModel):
    title: str 
    description: str
    target_type: str  #ex. "points_earned"
    target_value: float #ex. 30
    reward_points: float #ex. 5
    activity_rule_id: int | None = None

class RewardCreate(BaseModel):
    name: str
    description: str
    tag: str
    point_cost: float
    estimated_cost: float
    image_url: str | None = None
    is_locked: bool = False
    required_goal_id: int | None = None
