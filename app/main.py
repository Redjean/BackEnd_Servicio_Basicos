from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from .modelsSB import SearchModel, BillsModel
from .search import search_bill, set_bills

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