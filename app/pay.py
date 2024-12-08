from .search import getCollection 
from datetime import datetime
from bson import ObjectId
from .databaseSB import facturas_canceladas_collection
import random

async def generateNum():
    randomNumber = random.randint(1000000000, 9999999999)  # 10 dígitos
    #Verificar si el número de contrato existe
    result = await facturas_canceladas_collection.find_one({"Número de factura": randomNumber})
    print(result)
    if result is None:
        print(randomNumber)
        return randomNumber
    else:
        generateNum()

async def get_bill_amount(account_number: int, service_type: str):
    collection = getCollection(service_type)
    print(collection)
    result = await collection.find_one({"account": account_number})
    if not result:
        return {"code": "No existe cuenta pendiente"}
    elif result.get("status") == "Pendiente":
        return {"monto": result["amount"]}
    else:
        return {"code": "No hay monto pendiente"}

async def check_Paid(account_number: int, service_type: str):
    collection = getCollection(service_type)
    # Buscar la factura pendiente
    result = await collection.find_one({"account": account_number})
    if not result:
        return 200, {"code": "Factura no encontrada"}

    if result.get("status") != "Pendiente":
        return 200, {"code": "La factura no está pendiente"}

    
    result["cancellation_date"] = datetime.now()
    cancellation_date= result["cancellation_date"].date().isoformat()
    num_invoice = await generateNum()

    nueva_factura ={
        "Número de factura": num_invoice,
        "Contrato": result["account"],
        "CI": result["ci"],
        "Tipo de servicio cancelado": result["type"],
        "Fecha de inicio de la planilla": result["start_date"],
        "Fecha de expiración": result["expired_date"],
        "Fecha que se realizó la cancelación": cancellation_date
    }

    # Insertar la factura en la colección de facturas canceladas
    insert_result = await facturas_canceladas_collection.insert_one(nueva_factura)
    if not insert_result.inserted_id:
        return 200, {"code": "Error al registrar nueva factura"}

    # Eliminar la factura original
    delete_result = await collection.delete_one({"account": account_number})
    if delete_result.deleted_count == 0:
        return 200, {"code": "Error al eliminar la factura original"}

    return 200, {"Code": "Pago exitoso y factura registrada"}