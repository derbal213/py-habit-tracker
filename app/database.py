import sqlite3

DATABASE_NAME = "habit_tracker.db"
CREATE_TASK_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY, 
    name text NOT NULL,
    point_value integer
);"""

def setup_database():
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            print(f"Opened sqlite database with version {sqlite3.sqlite_version} successfully")
            cursor: sqlite3.Cursor = conn.cursor()
            _ = cursor.execute(CREATE_TASK_TABLE)
            conn.commit()
    except sqlite3.OperationalError as oe:
        print("Failed to setup database:", oe)

def main():
    setup_database()

if __name__ == "__main__":
    main()