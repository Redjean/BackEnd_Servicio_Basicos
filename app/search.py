from .modelsSB import BillsModel, SearchModel
from .databaseSB import facturas_luz_collection, facturas_agua_collection, facturas_internet_collection, facturas_telefono_collection
from datetime import datetime, timedelta
import random

#Funciones auxiliares
def get_first_and_last_day(date: datetime):
    date = date.date()

    first_day = date.replace(day=1)

    next_month = first_day.replace(day=28) + timedelta(days=4)
    first_day_next_month = next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)
    
    first_day = first_day.isoformat()
    last_day = last_day.isoformat()
    return first_day, last_day

def getCollection(params:str):
    if params == "0":
        return facturas_luz_collection
    elif params == "1":
        return facturas_agua_collection
    elif params == "2":
        return facturas_internet_collection
    elif params == "3":
        return facturas_telefono_collection

async def generateNumInvoice(collection):
    randomNumber = random.randint(1000000000, 9999999999)  # 10 dígitos
    #Verificar si el número de contrato existe
    result = await collection.find_one({"contract": randomNumber})
    print(result)
    if result is None:
        print(randomNumber)
        return randomNumber
    else:
        generateNumInvoice(collection)

#Funciones que toman los end-points
#GET search_bill
async def search_bill(search: str):
    key_to_remove = ["_id", "status", "type"]
    if "_" in search:
        splitResult = search.split("_")
        if len(splitResult) == 2:
            contract, params = splitResult
            contract = int(contract)
        else:
            return ({"code": "formato no válido"})
        collection = getCollection(params)
        result = await collection.find_one({"account": contract})
        if not result: 
            return ({"code": "No existe cuenta pendiente"})
        else: 
            if result.get("status") == "Pendiente":
                for key in key_to_remove:
                    del result[key]
            return result
    else:
        return({"code": "formato no válido"})

#POST set_bill
async def set_bills(bill_data: BillsModel):
    
    today = datetime.now()
    start_date, end_date = get_first_and_last_day(today)
    bill_data.start_date = start_date
    bill_data.expired_date = end_date

    if bill_data.type == "luz":
        bill_data.account = await generateNumInvoice(facturas_luz_collection)
        bill_dict = bill_data.dict(by_alias=True)
        result = await facturas_luz_collection.insert_one(bill_dict)
    elif bill_data.type == "agua":
        bill_data.account = await generateNumInvoice(facturas_agua_collection)
        bill_dict = bill_data.dict(by_alias=True)    
        result = await facturas_agua_collection.insert_one(bill_dict)
    elif bill_data.type == "internet":
        bill_data.account = await generateNumInvoice(facturas_internet_collection) 
        bill_dict = bill_data.dict(by_alias=True)    
        result = await facturas_internet_collection.insert_one(bill_dict)
    elif bill_data.type == "telefono":
        bill_data.account = await generateNumInvoice(facturas_telefono_collection)    
        bill_dict = bill_data.dict(by_alias=True)
        result = await facturas_telefono_collection.insert_one(bill_dict)
    else:
        return 400, {"code": "INVALID_INVOICE_TYPE"}

    if result.inserted_id:
        return 200, {"code": "Éxito", "id": str(result.inserted_id)}
    else:
        return 500, {"code": "ERROR_INSERTING"}
