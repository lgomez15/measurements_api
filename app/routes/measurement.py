from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.models.measurement import Measurement  
from app.dependencies import get_db


router = APIRouter(prefix="/measurements", tags=["measurements"])

@router.post("/", response_model=schemas.Measurement, status_code=status.HTTP_201_CREATED)
def create_measurement(
    measurement: schemas.MeasurementCreate,
    db: Session = Depends(get_db)
):
    db_measurement = Measurement(**measurement.dict())
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement

@router.get("/", response_model=List[schemas.Measurement])
def read_measurements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    measurements = db.query(Measurement).offset(skip).limit(limit).all()
    return measurements

@router.get("/{measurement_id}", response_model=schemas.Measurement)
def read_measurement(
    measurement_id: int,
    db: Session = Depends(get_db)
):
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    if measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement

@router.put("/{measurement_id}", response_model=schemas.Measurement)
def update_measurement(
    measurement_id: int,
    measurement: schemas.MeasurementUpdate,
    db: Session = Depends(get_db)
):
    db_measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    if db_measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    
    for key, value in measurement.dict(exclude_unset=True).items():
        setattr(db_measurement, key, value)
    
    db.commit()
    db.refresh(db_measurement)
    return db_measurement

@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement(
    measurement_id: int,
    db: Session = Depends(get_db)
):
    db_measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    if db_measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    
    db.delete(db_measurement)
    db.commit()
    return