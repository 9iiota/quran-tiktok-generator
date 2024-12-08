from classes import Account, ColorModes, Languages
from enum import Enum


class Accounts(Enum):
    QURAN_2_LISTEN = Account(
        clipDirectories=["Background_Clips/Anime"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verseTextFontFile="Fonts/Hafs.ttf",
        verseTranslationFontFile="Fonts/Butler_Regular.otf",
    )
    DUTCH = Account(
        clipDirectories=["Background_Clips/Anime"],
        language=Languages.DUTCH,
        mode=ColorModes.DARK,
        verseTextFontFile="Fonts/Hafs.ttf",
        verseTranslationFontFile="Fonts/Butler_Regular.otf",
    )
    RECITE_2_REFLECT = Account(
        clipDirectories=["Background_Clips/Real", "Background_Clips/Real_2"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verseTextFontFile="Fonts/Hafs.ttf",
        verseTranslationFontFile="Fonts/Butler_Regular.otf",
    )
    HEARTFELTRECITATIONS = Account(
        clipDirectories=[
            "Background_Clips/Anime",
            "Background_Clips/Real",
            "Background_Clips/Real_2",
        ],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verseTextFontFile="Fonts/Hafs.ttf",
        verseTranslationFontFile="Fonts/Butler_Regular.otf",
    )
    QURANIC_TIKTOKS = Account(
        clipDirectories=["Background_Clips/Real", "Background_Clips/Real_2"],
        language=Languages.ENGLISH,
        mode=ColorModes.DARK,
        verseTextFontFile="Fonts/Hafs.ttf",
        verseTranslationFontFile="Fonts/Butler_Regular.otf",
    )
