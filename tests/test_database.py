import pytest
from app.database.database import query_tasks
from app.database.models import Task

def test_task_query():
    # First insert the record we need since we're working in memory
    task = Task(name="test_select", description="This is a test task for testing selects", point_value=3)
    task.insert()
    print(f"----> {task.name} | {task.updated_at}")
    assert task.id is not None and task.id >= 0
    
    new_task: list[Task] = query_tasks([task.id])
    assert new_task is not None and new_task
    print(f"----> {new_task[0].name} | {new_task[0].updated_at}")
    assert new_task == [task]
