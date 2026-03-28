# session_store.py
from abc import ABC, abstractmethod
from typing import Any, Optional
import asyncio
from SmartTiming.session import Session

class SessionStore(ABC):

    @abstractmethod
    async def get(self, session_id: str) -> Optional[dict]:
        ...

    @abstractmethod
    async def create(self, session_id: str) -> None:
        ...

    @abstractmethod
    async def delete(self, session_id: str) -> None:
        ...

    @abstractmethod
    async def session_ids(self) -> list[str]:
        ...


class InMemorySessionStore(SessionStore):
    def __init__(self):
        self._data = {}
        self._lock = asyncio.Lock()

    async def get(self, session_id: str) -> Optional[dict]:
        async with self._lock:
            return self._data.get(session_id)

    async def create(self, session_id: str) -> None:
        async with self._lock:
            if session_id in self._data:
                raise ValueError("Session existiert bereits")
            self._data[session_id] = Session()

    async def delete(self, session_id: str) -> None:
        async with self._lock:
            self._data.pop(session_id, None)

    async def session_ids(self) -> list[str]:
        async with self._lock:
            return list(self._data.keys())

