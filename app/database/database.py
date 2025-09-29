from .models import Task
from .db_consts import SessionLocal, engine
from sqlmodel import SQLModel, select
from sqlalchemy.sql.elements import BinaryExpression

def test() -> None:
    try:
        task: Task = Task(name="Take out trash", point_value=1)
        task.insert()
    except ValueError as ve:
        print(ve)
    
    tasks: list[Task] = query_tasks(point_value=[1])
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
        id: list[int] | None = None, 
        name: list[str] | None = None, 
        point_value: list[int] | None = None) -> list[Task]:    
    with SessionLocal() as session:
        statement = select(Task)
        filters: list[BinaryExpression[bool]] = []

        if id:
            filters.append(Task.id.in_(id))    # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]
        if name:
            filters.append(Task.name.in_(name))  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]
        if point_value:
            filters.append(Task.point_value.in_(point_value))  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]

        if filters:
            statement = statement.where(*filters)
            
        results = session.execute(statement)
        
        return list(results.scalars().all())

def main() -> None:
    SQLModel.metadata.create_all(engine)
    test()

if __name__ == "__main__":
    main()