from models import UserPreferences, ColorModes, Languages
from enum import Enum


class Accounts(Enum):
    QURAN_2_LISTEN = UserPreferences(
        clip_directories=["assets/background_clips/anime"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        arabic_font_file_path="assets/fonts/Hafs.ttf",
        translation_font_file_path="assets/fonts/Butler_Regular.otf",
    )
    VERSES_IN_THE_WIND = UserPreferences(
        clip_directories=["Background_Clips/Ghost_of_Tsushima"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        arabic_font_file_path="Fonts/Hafs.ttf",
        translation_font_file_path="Fonts/Butler_Regular.otf",
    )
    DUTCH = UserPreferences(
        clip_directories=["Background_Clips/Anime"],
        language=Languages.DUTCH,
        mode=ColorModes.DARK,
        arabic_font_file_path="Fonts/Hafs.ttf",
        translation_font_file_path="Fonts/Butler_Regular.otf",
    )
    RECITE_2_REFLECT = UserPreferences(
        clip_directories=["Background_Clips/Real", "Background_Clips/Real_2"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        arabic_font_file_path="Fonts/Hafs.ttf",
        translation_font_file_path="Fonts/Butler_Regular.otf",
    )
    HEARTFELTRECITATIONS = UserPreferences(
        clip_directories=[
            "Background_Clips/Anime",
            "Background_Clips/Real",
            "Background_Clips/Real_2",
        ],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        arabic_font_file_path="Fonts/Hafs.ttf",
        translation_font_file_path="Fonts/Butler_Regular.otf",
    )
    QURANIC_TIKTOKS = UserPreferences(
        clip_directories=["Background_Clips/Real", "Background_Clips/Real_2"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        arabic_font_file_path="Fonts/Hafs.ttf",
        translation_font_file_path="Fonts/Butler_Regular.otf",
    )
