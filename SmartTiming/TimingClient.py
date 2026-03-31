from abc import ABC, abstractmethod
from filterpy.kalman import KalmanFilter
import numpy as np

class TimingClient(ABC):

    def __init__(self, client_id: str):
        self._latitude = 0.0
        self._longitude = 0.0
        self._timestamp = 0.0
        self._speed = 0.0
        self._client_id =client_id
        self_kalman = KalmanFilter(dim_x=4, dim_z=2)

        # State: [x, y, vx, vy]
        self_kalman.x = np.array([0., 0., 0., 0.])

    def update(self, update_data):

        self._timestamp = update_data.timestamp
        self._speed = 0.0

        #self.kalman.predict()
        #self.kalman.update(np.array([update_data.coords.latitude, update_data.coords.longitude]))

        # filtered state
        self._latitude = update_data.coords.latitude
        self._longitude = update_data.coords.longitude

    @property
    def client_id(self):
        return self._client_id

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def speed(self):
        return self._speed

