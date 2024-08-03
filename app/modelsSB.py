from pydantic import BaseModel, EmailStr
from typing import Optional, List
from typing import Union
from datetime import datetime

class BillsModel(BaseModel):
    invoice: int
    ci:str
    name: str
    email: EmailStr
    amount: float
    type: str
    status: str
    Address: str
    start_date: str
    expired_date: str

class SearchModel(BaseModel):
    ci: str