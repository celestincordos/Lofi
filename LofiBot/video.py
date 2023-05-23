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
        logging.info("Compiling audio files...")
        for filename in tqdm(audio_files):
            full_filename = os.path.join(folder_name, filename)
            current_track = AudioSegment.from_mp3(full_filename)
            if audio is None:
                audio = current_track
            else:
                audio = audio + current_track
        output_name = os.path.join(folder_name, "audio.mp3")
        audio.export(output_name, format="mp3")

    def _compile_video(self, image_file: str, folder_name: str, audio_output: str, video_output: str) -> None:
        bashCommand = f"ffmpeg -hwaccel cuda  -loop 1 -i {os.path.join (folder_name,image_file)} -i {audio_output} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -filter:v fps=1 {video_output}"
        os.system(bashCommand)

    def _move_files(self, base_folder_name: str, audio_output: str, video_output: str) -> None:
        destination = os.path.join(EDITS_PATH, base_folder_name)
        os.mkdir(destination)
        move(audio_output, destination)
        move(video_output, destination)

    def compile_folder(self, folder_name: str, base_folder_name: str):
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
        audio_output = os.path.join(folder_name, 'audio.mp3')
        video_output = os.path.join(folder_name, 'out.mp4')
        self._compile_audio(audio_files=audio_files, folder_name=folder_name)
        self._compile_video(image_file=image_file, folder_name=folder_name,
                            audio_output=audio_output, video_output=video_output)
        self._move_files(base_folder_name=base_folder_name,
                         audio_output=audio_output, video_output=video_output)
        return

    def make_edits(self):
        dirs = set(os.listdir(PRODUCED_PATH))
        existing_dirs = set(os.listdir(EDITS_PATH))
        logging.info(f"Making the edits for {len(dirs)} directories")

        compile_dirs = dirs - existing_dirs
        length = len(compile_dirs)
        for i, folder_name in enumerate(compile_dirs):

            logging.info(f"Compiling folder {i}/{length}")
            full_folder_name = os.path.join(PRODUCED_PATH, folder_name)
            self.compile_folder(folder_name=full_folder_name,
                                base_folder_name=folder_name)

        return


def main():
    logging.basicConfig(level=logging.INFO)
    editor = Editor()
    editor.make_edits()


if __name__ == "__main__":
    main()
