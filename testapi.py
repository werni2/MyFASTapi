from fastapi import APIRouter
from mytypes import *
import numpy as np

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hallo Werner, FastAPI läuft!"}

@router.get("/Liste")
def Liste():
    return [1, 2, 3]

@router.get("/add") 
def add(a: float, b: float): 
    return {"summe": a + b}

@router.post("/vectornorm") 
def norm(vec: VectorModel): 
    v = np.array(vec.vector, dtype=float)
    return {"magnitude": float(np.linalg.norm(v))}

@router.post("/CriticalPower", response_model=CriticalPowerResultModel) 
def CriticalPower(data: PointsModel): 

    # get data & invert x
    x = np.array([1.0/p.x for p in data.points]) 
    y = np.array([p.y for p in data.points]) 

    # linear regression
    W, CP = np.polyfit(x, y, 1)
    
    return CriticalPowerResultModel(CP=CP, W=W)