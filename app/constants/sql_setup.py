DATABASE_NAME = "habit_tracker.db"

CREATE_TASK_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY, 
    name text NOT NULL,
    point_value integer
);"""
