from .databaseSB import facturas_luz_collection, facturas_agua_collection, facturas_internet_collection, facturas_telefono_collection

#Funciones Auxiliares
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
                    if key in result:
                        del result[key]
                return result
            else:
                return ({"code": "Cuenta no está pendiente"})
    else:
        return({"code": "formato no válido"})



