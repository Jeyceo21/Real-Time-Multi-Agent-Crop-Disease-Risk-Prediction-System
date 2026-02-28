from fastapi import FastAPI
from pydantic import BaseModel
from app.orchestrator import run_prediction

app = FastAPI()


class PredictionInput(BaseModel):
    latitude: float
    longitude: float
    nitrogen_days: int
    sowing_days: int
    state: str


@app.post("/predict")
def predict(data: PredictionInput):
    result = run_prediction(
        lat=data.latitude,
        lon=data.longitude,
        nitrogen_days=data.nitrogen_days,
        sowing_days=data.sowing_days,
        state=data.state
    )
    return result