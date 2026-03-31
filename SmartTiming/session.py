from abc import ABC, abstractmethod
from SmartTiming.TimingClient import TimingClient
import asyncio

class Session(ABC):

    def __init__(self):
        self.__clients = {}
        self.__lock = asyncio.Lock()
    
    async def add_client(self, client_id: str) -> None:
        async with self.__lock:
            if client_id in self.__clients:
                raise ValueError("Client existiert bereits")
            self.__clients[client_id] = TimingClient()

    async def get_client(self, client_id: str) -> TimingClient:
        async with self.__lock:
            if client_id not in self.__clients: 
                raise ValueError("Client existiert nicht")
            return self.__clients[client_id]