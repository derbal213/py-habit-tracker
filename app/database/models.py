import logging
from .db_consts import SessionLocal
from datetime import datetime, timezone
from typing import ClassVar, override
from pydantic import StrictInt, validator
from sqlmodel import SQLModel, Field, CheckConstraint, select, Column, VARCHAR, INTEGER

class BaseModel(SQLModel):
    # Specifies the set of index elements which represent the ON CONFLICT target
    UPSERT_INDEX_ELEMENTS: ClassVar[set[str]] = set()

    # Specifies the set of fields to exclude from updating in the resulting
    # UPSERT statement
    UPSERT_EXCLUDE_FIELDS: ClassVar[set[str]] = set()
    default_exclude_fields: ClassVar[set[str]] = {"id", "created_on", "updated_on"}

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    def upsert(self):
        with SessionLocal() as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            
class Task(BaseModel, table=True):    
    name: str = Field(sa_column=Column("name", VARCHAR, unique=True, index=True, nullable=False))
    description: str|None = None
    point_value: StrictInt = Field(default=0, nullable=False)

    __table_args__ = (CheckConstraint("typeof(point_value) = 'integer'", name="check_point_value_int"), )

    #UPSERT_EXCLUDE_FIELDS: ClassVar[set[str]] = {"id"}
    UPSERT_INDEX_ELEMENTS: ClassVar[set[str]] = {"id"}
    
    @override
    def __init__(self, *args: object, **kwargs: object):
        # Enforce required 'name' field manually
        if "name" not in kwargs or not kwargs["name"] or not str(kwargs["name"]).strip():
            raise ValueError("The 'name' field must be provided and non-empty.")
        # Enforce strict int for point_value
        if "point_value" in kwargs and not isinstance(kwargs["point_value"], int):
            raise TypeError(f"The 'point_value' field must be an int, got {type(kwargs['point_value']).__name__}")
        super().__init__(*args, **kwargs)
    
    # @validator("name", pre=True, always=True)
    # def name_must_be_provided(cls, v: object) -> object:
    #     if v is None or (isinstance(v, str) and not v.strip()):
    #         raise ValueError("The 'name' field must be provided and non-empty.")
    #     return v
    
    @override
    def __setattr__(self, name: str, value: object) -> None:
        if name == "point_value" and not isinstance(value, int):
            raise TypeError(f"{name} must be int, got {type(value).__name__}")
        if name == "name" and (value is None or (isinstance(value, str) and value.strip() == "")):
            raise ValueError(f"{name} must not be empty/none, got {value}")
        super().__setattr__(name, value)