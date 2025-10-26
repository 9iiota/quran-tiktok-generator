from audio_controller import AudioController
from file_controller import FileController


class VideoManager:
    def __init__(
        self, audio_controller: AudioController, file_controller: FileController
    ) -> None:
        self.audio_controller = audio_controller
        self.file_controller = file_controller

    def create_video(self):
        pass

if __name__ == "__main__":
    audio_controller = AudioController(