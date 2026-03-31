from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Modell für einen eindimensionalen Vektor aus Floats
class VectorModel(BaseModel):
    vector: List[float]


# Modell für einen einzelnen Punkt im 2D-Raum
class PointModel(BaseModel):
    x: float
    y: float


# Modell für eine Liste von Punkten (z. B. für Kurven, Messreihen)
class PointsModel(BaseModel):
    points: List[PointModel]


# Ergebnis eines Critical-Power-Berechnungsmodells
class CriticalPowerResultModel(BaseModel):
    CP: float   # Critical Power
    W: float    # Work Capacity (W′)


# Request-Modell zum Erstellen einer Session
class SessionCreate(BaseModel):
    session_name: str


# Request-Modell für den Beitritt eines Clients zu einer Session
class JoinSessionRequest(BaseModel):
    client_name: str


# Request-Modell für den Update eines Clients
class UpdateClientRequest(BaseModel):

    class GeoCoords(BaseModel):
        latitude: float
        longitude: float
        accuracy: float
        altitude: Optional[float] = None
        altitudeAccuracy: Optional[float] = None
        heading: Optional[float] = None
        speed: Optional[float] = None

    coords: GeoCoords
    timestamp: int


# Result-Modell für den gefilterten Update eines Clients
class UpdateClientResultModel(BaseModel):
    latitude: float
    longitude: float
    speed: float


