from fastapi import FastAPI
from models import UserRegister
from data import users
from fastapi import HTTPException
from models import UserRegister, UserLogin
from auth import hash_password, verify_password, create_access_token
from fastapi import Depends
from auth import get_current_user

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

@app.get("/users/me")
def read_users_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "username": current_user["username"]
    }
