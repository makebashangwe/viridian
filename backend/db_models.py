from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    #Keys
    id = Column(Integer, primary_key=True,index=True)
    
    #Other Attributes
    email = Column (String, unique = True, index = True, nullable = False)
    username = Column(String, unique = True, index = True, nullable = False)
    password_hash = Column(String, nullable = False)
    
    #Relationships
    activity_rules = relationship("ActivityRule", 
                                  back_populates="user"
                                  )
    activity_sessions = relationship("ActivitySession", 
                                     back_populates="user"
                                     )
    goals = relationship("Goal", 
                        back_populates="user"
                        )
    
class ActivityRule(Base):
    __tablename__ = "activity_rules"

    #Keys
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable = False)
    
    #Other Attributes
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

    #Relationships
    user = relationship("User",
                        back_populates = "activity_rules"
                        )
    
    activity_sessions = relationship("ActivitySession", 
                                     back_populates = "activity_rule"
                                     )
    goals = relationship("Goal",
                        back_populates="activity_rule"
                        )
    
class ActivitySession(Base): #Using ActivitySession to prevent name conflict with db: Session
    __tablename__="sessions"

    #Keys
    id = Column(Integer, primary_key = True, index = True)
    activity_rule_id = Column(Integer, ForeignKey("activity_rules.id"),index=True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable = False)

    #Other Attributes
    activity_name = Column(String, nullable = False)
    duration_minutes = Column(Integer,  nullable = False)
    location = Column(String, nullable=False)
    
    points_earned = Column(Float, nullable=False)
    legal_goal_completed = Column(Boolean, nullable=False)
    main_goal_completed = Column(Boolean, nullable=False)
    bonus_intervals = Column(Integer, nullable =False)
    
    notes = Column(String, nullable=True)
    
    #Relationships
    user = relationship("User", 
                        back_populates="activity_sessions")
    
    activity_rule = relationship("ActivityRule", 
                                  back_populates="activity_sessions"
                                  )

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    activity_rule_id = Column(Integer,ForeignKey("activity_rules.id"),nullable=True,index=True)

    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    target_type = Column(String,nullable=False)
    
    target_value = Column(Float,nullable=False)
    reward_points = Column(Float,nullable=False)
    progress_value = Column(Float,nullable = False,default=0)
    is_completed = Column(Boolean,nullable=False, default= False)

    user = relationship("User",
                        back_populates="goals"
                        )
    
    activity_rule = relationship("ActivityRule",
                                 back_populates="goals"
                                 )