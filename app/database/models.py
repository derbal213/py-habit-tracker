import logging
from .db_consts import SessionLocal, days_of_week
from datetime import datetime, timezone
from typing import override
from pydantic import StrictInt
from sqlmodel import SQLModel, Field, CheckConstraint, Column, VARCHAR, DateTime, text
from sqlalchemy.exc import IntegrityError

class BaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def upsert(self) -> None:
        try:
            with SessionLocal() as session:
                session.add(self)
                session.commit()
                session.refresh(self)
        except IntegrityError as ie:
            logging.warning(f"Integrity error while upserting {self}. Error: {ie}")
            raise
    
class Task(BaseModel, table=True):    
    name: str = Field(sa_column=Column("name", VARCHAR, unique=True, index=True, nullable=False))
    description: str|None = None
    point_value: StrictInt = Field(default=0, nullable=False)
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("(CURRENT_TIMESTAMP)"),
            server_onupdate=text("(CURRENT_TIMESTAMP)"),
            nullable=False,
            default=None,
            onupdate=None
        )
    )
    __table_args__: tuple[object] = (CheckConstraint("typeof(point_value) = 'integer'", name="check_point_value_int"), )
    
    @override
    def __init__(self, *args: object, **kwargs: object):
        # Enforce required 'name' field manually
        if "name" not in kwargs or not kwargs["name"] or not str(kwargs["name"]).strip():
            raise ValueError("The 'name' field must be provided and non-empty.")
        # Enforce strict int for point_value
        if "point_value" in kwargs and not isinstance(kwargs["point_value"], int):
            raise TypeError(f"The 'point_value' field must be an int, got {type(kwargs['point_value']).__name__}")
        super().__init__(*args, **kwargs)
        
    @override
    def __setattr__(self, name: str, value: object) -> None:
        if name == "point_value" and not isinstance(value, int):
            raise TypeError(f"{name} must be int, got {type(value).__name__}")
        if name == "name" and (value is None or (isinstance(value, str) and value.strip() == "")):
            raise ValueError(f"{name} must not be empty/none, got {value}")
        super().__setattr__(name, value)
        
class Schedule(BaseModel, table=True):
    day_of_week: days_of_week = Field(default=days_of_week.SUNDAY, sa_column_kwargs={"nullable": False})
    task_id: int = Field(nullable=False, foreign_key="task.id")
    updated_at: datetime = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("(CURRENT_TIMESTAMP)"),
            server_onupdate=text("(CURRENT_TIMESTAMP)"),
            nullable=False,
            default=None,
            onupdate=None
        )
    )