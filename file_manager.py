import os
from models import ColumnHeaders

class FileManager:
    def __init__(
        self, audio_file: str, output_file_name: str, verses_file_path: str, column_headers: ColumnHeaders, output_file_path: str=None
    ):
        self.audio_file = audio_file
        if not os.path.exists(self.audio_file):
            raise FileNotFoundError(f"File {self.audio_file} not found")
        self.audio_file_directory = os.path.dirname(self.audio_file)

        if output_file_path:
            self.output_file_path = output_file_path.replace("\\", "/")
            try:
                self.output_file_directory = os.path.dirname(self.output_file_path)
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    f"Directory {self.output_file_directory} not found"
                ) from e
        else:
            self.output_file_directory = os.path.join(
                self.audio_file_directory, "Videos"
            )
            self.output_file_path = os.path.join(
                self.output_file_directory, output_file_name
            )
        if not os.path.isdir(self.output_file_directory):
            os.makedirs(self.output_file_directory)

        self.verses_file_path = verses_file_path.replace("\\", "/")
        if not os.path.exists(self.verses_file_path):
            