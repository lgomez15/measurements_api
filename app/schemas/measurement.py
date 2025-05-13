from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MeasurementBase(BaseModel):
    co2_value: float = Field(..., gt=0, description="CO2 value in numeric format")
    unit: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None

class MeasurementCreate(MeasurementBase):
    pass

class MeasurementUpdate(MeasurementBase):
    co2_value: Optional[float] = Field(None, gt=0, description="CO2 value in numeric format")

class Measurement(MeasurementBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True
