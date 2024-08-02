from .modelsSB import BillsModel, SearchModel
from .databaseSB import facturas_luz, facturas_agua, facturas_internet, facturas_telefono
from datetime import datetime, timedelta

async def search_bill(search: SearchModel):
    collections = [facturas_luz, facturas_agua, facturas_internet, facturas_telefono]
    results = []

    for collection in collections:
        cursor = collection.find({'ci': search.ci})
        results.extend(await cursor.to_list(length=None))

    if not results:
        response = {'code': 'No resultados'}
        return 200, response
    else:
        formatted_results = []
        for bill in results:
            if '_id' in bill:
                del bill['_id']
            formatted_results.append(bill)
        return 200, formatted_results

def get_first_and_last_day(date: datetime):
    first_day = date.replace(day=1)
    next_month = first_day.replace(day=28) + timedelta(days=4)
    first_day_next_month = next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)
    return first_day, last_day

async def set_bills(bill_data: BillsModel):
    today = datetime.now()
    start_date, end_date = get_first_and_last_day(today)
    bill_data.start_date = start_date
    bill_data.expired_date = end_date
    bill_dict = bill_data.dict(by_alias=True)

    if bill_data.type == "luz":
        result = await facturas_luz.insert_one(bill_dict)
    elif bill_data.type == "agua":
        result = await facturas_agua.insert_one(bill_dict)
    elif bill_data.type == "internet":
        result = await facturas_internet.insert_one(bill_dict)
    elif bill_data.type == "telefono":
        result = await facturas_telefono.insert_one(bill_dict)
    else:
        return 400, {"code": "INVALID_INVOICE_TYPE"}

    if result.inserted_id:
        return 200, {"code": "Éxito", "id": str(result.inserted_id)}
    else:
        return 500, {"code": "ERROR_INSERTING"}
