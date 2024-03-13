from sqlalchemy.dialects import sqlite
from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Date, Computed, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


db_url = "sqlite:///minstroy.db"
engine = create_engine(db_url)

class Base(DeclarativeBase):
    pass

class Urls(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    tags = Column(JSON)
    url = Column(String, nullable=False)



# alembic init alembic
    # alembic/env.py # ----    

# alembic revision --autogenerate -m "first revision"
# alembic upgrade head