from .search import getCollection
from datetime import datetime

def FormatIso(date: datetime): #Entrada: datetime  Salida: str
    date = date.date()
    date = date.isoformat()
    return date

async def get_bill_amount(account_number: str, service_type: str):
    collection = getCollection(service_type)
    result = await collection.find_one({"account": account_number})
    if not result:
        return 200, {"code": "No existe cuenta pendiente"}
    elif result.get("status") == "Pendiente":
        return 200, {"monto": result["amount"]}
    else:
        return 200, {"code": "No hay monto pendiente"}
