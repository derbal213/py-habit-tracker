from .models import Task, Schedule
from .db_consts import SessionLocal, engine, days_of_week
from sqlmodel import SQLModel, select
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import Result
from typing import Any

def ensure_list(value: Any) -> list[Any] | None:
    if value is None:
        return None
    return value if isinstance(value, list) else [value]  # pyright: ignore[reportUnknownVariableType]

def run_query(stmt) -> list[Any]:  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    with SessionLocal() as session:
        results: Result[Any] = session.execute(stmt)
        return list(results.scalars().all())

def query_tasks(
        ids: int | list[int] | None = None, 
        names: str | list[str] | None = None, 
        point_values: int | list[int] | None = None) -> list[Task]:
    
    ids = ensure_list(ids)
    names = ensure_list(names)
    point_values = ensure_list(point_values)
    
    statement = select(Task)
    filters: list[BinaryExpression[bool]] = []

    if ids:
        filters.append(Task.id.in_(ids))    # pyright: ignore[reportAttributeAccessIssue]
    if names:
        filters.append(Task.name.in_(names))  # pyright: ignore[reportAttributeAccessIssue]
    if point_values:
        filters.append(Task.point_value.in_(point_values))  # pyright: ignore[reportAttributeAccessIssue]

    if filters:
        statement = statement.where(*filters)
    return run_query(statement)
    
def query_schedule(task_ids: int|list[int]|None = None, days: days_of_week|list[days_of_week]|None = None):
    days = ensure_list(days)
    task_ids = ensure_list(task_ids)
    
    statement = select(Schedule)
    filters: list[BinaryExpression[bool]] = []
    if task_ids:
        filters.append(Schedule.task_id.in_(task_ids))  # pyright: ignore[reportAttributeAccessIssue]
    if days:
        filters.append(Schedule.day_of_week.in_(days))  # pyright: ignore[reportAttributeAccessIssue]
    
    if filters:
        statement = statement.where(*filters)        
    return run_query(statement)
        

def main() -> None:
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    main()