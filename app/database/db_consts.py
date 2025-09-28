from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "sqlite:///task_tracker.sqlite"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
