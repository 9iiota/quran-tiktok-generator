import csv
import moviepy.editor as mpy
import os
import random
import requests
import uuid

from bs4 import BeautifulSoup
from colorama import Fore, Style
from compact_json import EolStyle, Formatter
from datetime import datetime, timedelta
from enum import Enum
from plyer import notification
from pyquran import quran

from Tiktok_uploader import uploadVideo

ARABIC_FONT = "Fonts/Hafs.ttf"
MINIMAL_CLIP_DURATION = 0.75

# TODO: Add support for clips shorter than final clip with still frames
# TODO: Add support for background clips disjoint from audio timings
# TODO: Fix pictures mode
# TODO: FIX VERTICAL OFFSET
# TODO: ADD DURATIONS IN VIDEO MAP AND UNCOMMENT CODE IN GET_VALID_BACKGROUND_CLIPS


def main() -> None:
    tiktok = TikToks(
        language=LANGUAGES.DUTCH,
    )
    tiktok.abdul_rahman_mossad_al_adiyat_1_11()
    tiktok.run()


def test():
    pass

    # # Get only the user-defined methods
    # user_defined_methods = [
    #     func
    #     for func in dir(TikToks)
    #     if callable(getattr(TikToks, func)) and not func.startswith("__") and not "run" in func
    # ]

    # return user_defined_methods


class ACCOUNTS(Enum):
    QURAN_2_LISTEN = {"english_font": "Fonts/Butler_Regular.otf"}  # crazyshocklight@hotmail.com
    LOVE_QURAN77 = {"english_font": "Fonts/Sk-Modernist-Regular.otf"}  # crazyshocklight2@gmail.com
    QURANIC_TIKTOKS = {"english_font": "Fonts/FreshStart.otf"}  # crazyshocky@hotmail.com


class LANGUAGES(Enum):
    ENGLISH = "en"
    DUTCH = "nl"


class MODES(Enum):
    DARK = {
        "shadow_color": (0, 0, 0),
        "verse_text_color": "rgb(255, 255, 255)",
        "verse_translation_color": "rgb(255, 255, 255)",
    }
    LIGHT = {
        "shadow_color": (255, 255, 255),
        "verse_text_color": "rgb(0, 0, 0)",
        "verse_translation_color": "rgb(0, 0, 0)",
    }


class TikToks:
    def __init__(
        self,
        directory_path: str = None,
        output_file_name: str = None,
        chapter_csv_file_path: str = None,
        start_line: int = 1,
        end_line: int = None,
        time_modifier: float = 0.0,
        start_time_modifier: float = 0.0,
        end_time_modifier: float = 0.0,
        chapter: int = None,
        start_verse: int = None,
        end_verse: int = None,
        language: LANGUAGES = LANGUAGES.ENGLISH,
        background_clips_directory_paths: list[str] = ["Anime_Clips", "Anime_Clips_2"],
        single_background_clip: str = None,
        single_background_clip_horizontal_offset: int = None,
        single_background_clip_vertical_offset: int = None,
        video_map: dict = None,
        pictures_mode: bool = False,
        allow_duplicate_background_clips: bool = False,
        allow_mirrored_background_clips: bool = False,
        video_dimensions: tuple[int, int] = (576, 1024),
        background_clips_speed: float = 1.0,
        shadow_opacity: float = 0.7,
        account: ACCOUNTS = ACCOUNTS.QURAN_2_LISTEN,
        mode: MODES = MODES.DARK,
    ) -> None:
        self.directory_path = directory_path
        self.output_file_name = output_file_name
        self.chapter_csv_file_path = chapter_csv_file_path
        self.start_line = start_line
        self.end_line = end_line
        self.time_modifier = time_modifier
        self.start_time_modifier = start_time_modifier
        self.end_time_modifier = end_time_modifier
        self.chapter = chapter
        self.start_verse = start_verse
        self.end_verse = end_verse
        self.language = language
        self.background_clips_directory_paths = background_clips_directory_paths
        self.single_background_clip = single_background_clip
        self.single_background_clip_horizontal_offset = single_background_clip_horizontal_offset
        self.single_background_clip_vertical_offset = single_background_clip_vertical_offset
        self.video_map = video_map
        self.pictures_mode = pictures_mode
        self.allow_duplicate_background_clips = allow_duplicate_background_clips
        self.allow_mirrored_background_clips = allow_mirrored_background_clips
        self.video_dimensions = video_dimensions
        self.background_clips_speed = background_clips_speed
        self.shadow_opacity = shadow_opacity
        self.account = account
        self.mode = mode

    def run(self) -> None:
        if self.chapter is None:
            self.chapter_csv_file_path = os.path.join(self.directory_path, "chapter.csv")

        self.output_file_name = f"{self.output_file_name} {self.language.value} {(self.account.name).lower()} {datetime.now().strftime('%H.%M.%S %d-%m-%Y')}"

        create_tiktok(
            directory_path=self.directory_path,
            output_file_name=self.output_file_name,
            chapter_csv_file_path=self.chapter_csv_file_path,
            start_line=self.start_line,
            end_line=self.end_line,
            time_modifier=self.time_modifier,
            start_time_modifier=self.start_time_modifier,
            end_time_modifier=self.end_time_modifier,
            chapter=self.chapter,
            start_verse=self.start_verse,
            end_verse=self.end_verse,
            language=self.language,
            background_clips_directory_paths=self.background_clips_directory_paths,
            background_video=self.single_background_clip,
            background_video_horizontal_offset=self.single_background_clip_horizontal_offset,
            background_video_vertical_offset=self.single_background_clip_vertical_offset,
            video_map=self.video_map,
            pictures_mode=self.pictures_mode,
            allow_duplicate_background_clips=self.allow_duplicate_background_clips,
            allow_mirrored_background_clips=self.allow_mirrored_background_clips,
            video_dimensions=self.video_dimensions,
            background_clips_speed=self.background_clips_speed,
            shadow_opacity=self.shadow_opacity,
            account=self.account,
            mode=self.mode,
        )

    def abdul_rahman_mossad_al_adiyat_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Al-'Adiyat by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-'Adiyat (100.1-11)"
        self.output_file_name = "Al-'Adiyat (100.1-11)"
        self.chapter = 100
        self.start_verse = 1
        self.end_verse = 11
        self.time_modifier = -0.2

    def abdul_rahman_mossad_al_ankabut_54_60(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 54-60 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-'Ankabut (29.53-64)"
        self.output_file_name = "Al-'Ankabut (29.54-60)"
        self.start_line = 3
        self.end_line = 27
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_al_ankabut_54_57(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 54-57 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-'Ankabut (29.53-64)"
        self.output_file_name = "Al-'Ankabut (29.54-57)"
        self.start_line = 3
        self.end_line = 15
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_al_ankabut_56_57(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-57 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-'Ankabut (29.53-64)"
        self.output_file_name = "Al-'Ankabut (29.56-57)"
        self.start_line = 10
        self.end_line = 13
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_maryam_93_98(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 93-98 of Surah Maryam by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Maryam (19.65-98)"
        self.output_file_name = "Maryam (19.93-98)"
        self.start_line = 29
        self.end_line = 45
        self.time_modifier = -0.2

    def abdul_rahman_mossad_al_ghashiyah_10_26(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 10-26 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-Ghashiyah (88.1-26)"
        self.output_file_name = "Al-Ghashiyah (88.10-26)"
        self.start_line = 14
        self.time_modifier = -0.2

    def abdul_rahman_mossad_al_ghashiyah_10_12(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 10-12 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-Ghashiyah (88.1-26)"
        self.output_file_name = "Al-Ghashiyah (88.10-12)"
        self.start_line = 14
        self.end_line = 16
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

        def abdul_rahman_mossad_al_muzzammil_6_13(self) -> None:
            """
            Modifies the parameters of the class for a TikTok video for verses 6-13 of Surah Al-Muzzammil by Abdul Rahman Mossad
            """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-Muzzammil (73.1-20)"
        self.output_file_name = "Al-Muzzammil (73.6-13)"
        self.start_line = 7
        self.end_line = 26
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_al_muzzammil_14_18(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-18 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-Muzzammil (73.1-20)"
        self.output_file_name = "Al-Muzzammil (73.14-18)"
        self.start_line = 27
        self.end_line = 38
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_al_muzzammil_14_15(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-15 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Al-Muzzammil (73.1-20)"
        self.output_file_name = "Al-Muzzammil (73.14-15)"
        self.start_line = 27
        self.end_line = 32
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    ######################################################################################################################################################
    ######################################################################################################################################################
    ######################################################################################################################################################
    ######################################################################################################################################################
    ######################################################################################################################################################
    ######################################################################################################################################################

    def abdul_rahman_mossad_maryam_93_94(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 93-94 of Surah Maryam by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Maryam (19.65-98)"
        self.output_file_name = "Maryam (19.93-94)"
        self.start_line = 29
        self.end_line = 32
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_yunus_7_10(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 7-10 of Surah Yunus by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Yunus (10.3-25)"
        self.output_file_name = "Yunus (10.7-10)"
        self.start_line = 5
        self.end_line = 22
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_yunus_17_20(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 17-20 of Surah Yunus by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - Yunus (10.3-25)"
        self.output_file_name = "Yunus (10.17-20)"
        self.start_line = 29
        self.end_line = 50
        self.time_modifier = -0.2
        self.end_time_modifier = -0.2

    def ahmed_khedr_taha_14_16(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-16 of Surah Taha by Ahmed Khedr
        """

        self.directory_path = r"Surahs\Ahmed Khedr - 20 - Taha"
        self.output_file_name = f"{(self.account.name).lower()}_14-16_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Ahmed Khedr - 20 - Taha\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Ahmed Khedr - 20 - Taha\chapter_translation.txt"

    def fatih_seferagic_ayatul_kursi_255(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 255 of Surah Al-Baqarah by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi"
        self.output_file_name = f"{(self.account.name).lower()}_255_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi\chapter_translation.txt"

    def fatih_seferagic_an_nisa_155_160(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 155-160 of Surah An-Nisa by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 4 - An-Nisa"
        self.output_file_name = f"{(self.account.name).lower()}_155-160_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 4 - An-Nisa\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 4 - An-Nisa\chapter_translation.txt"

    def fatih_seferagic_an_nur_35(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 35 of Surah An-Nur by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 24 - An-Nur"
        self.output_file_name = f"{(self.account.name).lower()}_35_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 24 - An-Nur\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 24 - An-Nur\chapter_translation.txt"

    def fatih_seferagic_al_hujurat_10(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 10 of Surah Al-Hujurat by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - Al-Hujurat (49.10)"
        self.output_file_name = f"{(self.account.name).lower()} Al-Hujurat (49.10) {self.language.value} {str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - Al-Hujurat (49.10)\chapter_text.txt"
        self.chapter_translation_file_path = (
            rf"Surahs\Fatih Seferagic - Al-Hujurat (49.10)\chapter_translation_{self.language.value}.txt"
        )
        self.verse_counter_file_path = r"Surahs\Fatih Seferagic - Al-Hujurat (49.10)\verse_counter.txt"
        self.time_modifier = -0.2

    def fatih_seferagic_al_hashr_21_24(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 21-24 of Surah Al-Hashr by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 59 - Al-Hashr"
        self.output_file_name = f"{(self.account.name).lower()}_21-24_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 59 - Al-Hashr\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 59 - Al-Hashr\chapter_translation.txt"

    def mansour_as_salimi_maryam_27_33(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 27-33 of Surah Maryam by Mansour As Salimi
        """

        self.directory_path = r"Surahs\Mansour As Salimi - 19 - Maryam"
        self.output_file_name = f"{(self.account.name).lower()}_27-33_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Mansour As Salimi - 19 - Maryam\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Mansour As Salimi - 19 - Maryam\chapter_translation.txt"

    def mansour_as_salimi_yusuf_1_5(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-5 of Surah Yusuf by Mansour As Salimi
        """

        self.directory_path = r"Surahs\Mansour As Salimi - 12 - Yusuf"
        self.output_file_name = f"{(self.account.name).lower()}_1-5_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Mansour As Salimi - 12 - Yusuf\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Mansour As Salimi - 12 - Yusuf\chapter_translation.txt"

    def mostafa_shaibani_al_qiyamah_20_27(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 20-27 of Surah Al-Qiyamah by Mostafa Shaibani
        """

        self.directory_path = r"Surahs\Mostafa Shaibani - Al-Qiyamah (75.20-27)"
        self.output_file_name = (
            f"{(self.account.name).lower()} Al-Qiyamah (75.20-27) {str(uuid.uuid4()).split('-')[-1]}"
        )
        self.chapter_text_file_path = r"Surahs\Mostafa Shaibani - Al-Qiyamah (75.20-27)\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Mostafa Shaibani - Al-Qiyamah (75.20-27)\chapter_translation.txt"
        self.verse_counter_file_path = r"Surahs\Mostafa Shaibani - Al-Qiyamah (75.20-27)\verse_counter.txt"

    def muhammad_al_luhaidan_al_baqarah_273_274(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 273-274 of Surah Al-Baqarah by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 2 - Al-Baqarah"
        self.output_file_name = f"{(self.account.name).lower()}_273-274_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 2 - Al-Baqarah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 2 - Al-Baqarah\chapter_translation.txt"

    def muhammad_al_luhaidan_al_anam_27_30(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 27-30 of Surah Al-An'am by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am"
        self.output_file_name = f"{(self.account.name).lower()}_27-30_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am\chapter_translation.txt"

    def muhammad_al_luhaidan_maryam_85_92(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 85-92 of Surah Maryam by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 19 - Maryam"
        self.output_file_name = f"{(self.account.name).lower()}_85-92_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 19 - Maryam\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 19 - Maryam\chapter_translation.txt"

    def muhammad_al_luhaidan_taha_105_108(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 105-108 of Surah Taha by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 20 - Taha"
        self.output_file_name = f"{(self.account.name).lower()}_105-108_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 20 - Taha\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 20 - Taha\chapter_translation.txt"

    def muhammad_al_luhaidan_al_furqan_74(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 74 of Surah Al-Furqan by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan"
        self.output_file_name = f"{(self.account.name).lower()}_72-77_{str(uuid.uuid4()).split('-')[-1]}"
        self.start_line = 8
        self.end_line = 11
        self.start_time_modifier = 0.1
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan\chapter_translation.txt"

    def muhammad_al_luhaidan_al_furqan_72_77(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 72-77 of Surah Al-Furqan by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan"
        self.output_file_name = f"{(self.account.name).lower()}_72-77_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan\chapter_translation.txt"

    def muhammad_al_luhaidan_al_furqan_26_30(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 25-30 of Surah Al-Furqan by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan - 2"
        self.output_file_name = f"{(self.account.name).lower()}_26-30_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan - 2\chapter_text.txt"
        self.chapter_translation_file_path = (
            r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan - 2\chapter_translation.txt"
        )

    def muhammad_al_luhaidan_al_haqqah_29_33(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 29-33 of Surah Al-Haqqah by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 69 - Al-Haqqah"
        self.output_file_name = f"{(self.account.name).lower()}_29-33_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 69 - Al-Haqqah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 69 - Al-Haqqah\chapter_translation.txt"

    def muhammad_al_luhaidan_al_insan_20_22(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 20-22 of Surah Al-Insan by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 76 - Al-Insan"
        self.output_file_name = f"{(self.account.name).lower()}_20-22_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 76 - Al-Insan\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 76 - Al-Insan\chapter_translation.txt"

    def muhammad_al_luhaidan_al_ahzab_23_24(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 23-24 of Surah Al-Ahzab by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - Al-Ahzab (33.23-24)"
        self.output_file_name = f"{(self.account.name).lower()} Al-Ahzab (33.23-24) {str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - Al-Ahzab (33.23-24)\chapter_text.txt"
        self.chapter_translation_file_path = (
            r"Surahs\Muhammad Al-Luhaidan - Al-Ahzab (33.23-24)\chapter_translation.txt"
        )
        self.verse_counter_file_path = r"Surahs\Muhammad Al-Luhaidan - Al-Ahzab (33.23-24)\verse_counter.txt"

    def muhammad_al_luhaidan_al_baqarah_214(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 214 of Surah Al-Baqarah by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - Al-Baqarah (2.214)"
        self.output_file_name = f"{(self.account.name).lower()} Al-Baqarah (2.214) {str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - Al-Baqarah (2.214)\chapter_text.txt"
        self.chapter_translation_file_path = (
            r"Surahs\Muhammad Al-Luhaidan - Al-Baqarah (2.214)\chapter_translation.txt"
        )
        self.verse_counter_file_path = r"Surahs\Muhammad Al-Luhaidan - Al-Baqarah (2.214)\verse_counter.txt"
        self.time_modifier = -0.2

    def muhammad_al_luhaidan_ali_imran_16_17(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 16-17 of Surah Ali 'Imran by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.16-17)"
        self.output_file_name = (
            f"{(self.account.name).lower()} Ali 'Imran (3.16-17) {str(uuid.uuid4()).split('-')[-1]}"
        )
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.16-17)\chapter_text.txt"
        self.chapter_translation_file_path = (
            r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.16-17)\chapter_translation.txt"
        )

    def muhammad_al_luhaidan_ali_imran_104_106(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 104-106 of Surah Ali 'Imran by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.104-106)"
        self.output_file_name = (
            f"{(self.account.name).lower()} Ali 'Imran (3.104-106) {str(uuid.uuid4()).split('-')[-1]}"
        )
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.104-106)\chapter_text.txt"
        self.chapter_translation_file_path = (
            r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.104-106)\chapter_translation.txt"
        )
        self.verse_counter_file_path = r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.104-106)\verse_counter.txt"

    def muhammad_al_luhaidan_an_naziat_34_41(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 34-41 of Surah An-Nazi'at by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - An-Nazi'at (79.1-46)"
        self.output_file_name = (
            f"{(self.account.name).lower()} An-Nazi'at (79.34-41) {str(uuid.uuid4()).split('-')[-1]}"
        )
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - An-Nazi'at (79.1-46)\chapter_text.txt"
        self.chapter_translation_file_path = (
            r"Surahs\Muhammad Al-Luhaidan - An-Nazi'at (79.1-46)\chapter_translation.txt"
        )
        self.verse_counter_file_path = r"Surahs\Muhammad Al-Luhaidan - An-Nazi'at (79.1-46)\verse_counter.txt"
        self.time_modifier = -0.2

    def muhammad_al_luhaidan_an_nisa_27_29(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 27-29 of Surah An-Nisa by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - An-Nisa (4.27-29)"
        self.output_file_name = "An-Nisa (4.27-29)"
        self.time_modifier = -0.2

    def muhammadloiq_qori_al_ahzab_35(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 35 of Surah Al-Ahzab by Muhammadloiq Qori
        """

        self.directory_path = r"Surahs\Muhammadloiq Qori - 33 - Al-Ahzab"
        self.output_file_name = f"{(self.account.name).lower()}_353_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammadloiq Qori - 33 - Al-Ahzab\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammadloiq Qori - 33 - Al-Ahzab\chapter_translation.txt"

    def salim_bahanan_al_fatihah_2_7(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 2-7 of Surah Al-Fatihah by Salim Bahanan
        """

        self.directory_path = r"Surahs\Salim Bahanan - 1 - Al-Fatihah"
        self.output_file_name = f"{(self.account.name).lower()}_2-7_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_translation.txt"

    def salim_bahanan_ad_duhaa_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Ad-Duhaa by Salim Bahanan
        """

        self.directory_path = r"Surahs\Salim Bahanan - 93 - Ad-Duhaa"
        self.output_file_name = f"{(self.account.name).lower()}_1-11_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\chapter_translation.txt"

    def salim_bahanan_al_qariah_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Al-Qari'ah by Salim Bahanan
        """

        self.directory_path = r"Surahs\Salim Bahanan - 101 - Al-Qari'ah"
        self.output_file_name = f"{(self.account.name).lower()}_1-11_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\chapter_translation.txt"

    def salim_bahanan_at_tin_1_8(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-8 of Surah At-Tin by Salim Bahanan
        """

        self.directory_path = r"Surahs\Salim Bahanan - 95 - At-Tin"
        self.output_file_name = f"{(self.account.name).lower()}_1-8_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Salim Bahanan - 95 - At-Tin\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Salim Bahanan - 95 - At-Tin\chapter_translation.txt"

    def unknown_taha_124_126(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 124-126 of Surah Taha by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - Taha (20.124-126)"
        self.output_file_name = f"{(self.account.name).lower()} Taha (20.124-126) {str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - Taha (20.124-126)\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - Taha (20.124-126)\chapter_translation.txt"

    def unknown_al_furqan_72_75(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 72-75 of Surah Al-Furqan by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - 25 - Al-Furqan"
        self.output_file_name = f"{(self.account.name).lower()}_72-75_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - 25 - Al-Furqan\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - 25 - Al-Furqan\chapter_translation.txt"

    def unknown_al_ankabut_56_58(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-58 of Surah Al-'Ankabut by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - 29 - Al-'Ankabut"
        self.output_file_name = f"{(self.account.name).lower()}_56-58_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_translation.txt"

    def unknown_al_ankabut_56_57(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-57 of Surah Al-'Ankabut by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - 29 - Al-'Ankabut"
        self.output_file_name = f"{(self.account.name).lower()}_56-57_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_translation.txt"
        self.start_line = 1
        self.end_line = 4

    def unknown_al_hujurat_12(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 12 of Surah Al-Hujurat by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - Al-Hujurat (49.12)"
        self.output_file_name = f"{(self.account.name).lower()}_12_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - Al-Hujurat (49.12)\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - Al-Hujurat (49.12)\chapter_translation.txt"

    def unknown_az_zumar_71_75(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 71-75 of Surah Az-Zumar by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - Az-Zumar (39.71-75)"
        self.output_file_name = f"{(self.account.name).lower()} Az-Zumar (39.71-75) {str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - Az-Zumar (39.71-75)\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - Az-Zumar (39.71-75)\chapter_translation.txt"
        self.single_background_clip_horizontal_offset = 750

    def yasser_al_dosari_al_muminun_34_39(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 34-39 of Surah Al-Mu'minun by Yasser Al-Dosari
        """

        self.directory_path = r"Surahs\Yasser Al-Dosari - 23 - Al-Mu'minun"
        self.output_file_name = f"{(self.account.name).lower()}_34-39_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Yasser Al-Dosari - 23 - Al-Mu'minun\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Yasser Al-Dosari - 23 - Al-Mu'minun\chapter_translation.txt"

    def yasser_al_dosari_al_fath_29(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 29 of Surah Al-Fath by Yasser Al-Dosari
        """

        self.directory_path = r"Surahs\Yasser Al-Dosari - 48 - Al-Fath"
        self.output_file_name = f"{(self.account.name).lower()}_29_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Yasser Al-Dosari - 48 - Al-Fath\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Yasser Al-Dosari - 48 - Al-Fath\chapter_translation.txt"

    def yasser_al_dosari_ar_rahman_26_34(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 26-34 of Surah Ar-Rahman by Yasser Al-Dosari
        """

        self.directory_path = r"Surahs\Yasser Al-Dosari - Ar-Rahman (55.1-78)"
        self.output_file_name = (
            f"{(self.account.name).lower()} Ar-Rahman (55.26-34) {str(uuid.uuid4()).split('-')[-1]}"
        )
        self.chapter_text_file_path = r"Surahs\Yasser Al-Dosari - Ar-Rahman (55.1-78)\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Yasser Al-Dosari - Ar-Rahman (55.1-78)\chapter_translation.txt"
        self.verse_counter_file_path = r"Surahs\Yasser Al-Dosari - Ar-Rahman (55.1-78)\verse_counter.txt"
        self.end_time_modifier = -0.3

    def yasser_al_dosari_az_zukhruf_68_73(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 68-73 of Surah Az-Zukhruf by Yasser Al-Dosari
        """

        self.directory_path = r"Surahs\Yasser Al-Dosari - Az-Zukhruf (43.1-89)"
        self.output_file_name = (
            f"{(self.account.name).lower()} Az-Zukhruf (43.68-73) {str(uuid.uuid4()).split('-')[-1]}"
        )
        self.chapter_text_file_path = r"Surahs\Yasser Al-Dosari - Az-Zukhruf (43.1-89)\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Yasser Al-Dosari - Az-Zukhruf (43.1-89)\chapter_translation.txt"
        self.verse_counter_file_path = r"Surahs\Yasser Al-Dosari - Az-Zukhruf (43.1-89)\verse_counter.txt"


def create_tiktok(
    directory_path: str,
    output_file_name: str,
    output_file_path: str = None,
    audio_file_path: str = None,
    chapter_csv_file_path: str = None,
    start_line: int = 1,
    end_line: int = None,
    time_modifier: float = 0.0,
    start_time_modifier: float = 0.0,
    end_time_modifier: float = 0.0,
    chapter: int = None,
    start_verse: int = None,
    end_verse: int = None,
    language: LANGUAGES = LANGUAGES.ENGLISH,
    background_clips_directory_paths: list[str] = ["Anime_Clips"],
    background_video: str = None,
    background_video_horizontal_offset: int = None,
    background_video_vertical_offset: int = None,
    video_map: dict = None,
    pictures_mode: bool = False,
    allow_duplicate_background_clips: bool = False,
    allow_mirrored_background_clips: bool = False,
    video_dimensions: tuple[int, int] = (576, 1024),
    background_clips_speed: float = 1.0,
    shadow_opacity: float = 0.7,
    account: ACCOUNTS = ACCOUNTS.QURAN_2_LISTEN,
    mode: MODES = MODES.DARK,
    new_clip_on_text_change: bool = False,
) -> None:
    """
    Creates a TikTok video
    """

    # Create output file path if it doesn't exist
    if output_file_path is None:
        # Get the directory path
        output_file_directory_path = os.path.join(directory_path, "Videos")

        # Create output file path
        output_file_path = os.path.join(output_file_directory_path, f"{output_file_name}.mp4")
    else:
        # Normalize output file path by replacing forward slashes with backslashes
        output_file_path = output_file_path.replace("/", "\\")

        # Get the directory path
        output_file_directory_path = os.path.dirname(output_file_path)

    # Create output file directory if it doesn't exist
    os.makedirs(output_file_directory_path, exist_ok=True)

    # Create audio file path if it doesn't exist
    if audio_file_path is None:
        try:
            # Get the audio file path
            audio_file = [file for file in os.listdir(directory_path) if file.endswith(".mp3")][0]

            # Create audio file path
            audio_file_path = os.path.join(directory_path, audio_file)
        except IndexError:
            colored_print(Fore.RED, "Audio file not found")
            return

    # Set the english font
    english_font = account.value["english_font"]

    # Set the colors
    shadow_color = mode.value["shadow_color"]
    verse_text_color = mode.value["verse_text_color"]
    verse_translation_color = mode.value["verse_translation_color"]

    if chapter_csv_file_path is None:
        chapter_csv_file_path = os.path.join(directory_path, "chapter.csv")

    if not os.path.isfile(chapter_csv_file_path):
        create_csv_file(chapter_csv_file_path, language.value, chapter, start_verse, end_verse)

        colored_print(Fore.GREEN, "Chapter csv file created successfully")
        return
    else:
        if add_translation_to_existing_csv_file(
            chapter_csv_file_path, language.value, chapter, start_verse, end_verse
        ):
            colored_print(Fore.GREEN, "Chapter csv file updated successfully")
            return

    # Create timestamps text file if it doesn't exist and populate it with the timestamps or update it if it already exists
    if os.path.isdir(directory_path):
        # Get the timestamps csv file path
        timestamps_csv_file_path = os.path.join(directory_path, "Markers.csv")

        # Populate the timestamps text file with the timestamps if it doesn't exist or update it if it already exists
        if os.path.isfile(timestamps_csv_file_path):
            create_timestamps_txt_file(timestamps_csv_file_path)

            timestamps_txt_file_path = timestamps_csv_file_path.replace("Markers.csv", "timestamps.txt")

            sort_timestamps_txt_file(timestamps_txt_file_path)
        else:
            colored_print(Fore.RED, "Markers.csv file not found")
            return
    else:
        colored_print(Fore.RED, "Directory not found")
        return

    # Read files
    chapter_csv_lines = select_columns(chapter_csv_file_path, ["verse", "ar", language.value])

    with open(timestamps_txt_file_path, "r", encoding="utf-8") as timestamps_file:
        timestamps_lines = timestamps_file.readlines()

        # Create the range of lines to loop through
        if end_line is None:
            end_line = len(chapter_csv_lines)

        loop_range = range(start_line, end_line)

        # Get data for final video
        video_width, video_height = video_dimensions
        if start_time_modifier != 0.0:
            video_start = modify_timestamp(timestamps_lines[start_line - 1].strip().split(",")[0], time_modifier)
        else:
            video_start = modify_timestamp(timestamps_lines[start_line - 1].strip().split(",")[0], start_time_modifier)

        if end_time_modifier != 0.0:
            video_end = modify_timestamp(timestamps_lines[end_line - 1].strip().split(",")[0], time_modifier)
        else:
            video_end = modify_timestamp(timestamps_lines[end_line - 1].strip().split(",")[0], end_time_modifier)

        if background_video is not None:
            background_clip = mpy.VideoFileClip(background_video).subclip(video_start)

            # Specify the target aspect ratio (9:16)
            target_aspect_ratio = 9 / 16

            # Calculate the dimensions to fit the target aspect ratio without resizing
            background_clip_width, background_clip_height = background_clip.size
            current_aspect_ratio = background_clip_width / background_clip_height

            if current_aspect_ratio > target_aspect_ratio:
                # Video is wider than 9:16, so we need to crop the sides
                new_width = int(background_clip_height * target_aspect_ratio)

                if background_video_horizontal_offset is None:
                    background_video_horizontal_offset = (background_clip_width - new_width) // 2

                background_clip = background_clip.crop(
                    x1=background_video_horizontal_offset,
                    x2=background_video_horizontal_offset + new_width,
                ).resize(video_dimensions)
            else:
                # Video is taller than 9:16, so we need to crop the top and bottom
                new_height = int(background_clip_width / target_aspect_ratio)

                if background_video_vertical_offset is None:
                    background_video_vertical_offset = (background_clip_height - new_height) // 2

                background_clip = background_clip.crop(
                    y1=background_video_vertical_offset, y2=background_video_vertical_offset + new_height
                ).resize(video_dimensions)

            # Create shadow clip
            shadow_clip = create_shadow_clip(
                size=video_dimensions,
                color=shadow_color,
                duration=background_clip.duration,
                opacity=shadow_opacity,
            )

            # Overlay shadow clip on video
            video = mpy.CompositeVideoClip([background_clip, shadow_clip])

        # Create variables
        all_background_clips_paths = get_all_background_clips_paths(background_clips_directory_paths)
        used_background_clips_paths = []
        video_clips = []
        text_clips_array = []
        video_map = {int(key): value for key, value in video_map.items()} if video_map is not None else None
        video_map_output = {}

        # Create video clips
        for i in loop_range:
            # Get data for video clip
            line = chapter_csv_lines[i - 1]
            verse_counter, verse_text, verse_translation = line

            if i == start_line:
                audio_start = video_start
            else:
                audio_start = modify_timestamp(timestamps_lines[i - 1].strip().split(",")[0], time_modifier)

            if i == end_line - 1:
                audio_end = video_end
            else:
                audio_end = modify_timestamp(timestamps_lines[i].strip().split(",")[0], time_modifier)

            video_clip_duration = get_time_difference_seconds(audio_start, audio_end)

            # Get text duration
            try:
                text_end = modify_timestamp(timestamps_lines[i].strip().split(",")[1], time_modifier)
                text_duration = get_time_difference_seconds(audio_start, text_end)
            except IndexError:
                text_duration = video_clip_duration

            if background_video is None:
                # Create variables for background clips
                video_clip_background_clip_paths = []

                # Get background clips for video clip if not in pictures mode
                if not pictures_mode:
                    background_clips_duration = 0

                    if video_map is not None and i in video_map.keys():
                        # Get background clips from the video map
                        for j in range(len(video_map[i])):
                            background_clip_info = video_map[i][j]

                            background_clip_path = background_clip_info[0]
                            background_clip = mpy.VideoFileClip(background_clip_path).speedx(background_clips_speed)

                            background_clip_duration = (
                                get_video_duration_seconds(background_clip_path) / background_clips_speed
                            )

                            # Get max time offset
                            max_time_offset = get_max_time_offset(background_clip_duration)

                            # Get time offset
                            if (
                                len(background_clip_info) > 1
                                and isinstance(background_clip_info[1], (int, float))
                                and background_clip_info[1] <= max_time_offset
                            ):
                                # Time offset entry exists, is either an int or a float and is less than or equal to the max time offset
                                background_clip_time_offset = background_clip_info[1]
                            else:
                                new_background_clip_time_offset = get_random_time_offset(max_time_offset)

                                colored_print(
                                    Fore.YELLOW,
                                    f"Verse {i} background clip {j + 1} time offset ({background_clip_time_offset}) is invalid, using ({new_background_clip_time_offset}) instead",
                                )

                                background_clip_time_offset = new_background_clip_time_offset

                            # Get max horizontal offset
                            max_horizontal_offset = get_max_horizontal_offset(background_clip.w, video_width)
                            if max_horizontal_offset < 0:
                                # Background clip width is less than video width
                                raise ValueError(
                                    f"Verse {i} Background clip {j + 1} width ({background_clip.w}) is less than video width ({video_width})"
                                )

                            # Get horizontal offset
                            if (
                                len(background_clip_info) > 2
                                and isinstance(background_clip_info[2], int)
                                and background_clip_info[2] <= max_horizontal_offset
                            ):
                                # Horizontal offset entry exists, is an int and is less than or equal to the max horizontal offset
                                background_clip_horizontal_offset = background_clip_info[2]
                            else:
                                new_background_clip_horizontal_offset = get_random_horizontal_offset(
                                    max_horizontal_offset
                                )

                                colored_print(
                                    Fore.YELLOW,
                                    f"Verse {i} background clip {j + 1} horizontal offset ({background_clip_horizontal_offset}) is invalid, using ({new_background_clip_horizontal_offset}) instead",
                                )

                                background_clip_horizontal_offset = new_background_clip_horizontal_offset

                            # Get background clip mirrored
                            if (
                                len(background_clip_info) > 3
                                and isinstance(background_clip_info[3], (str, bool))
                                and background_clip_info[3] in ["True", "False", True, False]
                            ):
                                # Mirrored entry exists and is a string
                                background_clip_mirrored = str(background_clip_info[3])
                            elif allow_mirrored_background_clips:
                                new_background_clip_mirrored = str(random.choice([True, False]))

                                colored_print(
                                    Fore.YELLOW,
                                    f"Verse {i} background clip {j + 1} mirrored ({background_clip_mirrored}) is invalid, using ({new_background_clip_mirrored}) instead",
                                )

                                background_clip_mirrored = new_background_clip_mirrored
                            else:
                                new_background_clip_mirrored = "False"

                                colored_print(
                                    Fore.YELLOW,
                                    f"Verse {i} background clip {j + 1} mirrored ({background_clip_mirrored}) is invalid, using ({new_background_clip_mirrored}) instead",
                                )

                                background_clip_mirrored = new_background_clip_mirrored

                            # Adjust background clip duration
                            adjusted_background_clip_duration = background_clip_duration - background_clip_time_offset

                            video_clip_leftover_duration = video_clip_duration - background_clips_duration
                            if check_background_clip_duration(
                                video_clip_leftover_duration, adjusted_background_clip_duration
                            ):
                                # Background clip duration is appropriate
                                video_clip_background_clip_paths.append(
                                    [
                                        background_clip_path,
                                        background_clip_time_offset,
                                        background_clip_horizontal_offset,
                                        background_clip_mirrored,
                                    ]
                                )
                                used_background_clips_paths.append(background_clip_path)

                                background_clips_duration += adjusted_background_clip_duration

                                if background_clips_duration >= video_clip_duration:
                                    break
                            else:
                                colored_print(
                                    Fore.RED,
                                    f"Verse {i} background clip {j + 1} duration ({background_clip_duration}) is invalid, skipping...",
                                )

                        video_clip_leftover_duration = video_clip_duration - background_clips_duration
                        if video_clip_leftover_duration > 0:
                            (
                                used_background_clips_paths,
                                i,
                                video_clip_background_clip_paths,
                                j,
                            ) = get_valid_background_clips(
                                all_background_clips_paths,
                                allow_duplicate_background_clips,
                                allow_mirrored_background_clips,
                                used_background_clips_paths,
                                video_map,
                                background_clips_speed,
                                video_clip_duration,
                                background_clips_duration,
                                i,
                                video_width,
                                video_clip_background_clip_paths,
                                j,
                            )
                    else:
                        (
                            used_background_clips_paths,
                            i,
                            video_clip_background_clip_paths,
                        ) = get_valid_background_clips(
                            all_background_clips_paths,
                            allow_duplicate_background_clips,
                            allow_mirrored_background_clips,
                            used_background_clips_paths,
                            video_map,
                            background_clips_speed,
                            video_clip_duration,
                            background_clips_duration,
                            i,
                            video_width,
                            video_clip_background_clip_paths,
                        )[
                            :3
                        ]

                    # Add background clips to video map output
                    video_map_output[i] = video_clip_background_clip_paths
                else:
                    background_clip_path = get_random_background_clip_path(all_background_clips_paths)

                    background_clip = mpy.VideoFileClip(background_clip_path)

                    # Get time offset
                    background_clip_time_offset = random.uniform(
                        0, max(0, background_clip_duration - video_clip_duration)
                    )

                    # Get x offset
                    width_difference = background_clip.w - video_dimensions[0]
                    background_clip_horizontal_offset = (
                        random.randint(0, width_difference) if width_difference > 0 else 0
                    )

                    # Get background clip mirrored
                    if allow_mirrored_background_clips:
                        background_clip_mirrored = str(random.choice([True, False]))
                    else:
                        background_clip_mirrored = "False"

                    video_clip_background_clip_paths.append(
                        [
                            background_clip_path,
                            background_clip_time_offset,
                            background_clip_horizontal_offset,
                            background_clip_mirrored,
                        ]
                    )

            # Start creating video clip
            colored_print(Fore.MAGENTA, f"Creating clip {i - start_line + 1}...")

            # Create text clips
            text_clips = [
                create_text_clip(
                    text=verse_text,
                    size=(video_dimensions[0] * 0.9, None),
                    color=verse_text_color,
                    fontsize=44,
                    font=ARABIC_FONT,
                    position=("center", 0.41),
                    method="caption",
                    duration=text_duration,
                ),
                create_text_clip(
                    text=verse_translation,
                    size=(video_dimensions[0] * 0.6, None),
                    color=verse_translation_color,
                    fontsize=20,
                    font=english_font,
                    position=("center", 0.49),
                    method="caption",
                    duration=text_duration,
                ),
            ]

            if verse_counter != "":
                text_clips.append(
                    create_text_clip(
                        text=verse_counter,
                        size=(video_dimensions[0] * 0.6, None),
                        color=verse_translation_color,
                        fontsize=20,
                        font=english_font,
                        position=("center", 0.75),
                        method="caption",
                        duration=text_duration,
                    )
                )

            if background_video:
                # Get start time of text clips
                text_start_time = get_time_difference_seconds(audio_start, video_start)

                text_clips[0] = text_clips[0].set_start(text_start_time)
                text_clips[1] = text_clips[1].set_start(text_start_time)

                if verse_counter != "":
                    text_clips[2] = text_clips[2].set_start(text_start_time)

                text_clips_array.extend(text_clips)
            else:
                # Create shadow clip
                shadow_clip = create_shadow_clip(
                    size=video_dimensions,
                    color=shadow_color,
                    duration=video_clip_duration,
                    opacity=shadow_opacity,
                )

                # Create video clip
                video_clip = create_video_clip(
                    background_clip_paths=video_clip_background_clip_paths,
                    final_clip_duration=video_clip_duration,
                    video_dimensions=video_dimensions,
                    text_clips=text_clips,
                    still_frame=pictures_mode,
                    background_clip_speed=background_clips_speed,
                    text_duration=text_duration,
                    shadow_clip=shadow_clip,
                )

                colored_print(Fore.CYAN, f"Using background clip(s):")
                for background_clip_path in video_clip_background_clip_paths:
                    colored_print(Fore.CYAN, f"- {background_clip_path[0]}")

                video_clips.append(video_clip)

                colored_print(Fore.GREEN, f"Successfully created clip {i - start_line + 1}")

        audio = mpy.AudioFileClip(audio_file_path).set_start(video_start).subclip(video_start, video_end)

        if background_video is not None:
            final_video = mpy.CompositeVideoClip([video, *text_clips_array], use_bgclip=True).set_audio(audio)

            video_map_output = background_video
        else:
            # Concatenate video clips, add audio, and set duration for final video
            final_video = mpy.concatenate_videoclips(clips=video_clips, method="chain").set_audio(audio)

        # Start creating final video
        colored_print(Fore.GREEN, "Creating final video...")

        # Create json file and write video map output to it
        json_output_file_path = output_file_path.replace(".mp4", ".json")

        formatter = Formatter()
        formatter.use_tab_to_indent = True
        formatter.nested_bracket_padding = False
        formatter.max_inline_complexity = 10
        formatter.json_eol_style = EolStyle.LF
        formatter.dont_justify_numbers = True

        formatter.dump(
            video_map_output,
            output_file=json_output_file_path,
            newline_at_eof=True,
        )

        try:
            if background_video:
                final_video.write_videofile(
                    output_file_path,
                    fps=video.fps,
                )
            elif not pictures_mode:
                final_video.write_videofile(
                    filename=output_file_path,
                    codec="libx264",
                )
            else:
                final_video.write_videofile(
                    filename=output_file_path,
                    codec="libx264",
                    fps=60,
                )

            colored_print(Fore.GREEN, "Successfully created final video")

            # Create notification to indicate that the video has been created
            create_notification(title="TikTok Video Created", message=f"Video created for {directory_path}")
        except Exception as error:
            colored_print(Fore.RED, f"Error: {error}")
            return


def create_video_clip(
    background_clip_paths: list[list[str, float or None, int or None, str or None]],
    final_clip_duration: float,
    video_dimensions: tuple[int, int],
    text_clips: list[mpy.TextClip],
    still_frame: bool = False,
    background_clip_speed: float = 1.0,
    text_duration: float = None,
    shadow_clip: mpy.ColorClip = None,
) -> mpy.CompositeVideoClip:
    """
    Creates a video clip
    """

    video_width, video_height = video_dimensions
    background_clips = []

    if still_frame:
        background_clip = mpy.VideoFileClip(background_clip_paths[0][0])

        # Get the total number of frames
        total_frames = int(background_clip.fps * background_clip.duration)

        # Generate a random frame number
        random_frame_number = random.randint(1, total_frames)

        # Seek to the random frame and capture it as an image
        random_frame = background_clip.get_frame(random_frame_number / background_clip.fps)

        video_clip = mpy.ImageClip(random_frame)
    else:
        for background_clip_info in background_clip_paths:
            background_clip_path = background_clip_info[0]
            background_mirrored = background_clip_info[3]
            background_clip = mpy.VideoFileClip(background_clip_path).speedx(background_clip_speed)
            if background_mirrored == "True":
                background_clip = background_clip.fx(mpy.vfx.mirror_x)

            background_clip_time_offset = background_clip_info[1]
            background_clip_horizontal_offset = background_clip_info[2]

            background_clip_duration = (
                get_video_duration_seconds(background_clip_path) / background_clip_speed - background_clip_time_offset
            )

            # Crop, trim and set duration for background clip
            background_clip = (
                background_clip.crop(
                    x1=background_clip_horizontal_offset,
                    y1=0,
                    x2=background_clip_horizontal_offset + video_width,
                    y2=video_height,
                )
                .subclip(
                    t_start=background_clip_time_offset,
                )
                .set_duration(background_clip_duration)
            )

            # Specify the target aspect ratio (9:16)
            target_aspect_ratio = 9 / 16

            # Calculate the dimensions to fit the target aspect ratio
            current_aspect_ratio = background_clip.w / background_clip.h

            if current_aspect_ratio > target_aspect_ratio:
                # Video is wider than 9:16, so we need to crop the sides
                new_width = int(background_clip.h * target_aspect_ratio)
                horizontal_offset = (background_clip.w - new_width) // 2
                background_clip = background_clip.crop(x1=horizontal_offset, x2=horizontal_offset + new_width).resize(
                    video_dimensions
                )

            background_clips.append(background_clip)

        video_clip = mpy.concatenate_videoclips(clips=background_clips, method="chain")
        # background_clip = background_clip.fx(mpy.vfx.colorx, 1.25) # Saturation

    video_clip = video_clip.set_duration(final_clip_duration)
    text_duration = text_duration if text_duration is not None else final_clip_duration
    clips = [video_clip, shadow_clip, *text_clips] if shadow_clip is not None else [video_clip, *text_clips]
    final_video_clip = mpy.CompositeVideoClip(clips, use_bgclip=True).set_duration(final_clip_duration)

    if still_frame:
        final_video_clip = final_video_clip.fadein(final_video_clip.duration / 8).fadeout(
            final_video_clip.duration / 8
        )

    return final_video_clip


def create_shadow_clip(
    size: tuple[int, int],
    color: tuple[int, int, int],
    duration: float,
    opacity: float = 0.7,
) -> mpy.ColorClip:
    """
    Creates a shadow clip
    """

    return mpy.ColorClip(size=size, color=color, duration=duration).set_opacity(opacity)


def create_text_clip(
    text: str,
    size: tuple,
    color: str,  # "rgb(int, int, int)"
    fontsize: int,
    font: str,
    duration: float,
    position: tuple[str or float, str or float],
    bg_color: str = "transparent",
    method: str = "label",
    fade_duration: float = 0.5,
) -> mpy.TextClip:
    """
    Creates a text clip
    """

    return (
        mpy.TextClip(
            txt=text,
            size=size,
            color=color,
            bg_color=bg_color,
            fontsize=fontsize,
            font=font,
            method=method,
        )
        .set_position(position, relative=True)
        .set_duration(duration)
        .crossfadein(fade_duration)
        .crossfadeout(fade_duration)
    )


def colored_print(color: str, text: str) -> None:
    """
    Prints text in color
    """

    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{current_time}] {text}{Style.RESET_ALL}")


def colored_input(color: str, text: str) -> None:
    """
    Prints text in color and then waits for user input
    """

    current_time = datetime.now().strftime("%H:%M:%S")
    input(f"{color}[{current_time}] {text}{Style.RESET_ALL}")


def get_time_difference_seconds(time1: str, time2: str) -> float:
    """
    Calculate the time difference between two time strings in the format "MM:SS.SSS"
    """

    # Convert the time strings to timedelta objects
    time_format = "%M:%S.%f"

    time1 = datetime.strptime(time1, time_format)
    time2 = datetime.strptime(time2, time_format)

    # Calculate the time difference (subtraction)
    time_difference = abs(time2 - time1)

    return time_difference.total_seconds()


def get_video_duration_seconds(video_path: str) -> float:
    """
    Get the duration of a video in seconds.
    """

    video = mpy.VideoFileClip(video_path)
    video_duration = video.duration
    video.close()

    return video_duration


def create_notification(title: str, message: str) -> None:
    """
    Create a notification with the given parameters.
    """

    notification.notify(title=title, message=message, app_name="Python", timeout=1)


def get_verse_text(chapter, verse):
    """
    Gets the text of a verse from the Quran
    """

    verse_text = quran.get_verse(chapter, verse, with_tashkeel=True)
    if verse_text is None or verse_text == "":
        colored_print(Fore.RED, f"Verse {verse} not found")
        return None
    return verse_text


def get_verse_translation(chapter, verse, language="en"):
    """
    Gets the translation of a verse from the Quran
    """

    if language == "en":
        translation_id = 20
    elif language == "nl":
        translation_id = 144

    try:
        response = requests.get(
            f"https://api.quran.com/api/v4/quran/translations/{translation_id}?verse_key={chapter}:{verse}"
        )
        translation = response.json()["translations"][0]["text"]
        soup = BeautifulSoup(translation, "html.parser")
        return soup.get_text()
    except Exception as error:
        colored_print(Fore.RED, f"Error: {error}")
        return None


def create_timestamps_txt_file(timestamps_csv_file_path: str) -> None:
    """
    Creates a timestamps.txt file from a Markers.csv file
    """

    with open(timestamps_csv_file_path, "r", encoding="utf-8") as csv_file:
        lines = csv_file.readlines()[1:]
        timestamps_txt_file_path = timestamps_csv_file_path.replace("Markers.csv", "timestamps.txt")
        with open(timestamps_txt_file_path, "w", encoding="utf-8") as output_file:
            i = 0
            while i < len(lines):
                marker_time = lines[i].split("\t")[1]
                maker_type = lines[i].split("\t")[4]
                if maker_type == "Subclip":
                    i += 1
                    time2 = lines[i].split("\t")[1]
                    output_file.write(f"{time2},{marker_time}\n")
                else:
                    output_file.write(marker_time)
                    if (i + 1) < len(lines):
                        output_file.write("\n")
                i += 1
    colored_print(Fore.GREEN, f"Successfully created '{timestamps_txt_file_path}'")


def sort_timestamps_txt_file(timestamps_txt_file_path: str) -> None:
    """
    Sorts the timestamps in a timestamps.txt file
    """

    # Read timestamps from the file
    with open(timestamps_txt_file_path, "r") as file:
        timestamps = file.read().splitlines()

    # Convert timestamps to timedelta objects
    timestamps = [
        timedelta(minutes=int((time.split(",")[0]).split(":")[0]), seconds=float((time.split(",")[0]).split(":")[1]))
        for time in timestamps
    ]

    # Sort the timestamps
    timestamps.sort()

    # Convert sorted timestamps back to string format
    sorted_timestamps = [
        f"{ts.seconds // 60}:{ts.seconds % 60:02d}.{ts.microseconds // 1000:03d}" for ts in timestamps
    ]

    # Write the sorted timestamps back to the file
    with open(timestamps_txt_file_path, "w") as file:
        file.write("\n".join(sorted_timestamps))


def get_all_background_clips_paths(
    background_clips_directory_paths: list[str],
) -> list[str]:
    """
    Gets all background clip paths
    """

    return [
        os.path.join(path, clip)
        for path in background_clips_directory_paths
        for clip in os.listdir(path)
        if clip.endswith(".mp4")
    ]


def get_random_background_clip_path(all_background_clips_paths: list[str]) -> str:
    """
    Gets a random background clip path
    """

    return random.choice(all_background_clips_paths)


def get_random_time_offset(max_time_offset: float) -> float:
    """
    Returns a random time offset
    """

    return random.uniform(0, max_time_offset / 2)


def get_random_horizontal_offset(max_horizontal_offset: int) -> int:
    """
    Returns a random horizontal offset
    """

    return random.randint(0, max_horizontal_offset)


def check_dictionary_for_path(clip_path: str, dictionary: dict) -> bool:
    """
    Checks if a clip path is in a dictionary
    """
    all_strings = list(
        filter(
            lambda value: isinstance(value[0], str), [value[0] for values in dictionary.values() for value in values]
        )
    )

    return clip_path in all_strings


def check_background_clip_duration(video_clip_leftover_duration: float, background_clip_duration: float) -> bool:
    return (
        video_clip_leftover_duration - background_clip_duration >= MINIMAL_CLIP_DURATION
        or video_clip_leftover_duration - background_clip_duration <= 0
    )


def get_max_time_offset(background_clip_duration: float) -> float:
    """
    Gets the max time offset for a background clip
    """

    get_max_time_offset = background_clip_duration - MINIMAL_CLIP_DURATION

    return max(get_max_time_offset, 0)


def get_max_horizontal_offset(background_clip_width: int, video_width: int) -> int:
    """
    Gets the max horizontal offset for a background clip
    """

    return background_clip_width - video_width


def get_valid_background_clips(
    all_background_clips_paths,
    allow_duplicate_background_clips,
    allow_mirrored_background_clips,
    used_background_clips_paths,
    video_map,
    background_clips_speed,
    video_clip_duration,
    background_clips_duration,
    i,
    video_width,
    video_clip_background_clip_paths,
    j=0,
):
    while True:
        # Get new background clips until the total duration of the background clips is long enough for the video clip
        background_clip_path = get_random_background_clip_path(all_background_clips_paths)

        if len(used_background_clips_paths) == len(all_background_clips_paths):
            allow_duplicate_background_clips = True

        if allow_duplicate_background_clips or (
            not allow_duplicate_background_clips
            and background_clip_path not in used_background_clips_paths
            and (
                (video_map is not None and not check_dictionary_for_path(background_clip_path, video_map))
                or video_map is None
            )
        ):
            # Background clip is not a duplicate or duplicates are allowed
            background_clip_duration = get_video_duration_seconds(background_clip_path) / background_clips_speed

            # Get max time offset
            max_time_offset = get_max_time_offset(background_clip_duration)

            # Get time offset
            background_clip_time_offset = get_random_time_offset(max_time_offset)

            # Get background clip duration starting from the time offset
            background_clip_leftover_duration = background_clip_duration - background_clip_time_offset

            # TO BE ADDED WHEN DURATION IN VIDEO MAPS IS IMPLEMENTED
            # # Get a random clip duration between the minimal clip duration and the leftover duration
            # adjusted_background_clip_duration = max(
            #     MINIMAL_CLIP_DURATION,
            #     random.uniform(MINIMAL_CLIP_DURATION, min(background_clip_leftover_duration, video_clip_duration)),
            # )
            adjusted_background_clip_duration = min(background_clip_leftover_duration, video_clip_duration)

            video_clip_leftover_duration = video_clip_duration - background_clips_duration
            if check_background_clip_duration(video_clip_leftover_duration, adjusted_background_clip_duration):
                # Background clip duration is appropriate
                background_clip = mpy.VideoFileClip(background_clip_path)

                # Get max horizontal offset
                max_horizontal_offset = get_max_horizontal_offset(background_clip.w, video_width)
                if max_horizontal_offset < 0:
                    # Background clip width is less than video width
                    raise ValueError(
                        f"Verse {i} Background clip {j + 1} width ({background_clip.w}) is less than video width ({video_width})"
                    )

                # Get horizontal offset
                background_clip_horizontal_offset = get_random_horizontal_offset(max_horizontal_offset)

                # Get background clip mirrored
                if allow_mirrored_background_clips:
                    background_clip_mirrored = str(random.choice([True, False]))
                else:
                    background_clip_mirrored = "False"

                video_clip_background_clip_paths.append(
                    [
                        background_clip_path,
                        background_clip_time_offset,
                        background_clip_horizontal_offset,
                        background_clip_mirrored,
                    ]
                )
                used_background_clips_paths.append(background_clip_path)

                background_clips_duration += adjusted_background_clip_duration
                j += 1

                if background_clips_duration >= video_clip_duration:
                    break

    return (used_background_clips_paths, i, video_clip_background_clip_paths, j)


def modify_timestamp(timestamp: str, time_in_seconds: int) -> str:
    # Parse the original time string into a timedelta object
    minutes, seconds = timestamp.split(":")
    seconds, milliseconds = seconds.split(".")
    original_timedelta = timedelta(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

    # Ensure the result remains non-negative
    new_timedelta = max(original_timedelta + timedelta(seconds=time_in_seconds), timedelta(0))

    return "{:02d}:{:02d}.{:03d}".format(
        new_timedelta.seconds // 60,
        new_timedelta.seconds % 60,
        new_timedelta.microseconds // 1000,
    )


def remove_empty_rows_from_csv_file(csv_file_path: str) -> None:
    with open(csv_file_path, mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = [
            row
            for row in reader
            if any(cell.strip() != "" for cell in row) or not all(cell.strip() == "" for cell in row)
        ]

    with open(csv_file_path, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


def select_columns(csv_file_path: str, columns_to_select: list[str]) -> list[list[str]]:
    selected_data = []

    with open(csv_file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            selected_row = [row[column] for column in columns_to_select]
            selected_data.append(selected_row)

    return selected_data


def add_translation_to_existing_csv_file(
    chapter_csv_file_path: str, language: LANGUAGES, chapter: int, start_verse: int, end_verse: int
) -> bool:
    with open(chapter_csv_file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        field_names = reader.fieldnames

        if language not in field_names:
            field_names.append(language)
            data = list(reader)

            # Loop through verses and add translations to the corresponding rows
            for verse in range(start_verse, end_verse + 1):
                row_index = verse - start_verse
                data[row_index][language] = get_verse_translation(chapter, verse, language)

            # Write the updated data back to the same file
            with open(chapter_csv_file_path, "w", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(data)

            remove_empty_rows_from_csv_file(chapter_csv_file_path)

            return True


def create_csv_file(
    chapter_csv_file_path: str, language: LANGUAGES, chapter: int, start_verse: int, end_verse: int
) -> None:
    # Create the chapter csv file path
    with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
        csvwriter = csv.writer(chapter_csv_file)
        csvwriter.writerow(["verse", "ar", language])

        for verse in range(start_verse, end_verse + 1):
            # Get the verse text
            verse_text = get_verse_text(chapter, verse)

            # Get the verse translation
            verse_translation = get_verse_translation(chapter, verse, language)

            # Write the verse text and translation to the chapter csv file
            if verse_text is not None and verse_translation is not None:
                csvwriter.writerow([verse, verse_text, verse_translation])
            else:
                break

    remove_empty_rows_from_csv_file(chapter_csv_file_path)


if __name__ == "__main__":
    main()
