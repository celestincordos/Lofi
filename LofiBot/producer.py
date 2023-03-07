from data import DataManager
import logging
from random import sample


class Producer:

    data_manager = DataManager()

    def __init__(self) -> None:
        pass

    def compose_random(self, accept_existing: bool = False, nr_of_tracks: int = 10):
        free_ids = self.data_manager.free_ids
        used_ids = []
        if not accept_existing:
            if len(self.data_manager.free_ids) > nr_of_tracks:
                logging.info(
                    f"There are only {len(self.data_manager.free_ids)} free tracks but a composition of {nr_of_tracks} was requested... Will stop here")
                return
            used_ids = sample(free_ids, k=nr_of_tracks)
            self.data_manager.mark_used(used_ids)
