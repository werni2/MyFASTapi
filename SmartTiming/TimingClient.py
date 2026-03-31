from abc import ABC, abstractmethod
from filterpy.kalman import KalmanFilter
import numpy as np

class TimingClient(ABC):

    def __init__(self):
        self._latitude = None
        self._longitude = None
        self._timestamp = None
        self._speed = None
        self_kalman = KalmanFilter(dim_x=4, dim_z=2)

        # State: [x, y, vx, vy]
        self_kalman.x = np.array([0., 0., 0., 0.])

    def update(self, update_data):

        self._timestamp = update_data.timestamp
        self._speed = 0.0

        self.kalman.predict()
        self.kalman.update(np.array([update_data.coords.latitude, update_data.coords.longitude]))

        # filtered state
        self._latitude = self.kalman.x[0]
        self._longitude = self.kalman.x[1]

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

