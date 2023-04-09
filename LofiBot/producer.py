from data import DataManager
import logging
from random import sample
import os
from pydub import AudioSegment
from tqdm import tqdm

from settings import PRODUCED_PATH, FILE_EXTENSION_CONVERTED


class Producer:

    data_manager = DataManager()

    def __init__(self, track_repetitions: int = 1) -> None:
        self.working_directory = self._create_working_directory()
        self.track_repetitions = track_repetitions

    def _create_working_directory(self) -> str:
        base_folder = os.path.join(PRODUCED_PATH)
        other_folders = set(os.listdir(base_folder))
        new_folder = 0
        while str(new_folder) in other_folders:
            new_folder += 1
        return os.path.join(base_folder, str(new_folder))

    def _compose(self, track_paths: dict[str]):
        os.mkdir(self.working_directory)
        logging.info(f'Composing...')
        for (key, path) in (tqdm(track_paths.items())):
            audio: AudioSegment = AudioSegment.from_file(
                path, FILE_EXTENSION_CONVERTED)
            composed = audio * self.track_repetitions
            composed.export(os.path.join(self.working_directory, f"{key}.{FILE_EXTENSION_CONVERTED}"),
                            format=FILE_EXTENSION_CONVERTED)

    def compose_random(self, nr_of_tracks: int = 10, accept_existing: bool = False):
        free_ids = self.data_manager.free_ids
        work_ids = []  # the ones that are being used for this compilation...

        # IF there are enough free tracks...
        if len(self.data_manager.free_ids) >= nr_of_tracks:  # the good case...
            work_ids = sample(free_ids, k=nr_of_tracks)
            self.data_manager.mark_used(work_ids)
        else:
            # If you don't accept already used, stop here
            if not accept_existing:
                logging.info(
                    f"There are only {len(self.data_manager.free_ids)} free tracks but a composition of {nr_of_tracks} was requested... Will stop here")
                return
            # If you do accept, I will give you alle the free ones plus used ones
            else:
                # use the free
                self.data_manager.mark_used(free_ids)
                existing = self.data_manager.used_ids
                work_ids = sample(existing, nr_of_tracks -
                                  len(work_ids)) + existing
        track_paths = {id: self.data_manager.get_track_path(
            id) for id in work_ids}
        self._compose(track_paths)


def main():
    logging.basicConfig(level=logging.INFO)
    producer = Producer()
    producer.compose_random(10)


if __name__ == "__main__":
    main()
