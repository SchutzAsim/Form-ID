from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
import os
import mariadb
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from app.model.model import AllUsersEntity, AllUsersEntitys
from app.schema.schema import Token, TokenData, User, NewUser
from app.databases.db import conn, cursor

# DataBase Table Selection
user_table = 'users' if int(os.getenv("SERVER_PORT")) == 8181 else 'test_user'

# Load Secrets
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALOGRITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# Authentication Router
auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Hashed Password Instance
password_hashed = PasswordHash.recommended()


# Store Requested User with password
class UserInDB(User):
    hashed_password: str


# Password Hashing for DB
def PasswordHashing(password):
    PasswordHashedKey = password_hashed.hash(password)
    return PasswordHashedKey



# All Users Dict list
def UserManager():
    # Select Query
    get_user_query = f"SELECT * FROM {user_table}"

    # Execute Query
    cursor.execute(get_user_query)
    userdata = cursor.fetchall()

    # commit data
    conn.commit()

    # list of all users
    AllUsers = AllUsersEntitys(userdata)

    # Dict of user by username
    AllUsersDict = {}
    for one in AllUsers:
        AllUsersDict.update({one["username"]: one})
    return AllUsersDict


# Varify user password
def verify_password(plain_password, hashed_password):
    return password_hashed.verify(plain_password, hashed_password)

# convert user password to hashed password for verification
def get_password_hashed(password):
    return password_hashed.hash(password)

# Get Correct User if Available in UserData
def register_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Decode user's given token
def register_decode_token(token):
    user = register_user(UserManager(), token)
    return user


# Authenticate User Credentials
def authenticate_user(fake_db, username: str, password: str):
    user = register_user(fake_db, username)

    if not user:
        # verify_password(password, user.hashed_password)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=2)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encode_jwt

# Return Requested User if Authorized
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
       user = register_user(UserManager(), username=token_data.username)
       if user is None:
           raise Credentials_exception
       return user

# Return Current User Active or Not
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


@auth_router.post('/new/user')
async def NewUser(FormData: NewUser):
    if FormData.username in UserManager():
        raise HTTPException(status_code=409, detail="Pick Another Username")

    try:
        # Making Hashed Password
        HashedPassword = PasswordHashing(FormData.hashed_password)

        # New User Insertion Query
        inser_query = f"INSERT INTO {user_table} (username, hashed_password, email, disabled, created_at) VALUES ('{FormData.username}', '{HashedPassword}', '{FormData.email}', '{FormData.disabled}', Default)"

        # Execeute Query
        cursor.execute(inser_query)

        return JSONResponse(content=f"User {FormData.username} Added Successfully!", status_code=201)
    except mariadb.Error as err:
        raise HTTPException(status_code=400, detail=f"User {FormData.username} insertion failed! with error {err}")

    finally:
        conn.commit()
        UserManager()


@auth_router.get("/all/users")
async def AllUsers(current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        allusers = UserManager()
        return JSONResponse(status_code=200, content=allusers)

    except mariadb.Error as e:
        raise HTTPException(status_code=404, detail="Users Not Found!")
    finally:
        conn.commit()


@auth_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(UserManager(), form_data.username, form_data.password)
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



@auth_router.get("/user/me")
async def read_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user