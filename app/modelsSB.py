from pydantic import BaseModel, EmailStr
from typing import Optional, List
from typing import Union
from datetime import datetime

class BillsModel(BaseModel):
    ci:str
    name: str
    email: EmailStr
    amount: float
    description: str
    status: str
    start_date: Optional[datetime]
    expired_date: Optional[datetime]

class SearchModel(BaseModel):
    ci: str