from abc import ABC, abstractmethod
import math
from filterpy.kalman import KalmanFilter
import numpy as np

class TimingClient(ABC):

    def __init__(self, sigma_m: float, q: float, client_id: str, update_data = None):

        self.__sigma_m      = sigma_m
        self.__q            = q
        self.__client_id    = client_id
        self.__kf           = KalmanFilter(dim_x=6, dim_z=2)
        self.__origin       = update_data.coords if update_data is not None else None
        self.__t            = update_data.timestamp / 1000.0 if update_data is not None else None 
        self.__dt           = 0.0  
        self.__speed        = 0.0  

        # State: px, vx, ax, py, vy, ay
        self.__kf.x         = np.zeros(6)

        # Measurement: px, py
        self.__kf.H         = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0]
        ])

        # Measurement noise
        self.__kf.R         = np.eye(2) * (self.__sigma_m**2)

        # Initial covariance
        self.__kf.P           = np.eye(6) * 10.0

    def __predict(self, dt):
        
        dt2                 = dt*dt
        dt3                 = dt2*dt
        dt4                 = dt2*dt2
        dt5                 = dt3*dt2

        # State transition matrix
        self.__kf.F         = np.array([
            [1, dt, dt2/2, 0,  0,     0],
            [0,  1, dt,    0,  0,     0],
            [0,  0, 1,     0,  0,     0],
            [0,  0, 0,     1, dt, dt2/2],
            [0,  0, 0,     0,  1, dt],
            [0,  0, 0,     0,  0, 1]
        ])

        # Process noise
        self.__kf.Q         = self.__q * np.array([
            [dt5/20, dt4/8, dt3/6, 0,       0,       0],
            [dt4/8,  dt3/3, dt2/2, 0,       0,       0],
            [dt3/6,  dt2/2, dt,    0,       0,       0],
            [0,      0,      0,    dt5/20, dt4/8, dt3/6],
            [0,      0,      0,    dt4/8,  dt3/3, dt2/2],
            [0,      0,      0,    dt3/6,  dt2/2, dt]
        ])

        self.__kf.predict()

    def __update(self, coord):

        def gps_to_xy(coord, coord0) -> tuple[float, float]:
            # Meter pro Grad
            m_per_deg_lat = 111320
            m_per_deg_lng = 111320 * math.cos(math.radians(coord0.latitude))

            x = (coord.longitude - coord0.longitude) * m_per_deg_lng
            y = (coord.latitude - coord0.latitude) * m_per_deg_lat

            return (x, y)

        pos = gps_to_xy(coord, self.__origin)
        self.__kf.update(np.array([pos[0], pos[1]]))
    
    def __call__(self, update_data = None):
        self.__dt = update_data.timestamp / 1000.0 - self.__t
        self.__t = update_data.timestamp / 1000.0
        self.__predict(dt = self.__dt) 
        self.__update(update_data.coords)
    
    @property
    def client_id(self):
        return self.__client_id

    @property
    def state(self):
        return [float(f) for f in self.__kf.x]

    @property
    def time(self):
        return self.__t

    @property
    def speed(self):
        return self.__speed





