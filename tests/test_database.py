import pytest
from app.database.database import query_tasks, query_schedule
from app.database.models import Task, Schedule
from app.database.db_consts import days_of_week

def test_task_queries():
    # First insert the record we need since we're working in memory
    task: Task = Task(name="test_select", description="This is a test task for testing selects", point_value=33)
    task2: Task = Task(name="test_select2", description="This is a second value for testing selection", point_value=33)
    task.upsert()
    task2.upsert()
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
    
def test_schedule_queries():
    task: Task = Task(name="Basic Schedule Query", description="This test is a basic schedule query", point_value=3)
    task.upsert()
    assert task.id
    
    task_schedule: Schedule = Schedule(day_of_week=days_of_week.MONDAY, task_id=task.id)
    task_schedule.upsert()
    assert task_schedule.id
    
    assert task_schedule.day_of_week == days_of_week.MONDAY
    assert task.id == task_schedule.task_id
    
    schedule2: Schedule = Schedule(day_of_week=days_of_week.FRIDAY, task_id=task.id)
    schedule2.upsert()
    assert schedule2.id
    assert schedule2.day_of_week == days_of_week.FRIDAY
    assert schedule2.task_id == task.id

    schedules: list[Schedule] = query_schedule(task.id, None)
    assert len(schedules) == 2
    
    schedules_friday = query_schedule(days=days_of_week.FRIDAY)
    assert len(schedules_friday) == 1