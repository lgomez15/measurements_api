def test_create_measurement(client, db):
    response = client.post(
        "/measurements/",
        json={"co2_value": 400.5, "unit": "ppm", "source": "sensor1", "description": "Test measurement"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["co2_value"] == 400.5
    assert data["unit"] == "ppm"
    assert data["source"] == "sensor1"
    assert "id" in data

def test_read_measurements(client):
    response = client.get("/measurements/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_measurement(client, db):
    measurement = models.Measurement(co2_value=450.0, unit="ppm", source="sensor2")
    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    response = client.get(f"/measurements/{measurement.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == measurement.id

def test_update_measurement(client, db):
    measurement = models.Measurement(co2_value=500.0, unit="ppm", source="sensor3")
    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    response = client.put(f"/measurements/{measurement.id}", json={"co2_value": 550.0, "description": "Updated"})
    assert response.status_code == 200
    assert response.json()["co2_value"] == 550.0

def test_delete_measurement(client, db):
    measurement = models.Measurement(co2_value=600.0, unit="ppm", source="sensor4")
    db.add(measurement)
    db.commit()
    db.refresh(measurement)

    response = client.delete(f"/measurements/{measurement.id}")
    assert response.status_code == 204

    response = client.get(f"/measurements/{measurement.id}")
    assert response.status_code == 404

def test_create_measurement_invalid_co2(client):
    response = client.post("/measurements/", json={"co2_value": -1, "unit": "ppm"})
    assert response.status_code == 422
