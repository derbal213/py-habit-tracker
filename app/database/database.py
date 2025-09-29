from .models import Task
from .db_consts import SessionLocal, engine
from sqlmodel import SQLModel, select
from sqlalchemy.sql.elements import BinaryExpression
from typing import Any

def test() -> None:
    try:
        task: Task = Task(name="Take out trash", point_value=1)
        task.insert()
    except ValueError as ve:
        print(ve)
    
    tasks: list[Task] = query_tasks(point_values=[1])
    for t in tasks:
        print(t)
        
    new_task = list(filter(lambda x: x.name == "Take out trash", tasks))[0]
    new_task.name = "Take out trash on Thursday"
    new_task.point_value = 2
    print()
    print(new_task)
    new_task.insert()
    
    task = Task(description="This test is missing a name", point_value=3)
    task.insert()

def query_tasks(
        ids: int | list[int] | None = None, 
        names: str | list[str] | None = None, 
        point_values: int | list[int] | None = None) -> list[Task]:
    
    def ensure_list(value: Any) -> list[Any] | None:  # pyright: ignore[reportExplicitAny]
        if value is None:
            return None
        return value if isinstance(value, list) else [value]  # pyright: ignore[reportUnknownVariableType]
    
    ids = ensure_list(ids)
    names = ensure_list(names)
    point_values = ensure_list(point_values)
    
    with SessionLocal() as session:
        statement = select(Task)
        filters: list[BinaryExpression[bool]] = []

        if ids:
            filters.append(Task.id.in_(ids))    # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]
        if names:
            filters.append(Task.name.in_(names))  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]
        if point_values:
            filters.append(Task.point_value.in_(point_values))  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]

        if filters:
            statement = statement.where(*filters)
            
        results = session.execute(statement)
        
        return list(results.scalars().all())

def main() -> None:
    SQLModel.metadata.create_all(engine)
    test()

if __name__ == "__main__":
    main()