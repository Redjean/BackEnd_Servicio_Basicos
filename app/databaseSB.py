from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)

try:
    client.admin.command('ping')
    print("Connected")
except ConnectionFailure:
    print("Connection Failed")


database = client.Servicios_Basicos

# Crear colecciones para diferentes tipos de facturas
facturas_luz_collection = database.get_collection("Facturas_Luz")
facturas_agua_collection = database.get_collection("Facturas_Agua")
cuentas_collection = database.get_collection("Cuentas Usuarios")
facturas_internet_collection = database.get_collection("Facturas_Internet")
facturas_telefono_collection = database.get_collection("Facturas_Telefono")
facturas_canceladas_collection = database.get_collection("Facturas_Canceladas")