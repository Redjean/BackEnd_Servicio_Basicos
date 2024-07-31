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

bills_collection = database.get_collection("Facturas")