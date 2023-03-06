import os
import logging
from tqdm import tqdm
from pathlib import Path

from settings import UNCONVERTED_PATH, CONVERTED_PATH, DOWNLOADED_PATH


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
    return ''.join(parts)


class Copier:
    def copy_converted(self):
        # file names ending in .wma :
        converted_files = os.listdir(CONVERTED_PATH)
        # folder names :
        existing_tracks = os.listdir(DOWNLOADED_PATH)
        logging.info("Copying converted files:")
        for file in tqdm(converted_files):
            new_filename = change_extension(file, "mp3")
            try:
                os.remove(os.path(UNCONVERTED_PATH, new_filename
                                  ))
            except FileNotFoundError as e:
                logging.warning(
                    "The file {file} was removed already it seems... Moving on... Here is the error: {e}")
            track_folder = remove_extension(file)
            try:
                Path(os.path.join(converted_files, file)).rename(
                    os.path.join(DOWNLOADED_PATH, track_folder, new_filename))
            except Exception as e:
                logging.warning(f"Track {track_folder} does not exist ! ")


def main():
    copier = Copier()
    copier.copy_converted()


if __name__ == "__main__":
    main()
