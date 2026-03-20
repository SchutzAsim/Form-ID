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
    Name: str | None = None
    Contact: str | None = None
    Service: str | None = None
    Service_Type: str | None = None
    Govt_Fee: int | None = None
    Service_Charge: int | None = None
    Total_Amount: int | None = None
    Month: str | None = None
    Created_At: str | None = None
    Application_ID: str | None = None
    Due: int | None = None
