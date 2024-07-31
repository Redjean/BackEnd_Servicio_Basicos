from pydantic import BaseModel, EmailStr
from typing import Optional, List
from typing import Union

class BillsModel(BaseModel):
    ci:str
    name: str
    email: EmailStr
    amount: float
    description: str
    status: str

class SearchModel(BaseModel):
    ci: str