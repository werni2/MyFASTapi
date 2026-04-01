from abc import ABC, abstractmethod
import math
from filterpy.kalman import KalmanFilter
import numpy as np

class TimingClient(ABC):

    def __init__(self, client_id: str):
        self._latitude = 0.0
        self._longitude = 0.0
        self._timestamp = 0.0
        self._speed = 0.0
        self._client_id =client_id
        self.kalman = KalmanFilter(dim_x=4, dim_z=2)

        # State: [lat, long, dlat, dlong]
        self.kalman.x = np.array([0., 0., 0., 0.])

        # Messmatrix: wir messen nur Position
        self.kalman.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])

        # Start-Kovarianz
        self.kalman.P = np.eye(4, dtype=float) * 1e-3

        # Messrauschen R
        self._m_per_deg_lat = 40000000.0 / 360.0
        self._m_per_deg_lon = self._m_per_deg_lat * math.cos(self._latitude * math.pi / 180)
        sigma_m = 3.0 
        self._sigma_lat_deg = sigma_m / self._m_per_deg_lat
        self._sigma_lon_deg = sigma_m / self._m_per_deg_lon
        self.kalman.R = np.diag([self._sigma_lon_deg**2, self._sigma_lat_deg**2])

    def update(self, update_data):

        dt = update_data.timestamp - self._timestamp # ms
        self._timestamp = update_data.timestamp
        self._speed = 0.0

        # Zustandsübergang
        self.kalman.F = np.array([
            [1, 0, dt, 0 ],
            [0, 1, 0,  dt],
            [0, 0, 1,  0 ],
            [0, 0, 0,  1 ]
        ], dtype=float)

        # prozessrauschen
        Q = np.zeros((4, 4), dtype=float)
        sx2 = self._sigma_lat_deg**2
        sy2 = self._sigma_lon_deg**2

        # x, vx
        Q[0, 0] = 0.25 * dt**4 * sx2
        Q[0, 2] = 0.5  * dt**3 * sx2
        Q[2, 0] = Q[0, 2]
        Q[2, 2] =        dt**2 * sx2

        # y, vy
        Q[1, 1] = 0.25 * dt**4 * sy2
        Q[1, 3] = 0.5  * dt**3 * sy2
        Q[3, 1] = Q[1, 3]
        Q[3, 3] =        dt**2 * sy2

        self.kalman.Q = Q

        self.kalman.predict()
        self.kalman.update(np.array([update_data.coords.latitude, update_data.coords.longitude]))

        # filtered state
        self._latitude = self.kalman.x[0]
        self._longitude = self.kalman.x[1]
        self._speed = math.sqrt((self.kalman.x[2]*self._m_per_deg_lat)**2 + (self.kalman.x[3]*self._m_per_deg_lon)**2) / 1000.0 

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

