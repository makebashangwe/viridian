from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True)
    email = Column (String, unique = True, index = True, nullable = False)
    username = Column(String, unique = True, index = True, nullable = False)
    password_hash = Column(String, nullable = False)

class ActivityRule(Base):
    __tablename__ = "activity_rules"
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, index=True, nullable = False)

    name = Column (String, index=True, nullable = False,)
    difficulty_rank = Column (Integer, index=True)

    legal_minutes = Column (Integer,  nullable = False)
    legal_points = Column (Float ,  nullable = False)

    goal_minutes  = Column (Integer ,  nullable = False)
    goal_points = Column (Float, nullable = False)

    bonus_interval_minutes =Column (Integer, nullable = False)
    bonus_points = Column (Float, nullable = False)

    max_session_minutes =Column (Integer, index=True)
    default_location = Column(String, nullable=False)
