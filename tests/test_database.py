import pytest
from app.database.database import query_tasks
from app.database.models import Task

def test_task_query():
    # First insert the record we need since we're working in memory
    task: Task = Task(name="test_select", description="This is a test task for testing selects", point_value=33)
    task2: Task = Task(name="test_select2", description="This is a second value for testing selection", point_value=33)
    task.insert()
    task2.insert()
    print(f"----> {task.name} | {task.updated_at}")
    assert task.id is not None and task.id >= 0
    
    # Test pulling by id
    new_task: list[Task] = query_tasks([task.id])
    assert new_task is not None and new_task
    print(f"----> {new_task[0].name} | {new_task[0].updated_at}")
    assert new_task == [task]
    
    # Test pulling by name
    new_task = query_tasks(names=task2.name)
    assert new_task
    assert new_task == [task2]
    
    # Test pulling by point value
    new_task = query_tasks(point_values=33)
    assert new_task
    print(new_task)
    assert new_task == [task, task2]