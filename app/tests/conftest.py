import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
from app.models import measurement as model

@pytest.fixture(scope="module")
def client():
    measurement_models.Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    measurement_models.Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
