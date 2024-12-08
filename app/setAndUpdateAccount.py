from datetime import datetime, timedelta
import random
from .modelsSB import BillsModel
from .databaseSB import facturas_luz_collection, facturas_agua_collection, facturas_internet_collection, facturas_telefono_collection, cuentas_collection


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

async def generateNum(collection):
    randomNumber = random.randint(1000000000, 9999999999)  # 10 dígitos
    #Verificar si el número de contrato existe
    result = await collection.find_one({"contract": randomNumber})
    print(result)
    if result is None:
        print(randomNumber)
        return randomNumber
    else:
        generateNum(collection)

async def insertAccount(facturas):
    cuenta= {
        "Número de cuenta":facturas.get("account"),
        "Ci":facturas.get("ci"),
        "Nombre del usuario": facturas.get("name"),
        "Servicio": facturas.get("type") 
    }
    result = await cuentas_collection.insert_one(cuenta)
    if result.inserted_id:
        return True

#POST set_bill
async def set_bills(bill_data: BillsModel):
    
    today = datetime.now()
    start_date, end_date = get_first_and_last_day(today)
    bill_data.start_date = start_date
    bill_data.expired_date = end_date

    if bill_data.type == "luz":
        bill_data.account = await generateNum(facturas_luz_collection)
        bill_dict = bill_data.dict(by_alias=True)
        result = await facturas_luz_collection.insert_one(bill_dict)
    elif bill_data.type == "agua":
        bill_data.account = await generateNum(facturas_agua_collection)
        bill_dict = bill_data.dict(by_alias=True)    
        result = await facturas_agua_collection.insert_one(bill_dict)
    elif bill_data.type == "internet":
        bill_data.account = await generateNum(facturas_internet_collection) 
        bill_dict = bill_data.dict(by_alias=True)    
        result = await facturas_internet_collection.insert_one(bill_dict)
    elif bill_data.type == "telefono":
        bill_data.account = await generateNum(facturas_telefono_collection)    
        bill_dict = bill_data.dict(by_alias=True)
        result = await facturas_telefono_collection.insert_one(bill_dict)
    else:
        return 400, {"code": "INVALID_INVOICE_TYPE"}
    add_new_account = await insertAccount(bill_dict)
    if result.inserted_id and add_new_account:
        return 200, {"code": "Éxito", "id": str(result.inserted_id)}
    else:
        return 500, {"code": "ERROR_INSERTING"}

