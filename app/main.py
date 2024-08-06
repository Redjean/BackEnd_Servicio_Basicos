from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from .modelsSB import CheckModel, BillsModel
from .search import search_bill
from .pay import get_bill_amount, check_Paid
from .setAndUpdateAccount import set_bills
from bson import ObjectId
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

@app.get("/")
async def message_root ():
    return {'Mensaje':'Back de servicios básicos'}

@app.get("/search_bill/{NumContract_Params}")
async def search_Bill(NumContract_Params:str):
    response = await search_bill(NumContract_Params)
    response = jsonable_encoder(response)
    return JSONResponse(content=response)
    

@app.post("/set_bill", response_model=BillsModel)
async def set_Bill(bill:BillsModel):
    status, response = await set_bills(bill)
    response = jsonable_encoder(response)
    return JSONResponse(status_code=status, content=response)


@app.get("/get_bill_amount/{account_number}/{service_type}")
async def get_Bill_Amount(account_number: int, service_type: str):
    response = await get_bill_amount(account_number, service_type)
    response = jsonable_encoder(response)
    return JSONResponse(content=response)

@app.post("/checkPaid/", response_model=CheckModel)
async def cancel_Bill(check:CheckModel):
    account_number = check.account_number
    service_type = check.type_params
    status, response = await check_Paid(account_number, service_type)
    if "_id" in response and isinstance(response["_id"], ObjectId):
        response["_id"] = str(response["_id"])
    response = jsonable_encoder(response)
    return JSONResponse(status_code=status, content=response)