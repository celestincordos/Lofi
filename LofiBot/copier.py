import os
import logging
from tqdm import tqdm
from pathlib import Path
from shutil import move

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
