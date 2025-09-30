#import pytest
from app.database.db_consts import days_of_week
from app.database.models import Task, Schedule

def test_basic_insert():
    task: Task = Task(name="Basic Schedule", description="This test is a basic schedule insert", point_value=3)
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
    
