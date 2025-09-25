from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from models.base import base_table

def setup_database() -> None:
    # SQLite database
    engine: Engine = create_engine("sqlite:///task_tracker.db", echo=True)

    # Create table(s) if they don't exist
    base_table.metadata.create_all(engine)

def main() -> None:
    setup_database()

if __name__ == "__main__":
    main()