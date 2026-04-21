from pydantic import BaseModel


# Authenticated User Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class NewUser(BaseModel):
    username: str
    hashed_password: str
    email: str | None = None
    disabled: bool | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


# Data Schema
class CreateLog(BaseModel):
    Name: str
    Contact: str
    Service: str
    Service_Type: str
    Govt_Fee: int
    Service_Charge: int
    Total_Amount: int
    Month: str
    Created_At: str
    Application_ID: str
    Due: int


class UpdateLog(BaseModel):
    id: int
    Name: str
    Contact: str
    Service: str
    Service_Type: str
    Govt_Fee: int
    Service_Charge: int
    Total_Amount: int
    Month: str
    Created_At: str
    Application_ID: str
    Due: int


class UpdateID(BaseModel):
    id: int
    Due: int
