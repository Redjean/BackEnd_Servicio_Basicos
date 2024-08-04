from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from .modelsSB import SearchModel, BillsModel
from .search import search_bill, set_bills
from .pay import get_bill_amount, check_Paid
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
async def searchBill(NumContract_Params:str):
    response = await search_bill(NumContract_Params)
    response = jsonable_encoder(response)
    return JSONResponse(content=response)
    

@app.post("/set_bill", response_model=BillsModel)
async def setBill(bill:BillsModel):
    status, response = await set_bills(bill)
    response = jsonable_encoder(response)
    return JSONResponse(status_code=status, content=response)


@app.get("/get_bill_amount/{account_number}/{service_type}")
async def getBillAmount(account_number: int, service_type: str):
    status, response = await get_bill_amount(account_number, service_type)
    response = jsonable_encoder(response)
    return JSONResponse(status_code=status, content=response)

@app.delete("/checkPaid/{account_number}/{service_type}")
async def cancelBill(account_number: int, service_type: str):
    status, response = await check_Paid(account_number, service_type)
    if "_id" in response and isinstance(response["_id"], ObjectId):
        response["_id"] = str(response["_id"])
    response = jsonable_encoder(response)
    return JSONResponse(status_code=status, content=response)