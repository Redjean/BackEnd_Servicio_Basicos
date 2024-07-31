from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from modelsSB import SearchModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

@app.get("/serch_bill", response_model=SearchModel)
async def serchBill(seach:SearchModel):
    #crear funcion para buscar facturas mediante Ci. carpeta search
    a=1

#@app.post("/pay_bill")