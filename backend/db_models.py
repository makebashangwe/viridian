from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True)
    email = Column (String, unique = True, index = True, nullable = False)
    username = Column(String, unique = True, index = True, nullable = False)
    password_hash = Column(String, nullable = False)

'''class Activities(Base):
    __tablename__ = "activities"
    id = Column

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
'''