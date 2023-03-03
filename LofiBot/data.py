import os


class DataManager:
    # The ids of the trackl that are being created.... # so this class is "static" ? Do I really want that ? It should not matter....
    pending_ids: list[str] = []

    def __init__(self):
        self.existing_ids = set(os.listdir("../ressources"))

    def track_exists(self, id: str) -> bool:
        return (id in self.existing_ids)
