from database import get_db

import db_models #DB Models

from schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)

from sqlalchemy.orm import Session

from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends)

from auth import (
    hash_password, 
    verify_password, 
    create_access_token, 
    get_current_user)

from fastapi.security import OAuth2PasswordRequestForm


#CREATING APPLICATION
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

#USER & AUTHENTICATION LOGIC

#Register User and generate Hash
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
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
@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)):

    existing_user = db.query(db_models.User).filter(
        db_models.User.email == login_data.email).first()
    if existing_user is None:
        raise HTTPException(status_code=401, detail="Invalid Email or Password.")
    
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
@router.post(
    "/token",
    response_model=TokenResponse
)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(db_models.User).filter(
        db_models.User.email == form_data.username
    ).first()

    if existing_user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password",headers={"WWW-Authenticate": "Bearer"})

    success = verify_password(
        form_data.password,
        existing_user.password_hash
    )

    if not success:
        raise HTTPException(status_code=401, detail="Invalid email or password",headers={"WWW-Authenticate": "Bearer"})

    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#Get Current User Information 
@router.get(
    "/me",
    response_model=UserResponse
)
def read_users_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "username": current_user["username"]
    }