from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    model_validator
)
from typing import Literal
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class ActivityRuleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    difficulty_rank: int = Field(ge=1, le=5)

    legal_minutes: int = Field(gt=0)
    legal_points: float = Field(ge=0)

    goal_minutes: int = Field(gt=0)
    goal_points: float = Field(ge=0)

    bonus_interval_minutes: int = Field(gt=0)
    bonus_points: float = Field(ge=0)

    max_session_minutes: int = Field(gt=0)
    default_location: str = Field(min_length=1, max_length=100)
    

    @model_validator(mode="after")
    def validate_minute_order(self):
        if self.legal_minutes > self.goal_minutes:
            raise ValueError(
                "legal_minutes cannot exceed goal_minutes"
            )

        if self.goal_minutes > self.max_session_minutes:
            raise ValueError(
                "goal_minutes cannot exceed max_session_minutes"
            )

        return self


class ActivityRuleChange(BaseModel):
    name: str | None = None
    difficulty_rank: int | None = None

    legal_minutes: int | None = None
    legal_points: float | None = None

    goal_minutes: int | None = None
    goal_points: float | None = None

    bonus_interval_minutes: int | None = None
    bonus_points: float | None = None

    max_session_minutes: int | None = None
    default_location: str | None = None


class ActivitySessionCreate(BaseModel):
    activity_rule_id: int = Field(gt=0)
    duration_minutes: int = Field(gt=0)
    location: str = Field(min_length=1, max_length=100)
    notes: str | None = Field(default=None, max_length=1000)


class GoalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)

    target_type: Literal[
        "total_xp",
        "total_sessions",
        "legal_goals_completed",
        "main_goals_completed",
        "bonus_intervals"
    ]

    target_value: float = Field(gt=0)
    reward_points: float = Field(ge=0)

    activity_rule_id: int | None = Field(
        default=None,
        gt=0
    )


class RewardCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    tag: str = Field(min_length=1, max_length=50)

    point_cost: float = Field(gt=0)
    estimated_cost: float = Field(ge=0)

    image_url: str | None = None
    is_locked: bool = False
    required_goal_id: int | None = Field(
        default=None,
        gt=0
    )

    @model_validator(mode="after")
    def validate_locked_reward(self):
        if self.is_locked and self.required_goal_id is None:
            raise ValueError(
                "Locked rewards require a goal"
            )

        return self
    
class ActivityRuleResponse(BaseModel):
    id: int
    user_id: int

    name: str
    difficulty_rank: int

    legal_minutes: int
    legal_points: float

    goal_minutes: int
    goal_points: float

    bonus_interval_minutes: int
    bonus_points: float

    max_session_minutes: int
    default_location: str
    is_active : bool

    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ActivitySessionResponse(BaseModel):
    id : int
    activity_rule_id: int 
    user_id : int
    activity_name : str
        
    points_earned : float
    legal_goal_completed  : bool
    main_goal_completed  : bool
    bonus_intervals : int
    duration_minutes: int

    location: str
    notes: str | None

    model_config = {
        "from_attributes" : True
    }

class XPSummaryResponse(BaseModel):
    user_id : int
    total_points : float
    total_sessions : int
    legal_goal_completed_total : int
    main_goal_completed_total : int
    bonus_intervals_total : int

class XPByActivityResponse(BaseModel):
    user_id: int
    xp_by_activity: dict[str, float]

class XPByActivityIdResponse(BaseModel):
    user_id :int 
    activity_rule_id : int
    total_points :float

class XPBySessionIdResponse(BaseModel):
    user_id : int
    session_id : int
    total_points :float


class GoalResponse(BaseModel):
    id : int
    activity_rule_id :int | None
    user_id: int
    
    title : str
    description :str
    target_type : str
    
    target_value : float
    reward_points : float
    progress_value : float
    is_completed : bool

    model_config = {
        "from_attributes" : True
    }
    

class GoalProgressResponse(BaseModel):
    goal_id : int
    title: str
    progress_value: float
    target_value:  float
    is_completed : bool


class MessageResponse(BaseModel):
    message : str

class GoalRewardsSummaryResponse(BaseModel):
    user_id : int
    completed_goals: list[GoalResponse]
    reward_points_earned: float
    completed_goal_count :  int

class RewardResponse(BaseModel):
    id : int
    user_id :int
    required_goal_id : int | None

    name : str
    description : str
    tag : str
    point_cost : float
    estimated_cost : float
    is_locked: bool
    image_url :str | None

    model_config = {
    "from_attributes" : True
    }

class RewardBalanceResponse(BaseModel):
    user_id :int
    reward_points_earned : float
    reward_points_spent: float
    available_balance: float


class RewardRedemptionResponse(BaseModel):
    id : int
    user_id :int
    reward_id : int | None

    reward_name : str
    point_cost: float
    redeemed_at: datetime

    model_config = {
    "from_attributes" : True
    }

class ArchiveRewardResponse(BaseModel):
    message: str
    archive_id:int