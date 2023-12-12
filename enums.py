from enum import Enum


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
        verse_translation_color: str,
        verse_number_color: str,
        reciter_name_color: str,
    ):
        """
        shadow_color: (r, g, b)
        shadow_opacity: 0.0 - 1.0
        verse_text_color: "rgb(r, g, b)"
        verse_translation_color: "rgb(r, g, b)"
        verse_number_color: "rgb(r, g, b)"
        reciter_name_color: "rgb(r, g, b)"
        """

        self.shadow_color = shadow_color
        self.shadow_opacity = shadow_opacity
        self.verse_text_color = verse_text_color
        self.verse_translation_color = verse_translation_color
        self.verse_number_color = verse_number_color
        self.reciter_name_color = reciter_name_color


class Mode(Enum):
    DARK = ModeInfo(
        shadow_color=(0, 0, 0),
        shadow_opacity=0.7,
        verse_text_color="rgb(255, 255, 255)",
        verse_translation_color="rgb(255, 255, 255)",
        verse_number_color="rgb(255, 255, 255)",
        reciter_name_color="rgb(255, 255, 255)",
    )
    LIGHT = ModeInfo(
        shadow_color=(255, 255, 255),
        shadow_opacity=0.7,
        verse_text_color="rgb(0, 0, 0)",
        verse_translation_color="rgb(0, 0, 0)",
        verse_number_color="rgb(0, 0, 0)",
        reciter_name_color="rgb(0, 0, 0)",
    )


class AccountInfo:
    def __init__(
        self,
        background_clips_directory_paths: list[str],
        language: Language,
        mode: Mode,
        verse_translation_font_file_path: str,
    ):
        self.background_clips_directory_paths = background_clips_directory_paths
        self.language = language
        self.mode = mode
        self.verse_translation_font_file_path = verse_translation_font_file_path


class Account(Enum):
    QURAN_2_LISTEN = AccountInfo(["Anime_Clips"], Language.ENGLISH, Mode.DARK, "Fonts/Butler_Regular.otf")
    RECITE_2_REFLECT = AccountInfo(
        ["Real_Clips, Real_Clips_2"], Language.ENGLISH, Mode.DARK, "Fonts/Butler_Regular.otf"
    )
    HEARTFELTRECITATIONS = AccountInfo(
        ["Anime_Clips", "Real_Clips", "Real_Clips_2"], Language.ENGLISH, Mode.DARK, "Fonts/Butler_Regular.otf"
    )
