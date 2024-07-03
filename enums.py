from classes import Account, ColorModes, Languages
from enum import Enum


class Accounts(Enum):
    QURAN_2_LISTEN = Account(
        background_clips_directories=["Background_Clips/Anime"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
    DUTCH = Account(
        background_clips_directories=["Background_Clips/Anime"],
        language=Languages.DUTCH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
    RECITE_2_REFLECT = Account(
        background_clips_directories=["Background_Clips/Real", "Background_Clips/Real_2"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
    HEARTFELTRECITATIONS = Account(
        background_clips_directories=[
            "Background_Clips/Anime",
            "Background_Clips/Real",
            "Background_Clips/Real_2",
        ],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
    QURANIC_TIKTOKS = Account(
        background_clips_directories=["Background_Clips/Real", "Background_Clips/Real_2"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
