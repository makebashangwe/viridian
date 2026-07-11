from sqlalchemy import Column, Integer, String, Float, Boolean
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

class Sessions(Base): #Using plural to prevent name conflict with db: Session
    __tablename__="sessions"
    id = Column(Integer, primary_key = True, index = True)
    activity_rule_id = Column (Integer, index=True, nullable = False)
    user_id = Column(Integer, index=True, nullable = False)

    activity_name = Column(String, nullable = False)
    duration_minutes = Column(Integer,  nullable = False)
    location = Column(String, nullable=False)
    
    points_earned = Column(Float, nullable=False)
    legal_goal_completed = Column(Boolean, nullable=False)
    main_goal_completed = Column(Boolean, nullable=False)
    bonus_intervals = Column(Integer, nullable =False)
    
    notes = Column(String, nullable=True)
