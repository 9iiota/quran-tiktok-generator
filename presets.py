from enum import Enum


class Preset:
    def __init__(self, audio_directory_path: str, output_video_verse_range: str) -> None:
        self.audio_directory_path = audio_directory_path
        self.output_video_verse_range = output_video_verse_range


class Presets(Enum):
    ABDUL_RAHMAN_MOSSAD_AL_ADIYAT_1_11 = Preset(r"Surahs\Abdul Rahman Mossad - Al-'Adiyat (100.1-11)", (1, 11))
