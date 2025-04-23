import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.app.main import app
from app.db.models import Base
from app.db.database import get_db

DATABASE_URL = "postgresql://postgres:postgres@test-db:5432/postgres"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture(scope="function")
# def setup_db():
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     yield db
#     db.close()
#     Base.metadata.drop_all(bind=engine)
#


def override_get_db():
    db = TestingSessionLocal()
    print("db was overrode")
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("tabled created")
    yield


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


def test_create_vacation(client, setup_db):
    vacation_data = {
        "employee_id": 1,
        "start_date": "2025-05-01",
        "end_date": "2025-05-10",
    }
    response = client.post("/vacations/", json=vacation_data)

    assert response.status_code == 200
    assert response.json()["employee_id"] == vacation_data["employee_id"]
    assert response.json()["start_date"] == vacation_data["start_date"]
    assert response.json()["end_date"] == vacation_data["end_date"]


def test_last_three_vacations(client, setup_db):
    vacation_data_1 = {
        "employee_id": 1,
        "start_date": "2025-01-01",
        "end_date": "2025-01-10",
    }
    vacation_data_2 = {
        "employee_id": 1,
        "start_date": "2025-02-01",
        "end_date": "2025-02-10",
    }
    vacation_data_3 = {
        "employee_id": 1,
        "start_date": "2025-03-01",
        "end_date": "2025-03-10",
    }
    vacation_data_4 = {
        "employee_id": 1,
        "start_date": "2025-04-01",
        "end_date": "2025-04-10",
    }

    client.post("/vacations/", json=vacation_data_1)
    client.post("/vacations/", json=vacation_data_2)
    client.post("/vacations/", json=vacation_data_3)
    client.post("/vacations/", json=vacation_data_4)

    response = client.get("/vacations/last/1")
    assert response.status_code == 200
    vacations = response.json()
    assert len(vacations) == 3
    assert vacations[0]["employee_id"] == 1
    assert vacations[1]["employee_id"] == 1
    assert vacations[2]["employee_id"] == 1


def test_get_vacations_by_period(client, setup_db):
    vacation_data_1 = {
        "employee_id": 1,
        "start_date": "2025-01-01",
        "end_date": "2025-01-10",
    }
    vacation_data_2 = {
        "employee_id": 1,
        "start_date": "2025-02-01",
        "end_date": "2025-02-10",
    }

    client.post("/vacations/", json=vacation_data_1)
    client.post("/vacations/", json=vacation_data_2)

    response = client.get("/vacations/period?start_date=2025-01-01&end_date=2025-01-28")
    assert response.status_code == 200
    vacations = response.json()
    assert len(vacations) == 1


def test_delete_vacation(client, setup_db):
    vacation_data = {
        "employee_id": 1,
        "start_date": "2025-06-01",
        "end_date": "2025-06-10",
    }
    response = client.post("/vacations/", json=vacation_data)
    vacation_id = response.json()["id"]

    response = client.delete(f"/vacations/{vacation_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    response = client.delete(f"/vacations/{vacation_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Vacation not found"}
