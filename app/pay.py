from .search import getCollection
from datetime import datetime
from bson import ObjectId
from .databaseSB import facturas_canceladas_collection
def FormatIso(date: datetime): #Entrada: datetime  Salida: str
    date = date.date()
    date = date.isoformat()
    return date

async def get_bill_amount(account_number: int, service_type: str):
    collection = getCollection(service_type)
    result = await collection.find_one({"account": account_number})
    if not result:
        return 200, {"code": "No existe cuenta pendiente"}
    elif result.get("status") == "Pendiente":
        return 200, {"monto": result["amount"]}
    else:
        return 200, {"code": "No hay monto pendiente"}

async def check_Paid(account_number: int, service_type: str):
    collection = getCollection(service_type)

    # Buscar la factura pendiente
    result = await collection.find_one({"account": account_number})
    if not result:
        return 200, {"code": "Factura no encontrada"}

    if result.get("status") != "Pendiente":
        return 200, {"code": "La factura no está pendiente"}

    
    result["cancellation_date"] = datetime.now()
    result["cancellation_date"] = result["cancellation_date"].date().isoformat()


    result["_id"] = str(result["_id"])

    # Insertar la factura en la colección de facturas canceladas
    insert_result = await facturas_canceladas_collection.insert_one(result)
    if not insert_result.inserted_id:
        return 200, {"code": "Error al mover"}

    # Eliminar la factura original
    delete_result = await collection.delete_one({"account": account_number})
    if delete_result.deleted_count == 0:
        return 200, {"code": "Error al eliminar la factura original"}

    return 200, result