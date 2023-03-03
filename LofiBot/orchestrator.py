import asyncio

from creator import Creator
from data import DataManager
import numpy as np


class Track:
    def __init__(self, features: np.array[np.float32], id: str = None) -> None:
        self.features = features
        self.id = id

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Track):
            raise NotImplemented(
                f"Cannot compare object of type {type(__o)} and obect of type {type(self)}")
        if self.id is not None and __o.id is not None:
            return self.id == __o.id
        return np.array_equal(self.features, __o.features)


class Orchestrator:
    def __init__(self, nr_of_tasks: int = 5):
        self.nr_of_tasks = nr_of_tasks
        self.creators = [Creator(i) for i in range(self.nr_of_tasks)]
        self.data_manager = DataManager()

    async def async_create(self):
        tasks = [creator.create() for creator in self.creators]
        asyncio.gather(*tasks)

    def create(self):
        return
