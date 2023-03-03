import asyncio

from creator import Creator
from data import DataManager


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
