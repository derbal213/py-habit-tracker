from datetime import datetime
from sqlite3.dbapi2 import Timestamp
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from models.base import base_table

class Task(base_table):
    __tablename__: str = "Tasks"
    
    id: Column[int] = Column[int](Integer, primary_key=True)
    name: Column[str] = Column[str](String, nullable=False)
    created_at: Column[Timestamp] = Column[Timestamp](TIMESTAMP, server_default=text(text="CURRENT_TIMESTAMP"))
    description: Column[str] = Column[str](String)
    point_value: Column[int] = Column[int](Integer, server_default=text(text="0"))