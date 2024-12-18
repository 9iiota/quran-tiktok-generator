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
        self.verse_translation_color = (
            self.verse_translation_color or self.verse_text_color
        )
        self.verse_number_color = self.verse_number_color or self.verse_text_color
        self.reciter_name_color = self.reciter_name_color or self.verse_text_color


@dataclass
class Language:
    abbreviation: str
    translation_id: int


@dataclass
class Account:
    clipDirectories: list[str]
    language: Language
    mode: ColorMode
    verseTextFontFile: str
    verseTranslationFontFile: str
    verseNumberFontFile: Optional[str] = None
    reciterNameFontFile: Optional[str] = None

    def __post_init__(self):
        self.verseNumberFontFile = (
            self.verseNumberFontFile or self.verseTranslationFontFile
        )
        self.reciterNameFontFile = (
            self.reciterNameFontFile or self.verseTranslationFontFile
        )


@dataclass
class AudioSettings:
    audioFile: str
    chapterNumber: int
    verseRange: tuple[int, int]


@dataclass
class ColumnHeaders:
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
    timeModifier: float
    endTimeModifier: float
    startTimeModifier: Optional[float] = None


class VideoModes(Enum):
    VIDEO = 1
    IMAGE = 2


@dataclass
class VideoSettings:
    allowDuplicateClips: bool
    allowMirroredClips: bool
    clipSpeed: float
    minimumClipDuration: float
    videoDimensions: tuple[int, int]
    videoMode: VideoModes


@dataclass
class AdditionalVideoSettings:
    startLine: Optional[int] = None
    endLine: Optional[int] = None
    backgroundVideo: Optional[str] = None
    backgroundVideoHorizontalOffset: Optional[int] = None
    backgroundVideoVerticalOffset: Optional[int] = None
    videoMap: Optional[dict[str, list[list[str, float, int, str]]]] = None


class ColorModes(Enum):
    DARK = ColorMode(
        shadow_color=(0, 0, 0),
        shadow_opacity=0.7,
        verse_text_color="rgb(255, 255, 255)",
    )
    LIGHT = ColorMode(
        shadow_color=(255, 255, 255),
        shadow_opacity=0.7,
        verse_text_color="rgb(0, 0, 0)",
    )


class Languages(Enum):
    ENGLISH = Language(abbreviation="en", translation_id=20)
    DUTCH = Language(abbreviation="nl", translation_id=235)
