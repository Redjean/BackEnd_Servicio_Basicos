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
facturas_luz = database.get_collection("Facturas_Luz")
facturas_agua = database.get_collection("Facturas_Agua")
facturas_internet = database.get_collection("Facturas_Internet")
facturas_telefono = database.get_collection("Facturas_Telefono")