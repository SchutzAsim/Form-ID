from pydantic import BaseModel
from typing import Optional


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