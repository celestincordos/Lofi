import asyncio

from creator import Creator
from data import DataManager


class Orchestrator:
    def __init__(self, nr_of_tasks: int = 5):
        self.nr_of_tasks = nr_of_tasks
        self.data_manager = DataManager()
        self.creators = [Creator(i, data_manager=self.data_manager)
                         for i in range(self.nr_of_tasks)]

    async def async_create(self):
        tasks = [creator.create() for creator in self.creators]
        files = await asyncio.gather(*tasks)

    def create(self, iterations: int = 1):
        asyncio.run(self.async_create())
