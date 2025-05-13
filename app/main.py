from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import measurement
from app.models import measurement as measurement_models
from app.database import engine

app = FastAPI(title="Measurement API", version="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

measurement_models.Base.metadata.create_all(bind=engine)
app.include_router(measurement.router)