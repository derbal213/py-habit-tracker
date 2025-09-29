import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from app.database.models.base import base_table
from sqlmodel import SQLModel

@pytest.fixture(autouse=True)
def override_session(monkeypatch):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    print("conftest.py loaded")
    test_engine = create_engine("sqlite:///:memory:")
    SessionTest = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)
    monkeypatch.setattr("app.database.models.SessionLocal", SessionTest)  # pyright: ignore[reportUnknownMemberType]
    monkeypatch.setattr("app.database.database.SessionLocal", SessionTest)  # pyright: ignore[reportUnknownMemberType]
    #base_table.metadata.create_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    session = SessionTest()
    yield session
    session.close()