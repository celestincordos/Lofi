import os
import numpy as np
from hashlib import md5


class Track:

    def _encode(self) -> str:
        # maybe here I need mu = list(self.features) and to use mu instead of self.features in the following
        # create a hash for vector mu
        hash = ""
        # first 20 characters are each sampled from 5 entries
        for i in range(0, 100, 5):
            hash += str((self.features[0][i:i +
                        1].abs().sum() * 587).int().item())[-1]
        # last 4 characters are the beginning of the MD5 hash of the whole vector
        hash2 = int(md5(self.features.numpy()).hexdigest(), 16)
        hash = f"#{hash}{hash2}"[:25]
        return hash

    def __init__(self, features: np.array[np.float32], id: str = None) -> None:
        self.features: np.array[np.float32] = features
        # will still have to test this syntax right here... But it should work according to the first tests
        self.id: str = id or self._encode(self.features)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Track):
            raise NotImplemented(
                f"Cannot compare object of type {type(__o)} and obect of type {type(self)}")
        if self.id is not None and __o.id is not None:
            return self.id == __o.id
        return np.array_equal(self.features, __o.features)


class DataManager:
    # The ids of the trackl that are being created.... # so this class is "static" ? Do I really want that ? It should not matter....
    tracks: dict[Track] = {}

    def __init__(self):
        self.existing_ids = set(os.listdir("../ressources"))

    def track_exists(self, id: str) -> bool:
        return (id in self.existing_ids)
