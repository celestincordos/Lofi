import os
import numpy as np
from hashlib import md5
import torch
import logging
import json
from pydub import AudioSegment
from pathlib import Path
from miniaudio import decode
import logging
from tqdm import tqdm
from pathlib import Path
from shutil import move

from settings import UNCONVERTED_PATH, CONVERTED_PATH, DOWNLOADED_PATH, FILE_EXTENSION, USED_PATH


class Track:

    def _encode(self) -> str:
        # maybe here I need mu = list(self.features) and to use mu instead of self.features in the following
        # create a hash for vector mu
        hash = ""
        # first 20 characters are each sampled from 5 entries

        mu = torch.from_numpy(np.array([self.features]))
        for i in range(0, 100, 5):
            hash += str((mu[0][i:i +
                        1].abs().sum() * 587).int().item())[-1]
        # last 4 characters are the beginning of the MD5 hash of the whole vector
        hash2 = int(md5(mu.numpy()).hexdigest(), 16)
        hash = f"#{hash}{hash2}"
        return hash

    def __init__(self, features: np.array, id: str = None) -> None:
        self.features: np.array[np.float64] = features
        # will still have to test this syntax right here... But it should work according to the first tests
        self.id: str = id or self._encode()
        self.json_track: dict
        self.folder_path: str

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Track):
            raise NotImplemented(
                f"Cannot compare object of type {type(__o)} and obect of type {type(self)}")
        if self.id is not None and __o.id is not None:
            return self.id == __o.id
        return np.array_equal(self.features, __o.features)

    def __str__(self) -> str:
        return self.id

    def add_json(self, json_string: str) -> None:
        self.json_track = json.loads(json_string)

    # def clean_folder(self) -> None:
    #     files = os.listdir(self.folder_path)
    #     for filename in files:
    #         if f".{FILE_EXTENSION}" in filename:
    #             full_path: str = os.path.join(self.folder_path, filename)
    #             audio_bytes = Path(full_path).read_bytes()
    #             vector_bytes_str = str(audio_bytes)
    #             vector_bytes_str_enc = vector_bytes_str.encode()
    #             bytes_np_dec = vector_bytes_str_enc.decode(
    #                 'unicode-escape').encode('ISO-8859-1')[2:-1]
    #             array = np.frombuffer(bytes_np_dec)
    #             # array = np.frombuffer(audio_bytes)
    #             cleaned_audio = AudioSegment(array.tobytes())
    #             # os.remove(full_path)
    #             cleaned_audio.export(full_path, format="mp3")

    def prepare_download(self) -> os.path:
        path = os.path.join(DOWNLOADED_PATH, self.id)
        self.folder_path = path
        os.mkdir(path)
        if self.json_track:
            name = self.json_track["title"]
            with open(os.path.join(path, f"{name}.json"), "w+") as file:
                json.dump(self.json_track, file)
        else:
            logging.info(
                f"Track {self} does not have a json file associated with it at the time of saving. Saving regardless...")
        return path


class DataManager:
    # The ids of the trackl that are being created.... # so this class is "static" ? Do I really want that ? It should not matter....
    tracks: dict[Track] = {}

    def __init__(self):
        self.free_ids = set(os.listdir(DOWNLOADED_PATH))
        self.used_ids = set(os.listdir(USED_PATH))
        self.existing_ids = self.free_ids.union(self.used_ids)

    def track_exists(self, track: Track) -> bool:
        # this uses the id of the track, the one that I create
        return (track.id in self.existing_ids)

    def mark_used(self, ids: list[str]):
        for id in ids:
            # TODO.... copy folder from downloaded to used, then it will used by the producer


class UnexistingTrack (Exception):
    pass


def remove_extension(path: str) -> str:
    parts = path.split('.')
    del parts[-1]
    new = ''.join(parts)
    return new


def change_extension(filename: str, new_extension: str) -> str:
    parts = filename.split('.')
    parts[-1] = new_extension
    return ''.join(parts[:-1]) + '.'+parts[-1]


class Copier:
    def copy_converted(self):
        # file names ending in .wma :
        converted_files = os.listdir(CONVERTED_PATH)
        # folder names :
        existing_tracks = os.listdir(DOWNLOADED_PATH)
        logging.info("Copying converted files:")
        for file in tqdm(converted_files):
            # new_filename = change_extension(file, "mp3")
            old_filename = f'#{change_extension(file, "webm")}'
            try:
                os.remove(os.path.join(UNCONVERTED_PATH, old_filename
                                       ))
            except FileNotFoundError as e:
                logging.warning(
                    f"The file {old_filename} was removed already it seems... Moving on... Here is the error: {e}")
            track_folder = f"#{remove_extension(file)}"
            old_path: str = ""
            # try:
            old_path = os.path.join(CONVERTED_PATH, file)
            new_path = os.path.join(
                DOWNLOADED_PATH, track_folder, f"#{file}")
            move(old_path, new_path)
            # except Exception as e:
            #     logging.warning(f"Track {old_path} does not exist ! ")


def main():
    copier = Copier()
    copier.copy_converted()


if __name__ == "__main__":
    main()
