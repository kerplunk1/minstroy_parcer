from sqlalchemy import JSON, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase


db_url = "sqlite:///minstroy.db"
engine = create_engine(db_url)

class Base(DeclarativeBase):
    pass

class Urls(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    tags = Column(JSON)
    url = Column(String, nullable=False)


class Suppliers(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    legal_address = Column(String, nullable=False)
    inn = Column(String, nullable=False)
    ogrn = Column(String)
    ogrnip = Column(String)
    actual_address = Column(String)
    opf_legal = Column(String)
    kpp = Column(String)
    okved2 = Column(String)
    tnved = Column(String)
    transport = Column(String)
    contact = Column(String)
    network = Column(String)


class Warehouses(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(ForeignKey("suppliers.id"))
    name = Column(String)
    address = Column(String)


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(ForeignKey("suppliers.id"))
    okpd2 = Column(String)
    name = Column(String)


class ConstructionResources(Base):
    __tablename__ = "construction_resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(ForeignKey("suppliers.id"))
    ksr = Column(String)
    name = Column(String)
    unit = Column(String)
    capacity = Column(String)


# alembic init alembic
    # edit alembic/env.py # ----    

# alembic revision --autogenerate -m "first revision"
# alembic upgrade head
    