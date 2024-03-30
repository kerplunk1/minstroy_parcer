from fastapi import FastAPI
from datetime import date
from sqlalchemy.orm import Session
from models import engine, Suppliers, ConstructionResources

app = FastAPI()

@app.get("/get_dates")
def get_dates():
    with Session(engine) as session:
        data = session.query(Suppliers.parse_date).distinct()
    result = []
    for date in data:
        result.append(date[0])
    return result


@app.post("/get_ksr")
def get_ksr(date: date):
    with Session(engine) as session:
        data = session.query(ConstructionResources.ksr, ConstructionResources.name).distinct().\
        where(ConstructionResources.parse_date == date)
    result = []
    for ksr, name in data:
        result.append({"ksr": ksr, "name": name})
    return result


@app.post("/get_suppliers")
def get_suppliers(date: date, ksr: str):
    with Session(engine) as session:
        data = session.query(Suppliers.inn, Suppliers.full_name, ConstructionResources.ksr, ConstructionResources.name).\
        join(ConstructionResources, Suppliers.id == ConstructionResources.supplier_id).\
        where(ConstructionResources.ksr == ksr, ConstructionResources.parse_date == date)
    
    result = []
    for supplier_inn, supplier_name, item_ksr, item_name in data:
        result.append({"supplier_inn": supplier_inn,
                       "supplier_name": supplier_name,
                       "item_ksr": item_ksr,
                       "item_name": item_name})
        
    return result
