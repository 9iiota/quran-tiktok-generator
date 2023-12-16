import moviepy.editor as mpy

from enum import Enum
from typing import Union


class LanguageInfo:
    def __init__(self, abbreviation: str, translation_id: int):
        self.abbreviation = abbreviation
        self.translation_id = translation_id


class Language(Enum):
    ENGLISH = LanguageInfo(abbreviation="en", translation_id=20)
    DUTCH = LanguageInfo(abbreviation="nl", translation_id=235)


class ModeInfo:
    def __init__(
        self,
        shadow_color: tuple[int, int, int],
        shadow_opacity: float,
        verse_text_color: str,
        verse_translation_color: str = None,
        verse_number_color: str = None,
        reciter_name_color: str = None,
    ):
        self.shadow_color = shadow_color
        self.shadow_opacity = shadow_opacity
        self.verse_text_color = verse_text_color
        self.verse_translation_color = verse_translation_color or verse_text_color
        self.verse_number_color = verse_number_color or verse_text_color
        self.reciter_name_color = reciter_name_color or verse_text_color


class Mode(Enum):
    DARK = ModeInfo(shadow_color=(0, 0, 0), shadow_opacity=0.7, verse_text_color="rgb(255, 255, 255)")
    LIGHT = ModeInfo(shadow_color=(255, 255, 255), shadow_opacity=0.7, verse_text_color="rgb(0, 0, 0)")


class AccountInfo:
    def __init__(
        self,
        background_clips_directory_paths: list[str],
        language: Language,
        mode: Mode,
        verse_text_font_file_path: str,
        verse_translation_font_file_path: str,
        verse_number_font_file_path: str = None,
        reciter_name_font_file_path: str = None,
    ):
        self.background_clips_directory_paths = background_clips_directory_paths
        self.language = language
        self.mode = mode
        self.verse_text_font_file_path = verse_text_font_file_path
        self.verse_translation_font_file_path = verse_translation_font_file_path
        self.verse_number_font_file_path = verse_number_font_file_path or verse_translation_font_file_path
        self.reciter_name_font_file_path = reciter_name_font_file_path or verse_translation_font_file_path


class Account(Enum):
    QURAN_2_LISTEN = AccountInfo(
        background_clips_directory_paths=["Anime_Clips"],
        language=Language.ENGLISH,
        mode=Mode.DARK,
        verse_text_font_file_path="Fonts/Hafs.ttf",
        verse_translation_font_file_path="Fonts/Butler_Regular.otf",
    )
    RECITE_2_REFLECT = AccountInfo(
        background_clips_directory_paths=["Real_Clips, Real_Clips_2"],
        language=Language.ENGLISH,
        mode=Mode.DARK,
        verse_text_font_file_path="Fonts/Hafs.ttf",
        verse_translation_font_file_path="Fonts/Butler_Regular.otf",
    )
    HEARTFELTRECITATIONS = AccountInfo(
        background_clips_directory_paths=["Anime_Clips", "Real_Clips", "Real_Clips_2"],
        language=Language.ENGLISH,
        mode=Mode.DARK,
        verse_text_font_file_path="Fonts/Hafs.ttf",
        verse_translation_font_file_path="Fonts/Butler_Regular.otf",
    )


class VideoMode(Enum):
    VIDEO = 1
    IMAGE = 2


class VideoSettings:
    def __init__(
        self,
        allow_duplicate_background_clips: bool,
        allow_mirrored_background_clips: bool,
        background_clips_speed: float,
        video_dimensions: tuple[int, int],
        video_mode: VideoMode,
        single_background_video_path: str = None,
        single_background_video_horizontal_offset: int = None,
        single_background_video_vertical_offset: int = None,
    ) -> None:
        self.allow_duplicate_background_clips = allow_duplicate_background_clips
        self.allow_mirrored_background_clips = allow_mirrored_background_clips
        self.background_clips_speed = background_clips_speed
        self.video_dimensions = video_dimensions
        self.video_mode = video_mode
        self.single_background_video = single_background_video_path
        self.single_background_video_horizontal_offset = single_background_video_horizontal_offset
        self.single_background_video_vertical_offset = single_background_video_vertical_offset


class TimeModifiers:
    def __init__(self, time_modifier: float, end_time_modifier: float, start_time_modifier: float = None) -> None:
        self.time_modifier = time_modifier
        self.end_time_modifier = end_time_modifier
        self.start_time_modifier = start_time_modifier


class AudioSettings:
    def __init__(
        self,
        audio_mp3_file_path: str,
        chapter_number: int,
        start_to_end_timestamp_verse_range: tuple[int, int],
    ) -> None:
        self.audio_mp3_file_path = audio_mp3_file_path
        self.chapter_number = chapter_number
        self.start_to_end_timestamp_verse_range = start_to_end_timestamp_verse_range


class CSVColumnNames:
    def __init__(self, verse_number: str, verse_text: str, timestamp: str) -> None:
        self.verse_number = verse_number
        self.verse_text = verse_text
        self.timestamp = timestamp


class TextClipInfo:
    def __init__(
        self,
        text_background_color: str,
        text_fade_duration: float,
        text_font_size: int,
        text_method: str,
        text_position: tuple[Union[float, str], Union[float, str]],
        text_size: tuple[Union[float, None], Union[float, None]],
    ):
        self.text_background_color = text_background_color
        self.text_fade_duration = text_fade_duration
        self.text_font_size = text_font_size
        self.text_method = text_method
        self.text_position = text_position
        self.text_size = text_size

    def create_text_clip(self, color: str, duration: float, font: str, text: str):
        return (
            mpy.TextClip(
                bg_color=self.text_background_color,
                color=color,
                font=font,
                fontsize=self.text_font_size,
                method=self.text_method,
                size=self.text_size,
                txt=text,
            )
            .set_duration(duration)
            .set_position(self.text_position, relative=True)
            .crossfadein(self.text_fade_duration)
            .crossfadeout(self.text_fade_duration)
        )
