from pydantic import BaseModel 
from typing import List

class VectorModel(BaseModel): 
    vector: List[float]

class PointModel(BaseModel): 
    x: float 
    y: float

class PointsModel(BaseModel): 
    points: List[PointModel]

class CriticalPowerResultModel(BaseModel): 
    CP: float 
    W: float

