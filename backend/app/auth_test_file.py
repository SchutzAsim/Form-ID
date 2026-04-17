from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
import os
from fastapi import Depends, HTTPException, FastAPI, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from dotenv import load_dotenv

# Load Secret Key
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALOGRITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hashed = PasswordHash.recommended()
DUMMY_HASHED = password_hashed.hash("secret")


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    hashed_password: str | None = None
    email: str | None = None
    disabled: bool | None = None


def fake_hashed_password(password: str):
    return "schutz" + password


class UserInDB(User):
    hashed_password: str


fake_users_db = {
    "alice": {
        "username": "alice",
        "email": "alice@gmail.com",
        "hashed_password": DUMMY_HASHED,
        "disabled": False
    }
}

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return password_hashed.verify(plain_password, hashed_password)

def get_password_hashed(password):
    return password_hashed.hash(password)


def fake_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = fake_user(fake_users_db, token)
    return user


def authenticate_user(fake_db, username: str, password: str):
    user = fake_user(fake_db, username)
    if not user:
        verify_password(password, DUMMY_HASHED)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encode_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
       Credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
            headers={"WWW-Authenticated": "bearer"}
       )
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           username = payload.get("sub")
           if username is None:
               raise Credentials_exception
           token_data = TokenData(username=username)
       except InvalidTokenError:
           raise Credentials_exception
       user = fake_user(fake_users_db, username=token_data.username)
       if user is None:
           raise Credentials_exception
       return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token =  create_access_token(
        data= {"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type='bearer')



@app.get("/user/me")
async def read_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user