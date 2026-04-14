import math
import sys
import os
import numpy as np
import random
import matplotlib.pyplot as plt

# Pfad zum SmartTiming-Ordner hinzufügen
sys.path.append(os.path.abspath("C:\Dev\Python\MyfASTapi\SmartTiming"))
print(os.listdir(r"C:\Dev\Python\MyfASTapi\SmartTiming"))

from TimingClient import TimingClient

class Coord:

    def __init__(self, latitude: float, longitude: float):
        self._latitude = latitude
        self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude
    
class Update:
        
    def __init__(self, latitude: float, longitude: float, time: float):
        self._coords = Coord(latitude, longitude)
        self._timestamp = time * 1000.0

    @property
    def coords(self):
        return self._coords    

    @property
    def timestamp(self):
        return self._timestamp

class GPSProvider:

    def __init__(self, sigma_m: float = 10.0, latitude: float = 50.0, longitude: float = 9.0, max_speed_kmh: float = 40.0, distance_m: float = 1000.0):
        
        self.__m_per_deg_lat = 40000000.0 / 360.0
        self.__m_per_deg_lon = self.__m_per_deg_lat * math.cos(latitude * math.pi / 180)
        self.__sigma_lat_deg = sigma_m / self.__m_per_deg_lat
        self.__sigma_lon_deg = sigma_m / self.__m_per_deg_lon
        self.__latitude = latitude 
        self.__longitude = longitude
        self.__delta_lat = 0.5 * distance_m / self.__m_per_deg_lat
        self.__omega = max_speed_kmh / 3.6 / (0.5 * distance_m)

    def __GetCoordinate(self, t: float) -> Update:
        lat = self.__latitude + self.__delta_lat * math.sin(self.__omega * t)
        lon = self.__longitude 
        deriv_lat = random.gauss(0.0, self.__sigma_lat_deg)
        deriv_lon = random.gauss(0.0, self.__sigma_lon_deg)
        #lat = 0
        return Update(lat + deriv_lat, lon + deriv_lon, t)
    
    def __call__(self, t: float) -> tuple[float, float]:
        return self.__GetCoordinate(t)
    
def gps_to_xy(coord: Coord, coord0: Coord) -> tuple[float, float]:
    # Meter pro Grad
    m_per_deg_lat = 111320
    m_per_deg_lng = 111320 * math.cos(math.radians(coord0.latitude))

    dx = (coord.longitude - coord0.longitude) * m_per_deg_lng
    dy = (coord.latitude - coord0.latitude) * m_per_deg_lat

    return (dx, dy)

def length(pos: tuple[float, float]) -> float:

    return math.sqrt(pos[0]**2 + pos[1]**2)

if __name__ == "__main__":


    gps = GPSProvider(sigma_m=5.0)
    client = TimingClient(sigma_m=5.0, q=0.01, client_id="testclient", update_data=gps(0))

    time = []
    x_pos = []
    y_pos = []
    dy_pos = []
    len = []
    y_filt = []
    dy_filt = []
    coord0 = None
    for t in range(0, 1000, 1):
        coord = gps(t)
        if coord0 is None:
            coord0 = coord.coords

        client(coord)
        x, dx, ddx, y, dy, ddy = client.state
        y_filt.append(y)
        dy_filt.append(dy)

        pos = gps_to_xy(coord.coords, coord0)

        time.append(t)
        x_pos.append(pos[0])
        y_pos.append(pos[1])
        len.append(length(pos))

    sigma = float(np.std(len))  
    dy_pos = list(np.diff(y_pos))
    dy_pos.append(0.0)

    fig, ax1 = plt.subplots()

    ax1.plot(time, y_filt, color="red", label="y_filtered(t)")
    ax1.plot(time, y_pos, color="orange", label="y(t)")
    ax1.set_xlabel("t")
    ax1.set_ylabel("position [m]", color="red")
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()

    ax2.plot(time, dy_pos, color="blue", label="dy(t)")
    ax2.plot(time, dy_filt, color="green", label="dy_filtered(t)")
    ax2.set_ylabel("dy(t))", color="blue")
    ax2.tick_params(axis="y", labelcolor="blue")

    plt.title("lat(t) und dlat  (t) mit zwei y‑Achsen")
    plt.grid(True)

    plt.show()

   
    print("Client ID:", client.client_id)