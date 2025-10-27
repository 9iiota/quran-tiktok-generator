from models import Account, ColorModes, Languages
from enum import Enum


class Accounts(Enum):
    QURAN_2_LISTEN = Account(
        clip_directories=["assets/background_clips/anime"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="assets/fonts/Hafs.ttf",
        verse_translation_font_file="assets/fonts/Butler_Regular.otf",
    )
    VERSES_IN_THE_WIND = Account(
        clip_directories=["Background_Clips/Ghost_of_Tsushima"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
    DUTCH = Account(
        clip_directories=["Background_Clips/Anime"],
        language=Languages.DUTCH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
    RECITE_2_REFLECT = Account(
        clip_directories=["Background_Clips/Real", "Background_Clips/Real_2"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
    HEARTFELTRECITATIONS = Account(
        clip_directories=[
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
        clip_directories=["Background_Clips/Real", "Background_Clips/Real_2"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verse_text_font_file="Fonts/Hafs.ttf",
        verse_translation_font_file="Fonts/Butler_Regular.otf",
    )
