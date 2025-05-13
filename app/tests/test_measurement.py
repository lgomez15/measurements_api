from fastapi import status
from fastapi.testclient import TestClient  
from app.models.measurement import Measurement
from app.main import app  

def test_invalid_api_key(client):
    invalid_client = TestClient(app)
    response = invalid_client.post(
        "/measurements/",
        json={"co2_value": 400.5},
        headers={"api-key": "invalid-key"} 
    )
    assert response.status_code == 401

def test_create_measurement(client, db_session):
    response = client.post(
        "/measurements/",
        json={
            "co2_value": 400.5,
            "unit": "ppm",
            "source": "sensor1",
            "description": "Test measurement"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["co2_value"] == 400.5
    assert data["unit"] == "ppm"
    assert "id" in data

def test_read_measurements(client, db_session):
    measurements = [
        Measurement(co2_value=300, source="sensorA", unit="ppm"),
        Measurement(co2_value=500, source="sensorB", unit="ppb"),
    ]
    db_session.add_all(measurements)
    db_session.commit()

    response = client.get("/measurements/?source=sensorA&unit=ppm")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["source"] == "sensorA"

def test_read_measurement(client, db_session):
    measurement = Measurement(co2_value=450.0, unit="ppm")
    db_session.add(measurement)
    db_session.commit()

    response = client.get(f"/measurements/{measurement.id}")
    assert response.status_code == 200
    assert response.json()["id"] == measurement.id

def test_update_measurement(client, db_session):
    measurement = Measurement(co2_value=500.0, unit="ppm")
    db_session.add(measurement)
    db_session.commit()

    response = client.put(
        f"/measurements/{measurement.id}",
        json={"co2_value": 550.0, "description": "Updated"}
    )
    assert response.status_code == 200
    assert response.json()["co2_value"] == 550.0

def test_delete_measurement(client, db_session):
    measurement = Measurement(co2_value=600.0, unit="ppm")
    db_session.add(measurement)
    db_session.commit()

    response = client.delete(f"/measurements/{measurement.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/measurements/{measurement.id}")
    assert response.status_code == 404

def test_invalid_api_key(client):
    invalid_client = TestClient(app)
    response = invalid_client.post(
        "/measurements/",
        json={"co2_value": 400.5},
        headers={"api_key": "invalid-key"}
    )
    assert response.status_code == 401

def test_ordering(client, db_session):
    measurements = [
        Measurement(co2_value=800, unit="ppm"),
        Measurement(co2_value=400, unit="ppb"),
    ]
    db_session.add_all(measurements)
    db_session.commit()

    response = client.get("/measurements/?order_by=co2_value&order=desc")
    assert response.status_code == 200  
    data = response.json()
    assert len(data) >= 2  
    assert data[0]["co2_value"] == 800