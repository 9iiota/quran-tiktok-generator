import moviepy.editor as mpy

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


@dataclass
class ColorMode:
    shadow_color: tuple[int, int, int]
    shadow_opacity: float
    verse_text_color: str
    verse_translation_color: Optional[str] = None
    verse_number_color: Optional[str] = None
    reciter_name_color: Optional[str] = None

    def __post_init__(self):
        self.verse_translation_color = self.verse_translation_color or self.verse_text_color
        self.verse_number_color = self.verse_number_color or self.verse_text_color
        self.reciter_name_color = self.reciter_name_color or self.verse_text_color


@dataclass
class Language:
    abbreviation: str
    translation_id: int


@dataclass
class Account:
    background_clips_directories: list[str]
    language: Language
    mode: ColorMode
    verse_text_font_file: str
    verse_translation_font_file: str
    verse_number_font_file: Optional[str] = None
    reciter_name_font_file: Optional[str] = None

    def __post_init__(self):
        self.verse_number_font_file = self.verse_number_font_file or self.verse_translation_font_file
        self.reciter_name_font_file = self.reciter_name_font_file or self.verse_translation_font_file


@dataclass
class AudioSettings:
    audio_mp3_file: str
    chapter_number: int
    audio_verse_range: tuple[int, int]


@dataclass
class CSVColumnNames:
    verse_number: str
    verse_text: str
    timestamp: str


@dataclass
class TextClipInfo:
    text_background_color: str
    text_fade_duration: float
    text_font_size: int
    text_method: str
    text_position: tuple[Union[float, str], Union[float, str]]
    text_size: tuple[Union[float, None], Union[float, None]]

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


@dataclass
class TimeModifiers:
    time_modifier: float
    end_time_modifier: float
    start_time_modifier: Optional[float] = None


class VideoModes(Enum):
    VIDEO = 1
    IMAGE = 2


@dataclass
class VideoSettings:
    allow_duplicate_background_clips: bool
    allow_mirrored_background_clips: bool
    background_clips_speed: float
    minimal_background_clip_duration: float
    video_dimensions: tuple[int, int]
    video_mode: VideoModes


@dataclass
class OptionalVideoSettings:
    single_background_video: Optional[str] = None
    single_background_video_horizontal_offset: Optional[int] = None
    single_background_video_vertical_offset: Optional[int] = None
    video_map: Optional[dict[str, list[list[str, float, int, str]]]] = None


class ColorModes(Enum):
    DARK = ColorMode(shadow_color=(0, 0, 0), shadow_opacity=0.7, verse_text_color="rgb(255, 255, 255)")
    LIGHT = ColorMode(shadow_color=(255, 255, 255), shadow_opacity=0.7, verse_text_color="rgb(0, 0, 0)")


class Languages(Enum):
    ENGLISH = Language(abbreviation="en", translation_id=20)
    DUTCH = Language(abbreviation="nl", translation_id=235)
