import logging
import os
from tqdm import tqdm
from pydub import AudioSegment
from shutil import move

from settings import PRODUCED_PATH, EDITS_PATH


class Editor:

    def _compile_audio(self, audio_files: list[str], folder_name: str):
        audio_files.sort()
        audio: AudioSegment | None = None
        logging.log("Compiling audio files...")
        for filename in tqdm(audio_files):
            full_filename = os.path.join(folder_name, filename)
            current_track = AudioSegment.from_mp3(full_filename)
            if audio is None:
                audio = current_track
            else:
                audio = audio + current_track
        output_name = os.path.join(folder_name, "audio.mp3")
        audio.export(output_name, format="mp3")

    def _compile_video(self, image_file: str, folder_name: str) -> None:
        bashCommand = f"ffmpeg -loop 1 -i {os.path.join (folder_name,image_file)} -i {os.path.join(folder_name, 'audio.mp3')} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {os.path.join(folder_name, 'out.mp4')}"
        os.system(bashCommand)

    def _move_folder(folder_name: str) -> None:
        move(folder_name, EDITS_PATH)

    def compile_folder(self, folder_name: str):
        audio_files: list[str] = []
        image_file: str
        all_files = os.listdir(folder_name)
        for file in all_files:
            if file.endswith(".mp3"):
                audio_files.append(file)
            elif file.endswith(".png"):
                image_file = file
            else:
                logging.warning("What is file {file} in folder {folder}??")
        self._compile_audio(audio_files=audio_files, folder_name=folder_name)
        self._compile_video(image_file=image_file, folder_name=folder_name)
        self._move_folder(folder_name)
        return

    def make_edits(self):
        dirs = os.listdir(PRODUCED_PATH)
        logging.info(f"Making the edits for {len(dirs)} directories")
        length = len(dirs)
        for i, folder_name in enumerate(dirs):
            logging.info("Compiling folder {i}/{length}")
            full_folder_name = os.path.join(PRODUCED_PATH, folder_name)
            self.compile_folder(folder_name=full_folder_name)

        return


def main():
    logging.basicConfig(level=logging.INFO)
    editor = Editor()
    editor.make_edits()


if __name__ == "__main__":
    main()
