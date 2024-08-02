from .modelsSB import BillsModel, SearchModel
from .databaseSB import facturas_luz_collection, facturas_agua_collection, facturas_internet_collection, facturas_telefono_collection
from datetime import datetime, timedelta

#Funciones auxiliares
def get_first_and_last_day(date: datetime):
    first_day = date.replace(day=1)
    next_month = first_day.replace(day=28) + timedelta(days=4)
    first_day_next_month = next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)
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

#Funciones que toman los end-points
#GET search_bill
async def search_bill(search: str):
    results = []
    formatted_results = []
    key_to_remove = ["_id", "status", "type"]
    if "_" in search:
        splitResult = search.split("_")
        if len(splitResult) == 2:
            ci, params = splitResult
        else:
            formatted_results.append({"code": "formato no válido"})
            return formatted_results
        collection = getCollection(params)            
        cursor = collection.find({'ci': ci})
        results.extend(await cursor.to_list(length=None))
        if not results:
            formatted_results.append({"code": "No existen facturas pendientes"})
            return formatted_results
        else:
            for bill in results:
                if bill.get('status') == "Pendiente":
                    for key in key_to_remove:
                        if key in bill:
                            del bill[key]
                    formatted_results.append(bill)
            return formatted_results
    else: 
        formatted_results.append({"code": "formato no válido"})
        return formatted_results

#POST set_bill
async def set_bills(bill_data: BillsModel):
    today = datetime.now()
    start_date, end_date = get_first_and_last_day(today)
    bill_data.start_date = start_date
    bill_data.expired_date = end_date
    bill_dict = bill_data.dict(by_alias=True)

    if bill_data.type == "luz":
        result = await facturas_luz_collection.insert_one(bill_dict)
    elif bill_data.type == "agua":
        result = await facturas_agua_collection.insert_one(bill_dict)
    elif bill_data.type == "internet":
        result = await facturas_internet_collection.insert_one(bill_dict)
    elif bill_data.type == "telefono":
        result = await facturas_telefono_collection.insert_one(bill_dict)
    else:
        return 400, {"code": "INVALID_INVOICE_TYPE"}

    if result.inserted_id:
        return 200, {"code": "Éxito", "id": str(result.inserted_id)}
    else:
        return 500, {"code": "ERROR_INSERTING"}
