import pytest
from app.database.models import Task
from sqlalchemy.exc import IntegrityError

def test_insert_baseline():
    task = Task(name="test_insert", description="This is a test task for testing inserts", point_value=3)
    task.upsert()
    assert task.id is not None and task.id >= 0
    
def test_insert_missing_name():
    with pytest.raises(ValueError):
        task = Task(description="This test is missing a name", point_value=3)
        task.upsert()

def test_insert_then_update():
    task = Task(name="test_insert", description="This is a test task for testing inserts", point_value=3)
    task.upsert()
    assert task.id is not None and task.id >= 0
    
    old_task_id = task.id
    
    task.name = "This test is now changing the name"
    task.point_value = 4
    task.upsert()
    assert old_task_id == task.id
    assert task.name == "This test is now changing the name"
    
def test_invalid_points():
    with pytest.raises(TypeError):
        _ = Task(name="Invalid Point Test", point_value="str")
        
def test_valid_name_then_remove_name():
    task = Task(name="valid", description="This is a test for changing name to an invalid value")
    with pytest.raises(ValueError):
        task.name = None  # pyright: ignore[reportAttributeAccessIssue]
        
def test_valid_point_then_invalid_point():
    task = Task(name="Change Point Test", description="This is a test for changing point_value to an invalid value", point_value = 3)
    with pytest.raises(TypeError):
        task.point_value = "str"