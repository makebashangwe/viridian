
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from data import users
from sqlalchemy.orm import Session
from database import get_db
import db_models

#hashing algorithm that knows how to hash and verify that hash, and whether the old one is deprecated.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#uses bcrypt.
SECRET_KEY = "temporary-dev-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") #“Protected routes should expect a Bearer token.”
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")#for Swagger Oauth Testing

#A hash is designed so you can verify a password later, but you cannot easily turn the hash back into the original password.
def hash_password(password: str): #helper function takes in the plain password
    return pwd_context.hash(password) #return the hashed version

def verify_password(plain_password: str, password_hash:str):
    return pwd_context.verify(plain_password,password_hash) #“Does this plain password match this stored hash?”

def create_access_token(data: dict):
    to_encode = data.copy() #makes a copy of the user info we want in the token

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #turns the data into the token string

    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = db.query(db_models.User).filter(
        db_models.User.email == email
    ).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username
    }