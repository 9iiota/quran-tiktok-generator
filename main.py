import csv
import moviepy.editor as mpy
import os
import random
import re
import requests

from colorama import Fore, Style
from compact_json import EolStyle, Formatter
from datetime import datetime, timedelta
from enum import Enum
from fuzzywuzzy import fuzz
from plyer import notification
from pyquran import quran

ARABIC_FONT = "Fonts/Hafs.ttf"
MINIMAL_CLIP_DURATION = 0.75


# TODO: FIX VERTICAL OFFSET
# TODO: Add support for background clips disjoint from audio timings
# TODO: ADD DURATIONS IN VIDEO MAP AND UNCOMMENT CODE IN GET_VALID_BACKGROUND_CLIPS
# TODO: Add support for clips shorter than final clip with still frames
# TODO: FIX PICTURES MODE


def main() -> None:
    tiktok = TikToks(
        # account=ACCOUNTS.HEARTFELTRECITATIONS,
        # language=LANGUAGES.DUTCH,
    )
    tiktok.change_settings(video_map={})
    tiktok.abdul_rahman_mossad_al_ghashiyah_1_9()
    tiktok.run()


def change_timestamps(input_file, output_file, seconds_to_add):
    try:
        with open(input_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            fieldnames = reader.fieldnames

            data = list(reader)
            for line in range(len(data)):
                data[line]["Start"] = offset_timestamp(data[line]["Start"], seconds_to_add)

            with open(output_file, "w", encoding="utf-8") as output_csvfile:
                writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames, delimiter="\t")
                writer.writeheader()
                writer.writerows(data)

        remove_empty_rows_from_csv_file(output_file)

        print(f"Timestamps modified and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def test():
    # # Get only the user-defined methods
    # user_defined_methods = [
    #     func
    #     for func in dir(TikToks)
    #     if callable(getattr(TikToks, func))
    #     and not func.startswith("__")
    #     and not func.startswith("_")
    #     and not "run" in func
    #     and not "test" in func
    #     and not "change_settings" in func
    # ]

    # return user_defined_methods
    pass


class ACCOUNTS(Enum):
    QURAN_2_LISTEN = {
        "english_font": "Fonts/Butler_Regular.otf",
        "background_clips_directory_paths": ["Anime_Clips"],
    }  # crazyshocklight@hotmail.com
    REFLECT2RECITE = {
        "english_font": "Fonts/Butler_Regular.otf",
        "background_clips_directory_paths": ["Real_Clips"],
    }  # crazyshocklight2@gmail.com
    HEARTFELTRECITATIONS = {
        "english_font": "Fonts/Butler_Regular.otf",
        "background_clips_directory_paths": ["Anime_Clips", "Real_Clips"],
    }
    # LOVE_QURAN77 = {"english_font": "Fonts/Sk-Modernist-Regular.otf"}
    QURANIC_TIKTOKS = {
        "english_font": "Fonts/FreshStart.otf",
        "background_clips_directory_paths": ["Real_Clips"],
    }  # crazyshocky@hotmail.com


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
        language: LANGUAGES = LANGUAGES.ENGLISH,
        account: ACCOUNTS = ACCOUNTS.QURAN_2_LISTEN,
        mode: MODES = MODES.DARK,
        background_clips_directory_paths: list[str] = None,
        video_dimensions: tuple[int, int] = (576, 1024),
        background_clips_speed: float = 1.0,
        shadow_opacity: float = 0.7,
        video_mode: bool = True,
        allow_duplicate_background_clips: bool = True,
        allow_mirrored_background_clips: bool = False,
    ) -> None:
        self.account = account
        self.allow_duplicate_background_clips = allow_duplicate_background_clips
        self.allow_mirrored_background_clips = allow_mirrored_background_clips
        self.background_clips_directory_paths = background_clips_directory_paths
        self.background_clips_speed = background_clips_speed
        self.chapter = None
        self.chapter_csv_file_path = None
        self.directory_path = None
        self.end_line = None
        self.end_time_modifier = 0.0
        self.end_verse = None
        self.language = language
        self.mode = mode
        self.output_file_name = None
        self.video_mode = video_mode
        self.shadow_opacity = shadow_opacity
        self.single_background_clip = None
        self.single_background_clip_horizontal_offset = None
        self.single_background_clip_vertical_offset = None
        self.start_line = None
        self.start_time_modifier = None
        self.start_verse = None
        self.time_modifier = 0.0
        self.video_dimensions = video_dimensions
        self.video_map = None

    def joe(self):
        return (self.directory_path, self.chapter, self.start_verse, self.end_verse)

    def change_settings(
        self,
        single_background_clip: str = None,
        single_background_clip_horizontal_offset: float = None,
        single_background_clip_vertical_offset: float = None,
        video_map: dict[int, tuple[str, float, int]] = None,
    ) -> None:
        self.single_background_clip = single_background_clip
        self.single_background_clip_horizontal_offset = single_background_clip_horizontal_offset
        self.single_background_clip_vertical_offset = single_background_clip_vertical_offset
        self.video_map = video_map

    def run(self) -> None:
        if self.chapter is None:
            self.chapter_csv_file_path = os.path.join(self.directory_path, "chapter.csv")

        self.output_file_name = f"{self.output_file_name} {(self.account.name).lower()} {self.language.value} {datetime.now().strftime('%H.%M.%S %d-%m-%Y')}"

        create_tiktok(
            directory_path=self.directory_path,
            output_file_name=self.output_file_name,
            chapter_csv_file_path=self.chapter_csv_file_path,
            start_line=self.start_line,
            end_line=self.end_line,
            chapter=self.chapter,
            start_verse=self.start_verse,
            end_verse=self.end_verse,
            language=self.language,
            background_clips_directory_paths=self.background_clips_directory_paths,
            background_video=self.single_background_clip,
            background_video_horizontal_offset=self.single_background_clip_horizontal_offset,
            background_video_vertical_offset=self.single_background_clip_vertical_offset,
            video_map=self.video_map,
            video_mode=self.video_mode,
            allow_duplicate_background_clips=self.allow_duplicate_background_clips,
            allow_mirrored_background_clips=self.allow_mirrored_background_clips,
            video_dimensions=self.video_dimensions,
            background_clips_speed=self.background_clips_speed,
            shadow_opacity=self.shadow_opacity,
            account=self.account,
            mode=self.mode,
            time_modifier=self.time_modifier,
            start_time_modifier=self.start_time_modifier,
            end_time_modifier=self.end_time_modifier,
        )

    def _set_values(
        self,
        directory_path: str,
        output_file_name: str,
        chapter: int,
        start_verse: int,
        end_verse: int,
        time_modifier: float = -0.2,
    ) -> None:
        self.directory_path = directory_path
        self.chapter = chapter
        self.start_verse = start_verse
        self.end_verse = end_verse
        self.time_modifier = time_modifier
        self.output_file_name = (
            f"{((self.directory_path).split(' - ')[1]).split(' (')[0]} ({self.chapter}.{output_file_name})"
        )

    def test(self):
        self._set_values(
            r"Surahs\test - test (1.1)",
            "1",
            100,
            1,
            11,
        )

    def abdul_rahman_mossad_al_adiyat_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Al-'Adiyat by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-'Adiyat (100.1-11)",
            "1-11",
            100,
            1,
            11,
        )

    def abdul_rahman_mossad_al_ankabut_54_60(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 54-60 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-'Ankabut (29.53-64)",
            "54-60",
            29,
            53,
            64,
        )
        self.end_time_modifier = -0.4

    def abdul_rahman_mossad_al_ankabut_54_57(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 54-57 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-'Ankabut (29.53-64)",
            "54-57",
            29,
            53,
            64,
        )
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_al_ankabut_56_57(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-57 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-'Ankabut (29.53-64)",
            "56-57",
            29,
            53,
            64,
        )
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_al_ghashiyah_1_9(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-9 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-Ghashiyah (88.1-26)",
            "1-9",
            88,
            1,
            26,
        )
        self.end_time_modifier = -0.4

    def abdul_rahman_mossad_al_ghashiyah_10_26(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 10-26 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-Ghashiyah (88.1-26)",
            "10-26",
            88,
            1,
            26,
        )

    def abdul_rahman_mossad_al_ghashiyah_10_16(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 10-16 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-Ghashiyah (88.1-26)",
            "10-16",
            88,
            1,
            26,
        )
        self.end_time_modifier = -0.6

    def abdul_rahman_mossad_al_ghashiyah_10_12(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 10-12 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-Ghashiyah (88.1-26)",
            "10-12",
            88,
            1,
            26,
        )
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_al_muzzammil_6_13(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 6-13 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-Muzzammil (73.1-20)",
            "6-13",
            73,
            1,
            20,
        )
        self.end_time_modifier = -0.3

    def abdul_rahman_mossad_al_muzzammil_14_18(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-18 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-Muzzammil (73.1-20)",
            "14-18",
            73,
            1,
            20,
        )
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_al_muzzammil_14_15(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-15 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Al-Muzzammil (73.1-20)",
            "14-15",
            73,
            1,
            20,
        )
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_maryam_93_98(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 93-98 of Surah Maryam by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Maryam (19.65-98)",
            "93-98",
            19,
            65,
            98,
        )

    def abdul_rahman_mossad_maryam_93_94(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 93-94 of Surah Maryam by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Maryam (19.65-98)",
            "93-94",
            19,
            65,
            98,
        )
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_yunus_7_10(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 7-10 of Surah Yunus by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Yunus (10.3-25)",
            "7-10",
            10,
            3,
            25,
        )
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_yunus_17_20(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 17-20 of Surah Yunus by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Yunus (10.3-25)",
            "17-20",
            10,
            3,
            25,
        )
        self.end_time_modifier = -0.2

    def abdul_rahman_mossad_yunus_17(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 17 of Surah Yunus by Abdul Rahman Mossad
        """

        self._set_values(
            r"Surahs\Abdul Rahman Mossad - Yunus (10.3-25)",
            "17",
            10,
            3,
            25,
        )
        self.end_time_modifier = -0.5

    def ahmed_khedr_taha_14_16(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-16 of Surah Taha by Ahmed Khedr
        """

        self._set_values(
            r"Surahs\Ahmed Khedr - Taha (20.1-135)",
            "14-16",
            20,
            1,
            135,
        )

    def fatih_seferagic_al_hujurat_10(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 10 of Surah Al-Hujurat by Fatih Seferagic
        """

        self._set_values(
            r"Surahs\Fatih Seferagic - Al-Hujurat (49.10)",
            "10",
            49,
            10,
            10,
        )

    def fatih_seferagic_al_baqarah_255(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 255 of Surah Al-Baqarah by Fatih Seferagic
        """

        self._set_values(
            r"Surahs\Fatih Seferagic - Al-Baqarah (2.255)",
            "255",
            2,
            255,
            255,
        )

    def fatih_seferagic_al_hashr_21_24(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 21-24 of Surah Al-Hashr by Fatih Seferagic
        """

        self._set_values(
            r"Surahs\Fatih Seferagic - Al-Hashr (59.21-24)",
            "21-24",
            59,
            21,
            24,
        )

    def fatih_seferagic_al_qiyamah_1_12(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-12 of Surah Al-Qiyamah by Fatih Seferagic
        """

        self._set_values(
            r"Surahs\Fatih Seferagic - Al-Qiyamah (75.1-40)",
            "1-12",
            75,
            1,
            40,
        )
        self.end_time_modifier = -0.4

    def fatih_seferagic_al_qiyamah_13_19(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 13-19 of Surah Al-Qiyamah by Fatih Seferagic
        """

        self._set_values(
            r"Surahs\Fatih Seferagic - Al-Qiyamah (75.1-40)",
            "13-19",
            75,
            1,
            40,
        )
        self.end_time_modifier = -0.4

    def muhammad_al_luhaidan_ali_imran_15(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 15 of Surah Ali 'Imran by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.15)",
            "15",
            3,
            15,
            15,
        )

    def muhammad_al_luhaidan_an_nisa_75_76(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 75-76 of Surah An-Nisa by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - An-Nisa (4.75-76)",
            "75-76",
            4,
            75,
            76,
        )

    def salim_bahanan_ad_duhaa_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Ad-Duhaa by Salim Bahanan
        """

        self._set_values(
            r"Surahs\Salim Bahanan - Ad-Duhaa (93.1-11)",
            "1-11",
            93,
            1,
            11,
        )

    def salim_bahanan_al_qariah_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Al-Qari'ah by Salim Bahanan
        """

        self._set_values(
            r"Surahs\Salim Bahanan - Al-Qari'ah (101.1-11)",
            "1-11",
            101,
            1,
            11,
        )
        self.start_time_modifier = -0.2

    def unknown_al_furqan_63_70(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 63-70 of Surah Al-Furqan by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - Al-Furqan (25.63-70)",
            "63-70",
            25,
            63,
            70,
        )

    def unknown_as_saffat_123_132(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 123-132 of Surah As-Saffat by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - As-Saffat (37.123-132)",
            "123-132",
            37,
            123,
            132,
        )

    def yousef_al_soqier_ya_sin_63_65(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 63-65 of Surah Ya Sin by Yousef Al-Soqier
        """

        self._set_values(
            r"Surahs\Yousef Al-Soqier - Ya-Sin (36.55-67)",
            "63-65",
            36,
            55,
            67,
        )
        self.end_time_modifier = -0.2

    ######################################################################################################################################################
    ######################################################################################################################################################
    ######################################################################################################################################################
    ######################################################################################################################################################
    ######################################################################################################################################################
    ######################################################################################################################################################

    def fatih_seferagic_an_nisa_155_160(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 155-160 of Surah An-Nisa by Fatih Seferagic
        """

        self._set_values(
            r"Surahs\Fatih Seferagic - An-Nisa (4.155-160)",
            "155-160",
            4,
            155,
            176,
        )

    def fatih_seferagic_an_nur_35(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 35 of Surah An-Nur by Fatih Seferagic
        """

        self._set_values(
            r"Surahs\Fatih Seferagic - An-Nur (24.35)",
            "35",
            24,
            35,
            35,
        )

    def mansour_as_salimi_maryam_27_33(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 27-33 of Surah Maryam by Mansour As Salimi
        """

        self._set_values(
            r"Surahs\Mansour As Salimi - Maryam (19.27-33)",
            "27-33",
            19,
            27,
            33,
        )

    def mansour_as_salimi_yusuf_1_5(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-5 of Surah Yusuf by Mansour As Salimi
        """

        self._set_values(
            r"Surahs\Mansour As Salimi - Yusuf (12.1-5)",
            "1-5",
            12,
            1,
            5,
        )

    def mostafa_shaibani_al_qiyamah_20_27(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 20-27 of Surah Al-Qiyamah by Mostafa Shaibani
        """

        self._set_values(
            r"Surahs\Mostafa Shaibani - Al-Qiyamah (75.20-27)",
            "20-27",
            75,
            20,
            27,
        )

    def muhammad_al_luhaidan_al_baqarah_273_274(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 273-274 of Surah Al-Baqarah by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-Baqarah (2.273-274)",
            "273-274",
            2,
            273,
            274,
        )

    def muhammad_al_luhaidan_al_anam_27_30(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 27-30 of Surah Al-An'am by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-An'am (6.27-30)",
            "27-30",
            6,
            27,
            30,
        )

    def muhammad_al_luhaidan_maryam_85_92(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 85-92 of Surah Maryam by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Maryam (19.85-92)",
            "85-92",
            19,
            85,
            92,
        )

    def muhammad_al_luhaidan_taha_105_108(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 105-108 of Surah Taha by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Taha (20.105-108)",
            "105-108",
            20,
            105,
            108,
        )

    def muhammad_al_luhaidan_al_furqan_26_30(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 26-30 of Surah Al-Furqan by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-Furqan (25.26-30)",
            "26-30",
            25,
            26,
            30,
        )

    def muhammad_al_luhaidan_al_furqan_72_77(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 72-77 of Surah Al-Furqan by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-Furqan (25.72-77)",
            "72-77",
            25,
            72,
            77,
        )

    def muhammad_al_luhaidan_al_furqan_74(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 74 of Surah Al-Furqan by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-Furqan (25.72-77)",
            "74",
            25,
            72,
            77,
        )

    def muhammad_al_luhaidan_al_haqqah_29_33(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 29-33 of Surah Al-Haqqah by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-Haqqah (69.29-33)",
            "29-33",
            69,
            29,
            33,
        )

    def muhammad_al_luhaidan_al_insan_20_22(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 20-22 of Surah Al-Insan by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-Insan (76.20-22)",
            "20-22",
            76,
            20,
            22,
        )

    def muhammad_al_luhaidan_al_ahzab_23_24(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 23-24 of Surah Al-Ahzab by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-Ahzab (33.23-24)",
            "23-24",
            33,
            23,
            24,
        )

    def muhammad_al_luhaidan_al_baqarah_214(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 214 of Surah Al-Baqarah by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Al-Baqarah (2.214)",
            "214",
            2,
            214,
            214,
        )

    def muhammad_al_luhaidan_ali_imran_16_17(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 16-17 of Surah Ali 'Imran by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.16-17)",
            "16-17",
            3,
            16,
            17,
        )

    def muhammad_al_luhaidan_ali_imran_104_106(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 104-106 of Surah Ali 'Imran by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - Ali 'Imran (3.104-106)",
            "104-106",
            3,
            104,
            106,
        )

    def muhammad_al_luhaidan_an_naziat_34_41(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 34-41 of Surah An-Nazi'at by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - An-Nazi'at (79.1-46)",
            "34-41",
            79,
            1,
            46,
        )

    def muhammad_al_luhaidan_an_nisa_27_29(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 27-29 of Surah An-Nisa by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - An-Nisa (4.27-29)",
            "27-29",
            4,
            27,
            29,
        )

    def muhammad_al_luhaidan_an_nisa_27(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 27 of Surah An-Nisa by Muhammad Al-Luhaidan
        """

        self._set_values(
            r"Surahs\Muhammad Al-Luhaidan - An-Nisa (4.27-29)",
            "27",
            4,
            27,
            29,
        )
        self.end_time_modifier = -0.4

    def muhammadloiq_qori_al_ahzab_35(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 35 of Surah Al-Ahzab by Muhammadloiq Qori
        """

        self._set_values(
            r"Surahs\Muhammadloiq Qori - Al-Ahzab (33.35)",
            "35",
            33,
            35,
            35,
        )

    def salim_bahanan_al_fatihah_2_7(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 2-7 of Surah Al-Fatihah by Salim Bahanan
        """

        self._set_values(
            r"Surahs\Salim Bahanan - Al-Fatihah (1.1-7)",
            "2-7",
            1,
            1,
            7,
        )

    def salim_bahanan_at_tin_1_8(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-8 of Surah At-Tin by Salim Bahanan
        """

        self._set_values(
            r"Surahs\Salim Bahanan - At-Tin (95.1-8)",
            "1-8",
            95,
            1,
            8,
        )

    def unknown_taha_124_126(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 124-126 of Surah Taha by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - Taha (20.124-126)",
            "124-126",
            20,
            124,
            126,
        )

    def unknown_al_furqan_72_75(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 72-75 of Surah Al-Furqan by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - Al-Furqan (25.72-77)",
            "72-75",
            25,
            72,
            77,
        )

    def unknown_al_ankabut_56_58(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-58 of Surah Al-'Ankabut by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - Al-'Ankabut (29.56-58)",
            "56-58",
            29,
            56,
            58,
        )

    def unknown_al_ankabut_56_57(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-57 of Surah Al-'Ankabut by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - Al-'Ankabut (29.56-58)",
            "56-57",
            29,
            56,
            58,
        )

    def unknown_al_hujurat_12(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 12 of Surah Al-Hujurat by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - Al-Hujurat (49.12)",
            "12",
            49,
            12,
            12,
        )

    def unknown_az_zumar_71_75(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 71-75 of Surah Az-Zumar by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - Az-Zumar (39.71-75)",
            "71-75",
            39,
            71,
            75,
        )
        self.single_background_clip = os.path.join(self.directory_path, "video.mp4")
        self.single_background_clip_horizontal_offset = 750

    def unknown_az_zumar_73_75(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 73-75 of Surah Az-Zumar by an unknown reciter
        """

        self._set_values(
            r"Surahs\Unknown - Az-Zumar (39.71-75)",
            "73-75",
            39,
            71,
            75,
        )
        self.single_background_clip = os.path.join(self.directory_path, "video.mp4")
        self.single_background_clip_horizontal_offset = 750

    def yasser_al_dosari_al_muminun_34_39(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 34-39 of Surah Al-Mu'minun by Yasser Al-Dosari
        """

        self._set_values(
            r"Surahs\Yasser Al-Dosari - Al-Mu'minun (23.34-39)",
            "34-39",
            23,
            34,
            39,
        )

    def yasser_al_dosari_al_fath_29(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 29 of Surah Al-Fath by Yasser Al-Dosari
        """

        self._set_values(
            r"Surahs\Yasser Al-Dosari - Al-Fath (48.29)",
            "29",
            48,
            29,
            29,
        )

    def yasser_al_dosari_ar_rahman_26_34(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 26-34 of Surah Ar-Rahman by Yasser Al-Dosari
        """

        self._set_values(
            r"Surahs\Yasser Al-Dosari - Ar-Rahman (55.1-78)",
            "26-34",
            55,
            1,
            78,
        )
        self.end_time_modifier = -0.3

    def yasser_al_dosari_az_zukhruf_68_73(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 68-73 of Surah Az-Zukhruf by Yasser Al-Dosari
        """

        self._set_values(
            r"Surahs\Yasser Al-Dosari - Az-Zukhruf (43.1-89)",
            "68-73",
            43,
            1,
            89,
        )


def add_translation_to_existing_csv_file(
    chapter_csv_file_path: str, language: LANGUAGES, chapter: int, start_verse: int, end_verse: int
) -> bool:
    with open(chapter_csv_file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        field_names = reader.fieldnames

        if language not in field_names:
            data = list(reader)

            # If "timestamps" column exists, we insert the new column before it
            if "timestamps" in field_names:
                timestamps_index = field_names.index("timestamps")
                field_names.insert(timestamps_index, language)

            # If "timestamps" column doesn't exist, we append the new column
            else:
                field_names.append(language)

            translations = get_chapter_translation(chapter)[start_verse - 1 : end_verse]

            # Add the translations to the data
            for row_index, row in enumerate(data):
                row[language] = translations[row_index]

            # Write the updated data back to the same file
            with open(chapter_csv_file_path, "w", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(data)

            remove_empty_rows_from_csv_file(chapter_csv_file_path)

            return True


def add_or_update_csv_timestamps(chapter_csv_file_path: str, timestamps_csv_file_path: str) -> None:
    with open(timestamps_csv_file_path, "r", encoding="utf-8") as timestamps_csv_file:
        lines = timestamps_csv_file.readlines()[1:]
        timestamps = []
        i = 0
        while i < len(lines):
            marker_time = lines[i].split("\t")[1]
            marker_type = lines[i].split("\t")[4]
            if marker_type == "Subclip":
                i += 1
                time2 = lines[i].split("\t")[1]
                timestamps.append([time2, marker_time])
            else:
                timestamps.append(marker_time)
            i += 1

        sorted_nested_timestamps = sort_nested_timestamps(timestamps)
        sorted_timestamps = sorted(sorted_nested_timestamps, key=get_seconds_from_timestamp)

        with open(chapter_csv_file_path, "r", encoding="utf-8") as chapter_csv_file:
            reader = csv.DictReader(chapter_csv_file)
            field_names = reader.fieldnames

            if "timestamps" not in field_names:
                field_names.append("timestamps")

            data = list(reader)

            while len(data) < len(sorted_timestamps):
                data.append({"timestamps": sorted_timestamps[len(data)].strip()})

            for line in range(len(sorted_timestamps)):
                if isinstance(sorted_timestamps[line], list):
                    for i in range(len(sorted_timestamps[line])):
                        sorted_timestamps[line][i] = sorted_timestamps[line][i].strip()
                    data[line]["timestamps"] = ",".join(sorted_timestamps[line])
                else:
                    data[line]["timestamps"] = sorted_timestamps[line].strip()

        with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
            writer = csv.DictWriter(chapter_csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data)

        remove_empty_rows_from_csv_file(chapter_csv_file_path)

    colored_print(Fore.GREEN, f"Successfully updated timestamps of '{chapter_csv_file_path}'")


def add_or_update_csv_verse_numbers(
    chapter_csv_file_path: str, chapter: int, start_verse: int, end_verse: int
) -> None:
    translations = get_chapter_translation(chapter)[start_verse - 1 : end_verse]
    existing_verses = set()

    with open(chapter_csv_file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        field_names = reader.fieldnames

        data = []

        for row in reader:
            if row["en"] == "" and row["timestamps"] != "":
                data.append(row)
            else:
                best_ratio, best_verse_number = (0, None)
                csv_translation = row["en"]
                csv_translation_length = len(csv_translation)

                for j, translation in enumerate(translations, start=start_verse):
                    letter_difference = len(translation) - csv_translation_length

                    if letter_difference >= 0:
                        for k in range(letter_difference + 1):
                            match = translation[k : csv_translation_length + k]
                            ratio = fuzz.ratio(csv_translation, match)

                            if ratio > best_ratio:
                                best_ratio, best_verse_number = (ratio, j)

                            if ratio == 100:
                                break

                verse = f"{chapter}:{best_verse_number}"
                if verse not in existing_verses:
                    row["verse"] = verse
                    existing_verses.add(verse)
                else:
                    row["verse"] = ""

                data.append(row)

    with open(chapter_csv_file_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)

    colored_print(Fore.GREEN, f"Successfully updated verse numbers of '{chapter_csv_file_path}'")


def check_background_clip_duration(video_clip_leftover_duration: float, background_clip_duration: float) -> bool:
    return (
        video_clip_leftover_duration - background_clip_duration >= MINIMAL_CLIP_DURATION
        or video_clip_leftover_duration - background_clip_duration <= 0
    )


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


def colored_input(color: str, text: str) -> None:
    """
    Prints text in color and then waits for user input
    """

    current_time = datetime.now().strftime("%H:%M:%S")
    input(f"{color}[{current_time}] {text}{Style.RESET_ALL}")


def colored_print(color: str, text: str) -> None:
    """
    Prints text in color
    """

    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{current_time}] {text}{Style.RESET_ALL}")


def create_chapter_csv_file(
    chapter_csv_file_path: str, language: LANGUAGES, chapter: int, start_verse: int, end_verse: int
) -> None:
    # Create the chapter csv file path
    with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
        csvwriter = csv.writer(chapter_csv_file)
        csvwriter.writerow(["verse", "ar", language])

        texts = get_chapter_text(chapter)[start_verse - 1 : end_verse]
        translations = get_chapter_translation(chapter)[start_verse - 1 : end_verse]

        for i in range(len(translations)):
            verse = f"{chapter}:{i + start_verse}"
            verse_text = texts[i]
            verse_translation = translations[i]

            # Write the verse text and translation to the chapter csv file
            if verse_text is not None and verse_translation is not None:
                csvwriter.writerow([verse, verse_text, verse_translation])
            else:
                break

    remove_empty_rows_from_csv_file(chapter_csv_file_path)
    modify_unsupported_arabic_letters(chapter_csv_file_path)
    modify_unsupported_english_letters(chapter_csv_file_path)


def create_notification(title: str, message: str) -> None:
    """
    Create a notification with the given parameters.
    """

    notification.notify(title=title, message=message, app_name="Python", timeout=1)


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


def create_tiktok(
    directory_path: str,
    output_file_name: str,
    output_file_path: str = None,
    audio_file_path: str = None,
    chapter_csv_file_path: str = None,
    start_line: int = None,
    end_line: int = None,
    chapter: int = None,
    start_verse: int = None,
    end_verse: int = None,
    language: LANGUAGES = LANGUAGES.ENGLISH,
    background_clips_directory_paths: list[str] = None,
    background_video: str = None,
    background_video_horizontal_offset: int = None,
    background_video_vertical_offset: int = None,
    video_map: dict = None,
    video_mode: bool = True,
    allow_duplicate_background_clips: bool = False,
    allow_mirrored_background_clips: bool = True,
    video_dimensions: tuple[int, int] = (576, 1024),
    background_clips_speed: float = 1.0,
    shadow_opacity: float = 0.7,
    account: ACCOUNTS = ACCOUNTS.QURAN_2_LISTEN,
    mode: MODES = MODES.DARK,
    time_modifier: float = 0.0,
    start_time_modifier: float = None,
    end_time_modifier: float = 0.0,
) -> None:
    """
    Creates a TikTok video
    """

    # Get output file path
    if output_file_path is None:
        output_file_directory_path = os.path.join(directory_path, "Videos")

        output_file_path = os.path.join(output_file_directory_path, f"{output_file_name}.mp4")

        reciter_name = (output_file_path.split("\\")[-3]).split(" - ")[0]
        output_file_name_split = output_file_name.split(") ")
        output_file_name = f"{output_file_name_split[0]}) - {reciter_name} {output_file_name_split[1]}"

        output_file_path = os.path.join(output_file_directory_path, f"{output_file_name}.mp4")

    # Get output file directory path
    else:
        # Normalize output file path by replacing forward slashes with backslashes
        output_file_path = output_file_path.replace("/", "\\")

        output_file_directory_path = os.path.dirname(output_file_path)

    # Create output file directory if it doesn't exist
    os.makedirs(output_file_directory_path, exist_ok=True)

    # Get audio file path
    if audio_file_path is None:
        try:
            audio_file = [file for file in os.listdir(directory_path) if file.endswith(".mp3")][0]

            audio_file_path = os.path.join(directory_path, audio_file)
        except IndexError:
            colored_print(Fore.RED, "Audio file not found")
            return

    # Modify settings
    english_font = account.value["english_font"]
    background_clips_directory_paths = account.value["background_clips_directory_paths"]
    shadow_color = mode.value["shadow_color"]
    verse_text_color = mode.value["verse_text_color"]
    verse_translation_color = mode.value["verse_translation_color"]

    # Get chapter csv file path
    if chapter_csv_file_path is None:
        chapter_csv_file_path = os.path.join(directory_path, "chapter.csv")

    # Create chapter csv file if it doesn't exist and populate it with the chapter text and translation
    if not os.path.isfile(chapter_csv_file_path):
        create_chapter_csv_file(chapter_csv_file_path, language.value, chapter, start_verse, end_verse)

        colored_print(Fore.GREEN, "Chapter csv file created successfully")
        return

    # Add translation to existing chapter csv file if needed
    else:
        if add_translation_to_existing_csv_file(
            chapter_csv_file_path, language.value, chapter, start_verse, end_verse
        ):
            colored_print(Fore.GREEN, "Chapter csv file updated successfully")
            return

    # Check if directory exists
    if os.path.isdir(directory_path):
        timestamps_csv_file_path = os.path.join(directory_path, "Markers.csv")

        # Update timestamps in chapter csv file if timestamps csv file exists
        if os.path.isfile(timestamps_csv_file_path):
            add_or_update_csv_timestamps(chapter_csv_file_path, timestamps_csv_file_path)
            add_or_update_csv_verse_numbers(chapter_csv_file_path, chapter, start_verse, end_verse)
        else:
            colored_print(Fore.RED, "Markers.csv file not found")
            return
    else:
        colored_print(Fore.RED, "Directory not found")
        return

    # Get chapters csv columns
    chapter_csv_lines = select_columns(chapter_csv_file_path, ["verse", "ar", language.value, "timestamps"])

    # Get the range of lines to loop through
    if start_line is None or end_line is None:
        start_line, end_line = get_loop_range(output_file_name, chapter_csv_lines, chapter, start_line, end_line)

    loop_range = range(start_line, end_line)

    # Get variables for TikTok video
    video_width, video_height = video_dimensions

    video_start_timestamp = chapter_csv_lines[start_line - 1][3].strip().split(",")[0]
    if start_time_modifier is None:
        video_start = offset_timestamp(video_start_timestamp, time_modifier)
    else:
        video_start = offset_timestamp(video_start_timestamp, start_time_modifier)

    video_end_timestamp = chapter_csv_lines[end_line - 1][3].strip().split(",")[0]
    video_end = offset_timestamp(video_end_timestamp, end_time_modifier)

    video_duration = get_time_difference_seconds(video_start, video_end)

    audio = mpy.AudioFileClip(audio_file_path).subclip(video_start, video_end)

    # Get variables for final video
    all_background_clip_paths = get_all_background_clip_paths(background_clips_directory_paths)
    text_clips_array = []
    used_background_clip_paths = []
    video_clips = []
    video_map = {int(key): value for key, value in video_map.items()} if video_map is not None else None
    video_map_output = {}

    # Loop through lines
    for line in loop_range:
        # Get variables for video clip
        current_line = chapter_csv_lines[line - 1]
        verse_counter, verse_text, verse_translation, timestamp = current_line

        next_line = chapter_csv_lines[line]
        next_timestamp = next_line[3]

        if line == start_line:
            audio_start = video_start
        else:
            audio_start = offset_timestamp(get_stripped_timestamp(timestamp)[0], time_modifier)

        if line == end_line - 1:
            audio_end = video_end
        else:
            audio_end = offset_timestamp(get_stripped_timestamp(next_timestamp)[0], time_modifier)

        video_clip_duration = get_time_difference_seconds(audio_start, audio_end)

        try:
            text_end = offset_timestamp(get_stripped_timestamp(next_timestamp)[1], time_modifier)
            text_duration = get_time_difference_seconds(audio_start, text_end)
        except IndexError:
            text_duration = video_clip_duration

        if background_video is None:
            # Create variables for background clips
            video_clip_background_clip_paths = []
            total_background_clips_duration = 0

            # Get background clips for video clip if not in pictures mode
            if video_mode:
                video_map_index = line - start_line + 1
                if video_map is not None and video_map_index in video_map.keys():
                    # Get background clips from the video map
                    amount_of_background_clips = len(video_map[video_map_index])
                    for i in range(amount_of_background_clips):
                        background_clip_info = video_map[video_map_index][i]

                        background_clip_path = background_clip_info[0]
                        background_clip = mpy.VideoFileClip(background_clip_path).speedx(background_clips_speed)

                        background_clip_duration = get_background_clip_duration(
                            background_clip_path, background_clips_speed
                        )

                        # Get time offset
                        max_time_offset = get_max_time_offset(background_clip_duration)

                        background_clip_time_offset_tuple = get_time_offset_tuple(
                            background_clip_info, max_time_offset
                        )
                        background_clip_time_offset = background_clip_time_offset_tuple[0]

                        if not background_clip_time_offset_tuple[1]:
                            colored_print(
                                Fore.YELLOW,
                                f"Verse {video_map_index} background clip {i + 1} time offset is invalid, using ({background_clip_time_offset}) instead",
                            )

                        # Get max horizontal offset
                        max_horizontal_offset = get_max_horizontal_offset(background_clip.w, video_width)

                        if max_horizontal_offset < 0:
                            # Background clip width is less than video width
                            raise ValueError(
                                f"Verse {video_map_index} Background clip {i + 1} width ({background_clip.w}) is less than video width ({video_width})"
                            )

                        # Get horizontal offset
                        background_clip_horizontal_offset_tuple = get_horizontal_offset_tuple(
                            background_clip_info, max_horizontal_offset
                        )
                        background_clip_horizontal_offset = background_clip_horizontal_offset_tuple[0]

                        if not background_clip_horizontal_offset_tuple[1]:
                            colored_print(
                                Fore.YELLOW,
                                f"Verse {video_map_index} background clip {i + 1} horizontal offset is invalid, using ({background_clip_horizontal_offset}) instead",
                            )

                        # Get background clip mirrored
                        background_clip_mirrored_tuple = get_mirrored_tuple(
                            background_clip_info, allow_mirrored_background_clips
                        )
                        background_clip_mirrored = background_clip_mirrored_tuple[0]

                        if not background_clip_mirrored_tuple[1]:
                            colored_print(
                                Fore.YELLOW,
                                f"Verse {video_map_index} background clip {i + 1} mirrored ({background_clip_mirrored}) is invalid, using ({background_clip_mirrored}) instead",
                            )

                        # Adjust background clip duration
                        adjusted_background_clip_duration = background_clip_duration - background_clip_time_offset

                        video_clip_leftover_duration = video_clip_duration - total_background_clips_duration
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
                            used_background_clip_paths.append(background_clip_path)

                            total_background_clips_duration += adjusted_background_clip_duration

                            if total_background_clips_duration >= video_clip_duration:
                                break
                        else:
                            colored_print(
                                Fore.RED,
                                f"Verse {video_map_index} background clip {i + 1} duration ({background_clip_duration} : {round((video_clip_leftover_duration - background_clip_duration), 2)}) is invalid, skipping...",
                            )

                    video_clip_leftover_duration = video_clip_duration - total_background_clips_duration
                    if video_clip_leftover_duration > 0:
                        (
                            used_background_clip_paths,
                            video_map_index,
                            video_clip_background_clip_paths,
                            i,
                        ) = get_valid_background_clips(
                            all_background_clip_paths,
                            allow_duplicate_background_clips,
                            allow_mirrored_background_clips,
                            used_background_clip_paths,
                            video_map,
                            background_clips_speed,
                            video_clip_duration,
                            total_background_clips_duration,
                            video_map_index,
                            video_width,
                            video_clip_background_clip_paths,
                            i,
                        )
                else:
                    (
                        used_background_clip_paths,
                        video_map_index,
                        video_clip_background_clip_paths,
                    ) = get_valid_background_clips(
                        all_background_clip_paths,
                        allow_duplicate_background_clips,
                        allow_mirrored_background_clips,
                        used_background_clip_paths,
                        video_map,
                        background_clips_speed,
                        video_clip_duration,
                        total_background_clips_duration,
                        video_map_index,
                        video_width,
                        video_clip_background_clip_paths,
                    )[
                        :3
                    ]

                # Add background clips to video map output
                video_map_output[video_map_index] = video_clip_background_clip_paths
            else:
                background_clip_path = get_random_background_clip_path(all_background_clip_paths)

                background_clip = mpy.VideoFileClip(background_clip_path)

                # Get time offset
                background_clip_time_offset = random.uniform(0, max(0, background_clip_duration - video_clip_duration))

                # Get x offset
                width_difference = background_clip.w - video_dimensions[0]
                background_clip_horizontal_offset = random.randint(0, width_difference) if width_difference > 0 else 0

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
        colored_print(Fore.MAGENTA, f"Creating clip {line - start_line + 1}...")

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

        if line == start_line and reciter_name.lower() != "unknown":
            text_clips.append(
                create_text_clip(
                    text=reciter_name,
                    size=(video_dimensions[0] * 0.6, None),
                    color=verse_translation_color,
                    fontsize=20,
                    font=english_font,
                    position=("center", 0.20),
                    method="caption",
                    duration=text_duration,
                )
            )

        if background_video is None:
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
                video_mode=video_mode,
                background_clip_speed=background_clips_speed,
                text_duration=text_duration,
                shadow_clip=shadow_clip,
            )

            colored_print(Fore.CYAN, f"Using background clip(s):")
            for background_clip_path in video_clip_background_clip_paths:
                colored_print(Fore.CYAN, f"- {background_clip_path[0]}")

            video_clips.append(video_clip)

            colored_print(Fore.GREEN, f"Successfully created clip {line - start_line + 1}")
        else:
            # Get start time of text clips
            text_start_time = get_time_difference_seconds(audio_start, video_start)

            text_clips[0] = text_clips[0].set_start(text_start_time)
            text_clips[1] = text_clips[1].set_start(text_start_time)

            if verse_counter != "":
                text_clips[2] = text_clips[2].set_start(text_start_time)

            if line == start_line:
                text_clips[-1] = text_clips[-1].set_start(text_start_time)

            text_clips_array.extend(text_clips)

    if background_video is None:
        # Concatenate video clips, add audio, and set duration for final video
        final_video = mpy.concatenate_videoclips(clips=video_clips, method="chain").set_audio(audio)
    else:
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

        final_video = mpy.CompositeVideoClip([video, *text_clips_array], use_bgclip=True).set_audio(audio)

        video_map_output = background_video

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
        elif video_mode:
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
    background_clip_paths: list[list[str, float or int, int, str]],
    final_clip_duration: float,
    video_dimensions: tuple[int, int],
    text_clips: list[mpy.TextClip],
    video_mode: bool = True,
    background_clip_speed: float = 1.0,
    text_duration: float = None,
    shadow_clip: mpy.ColorClip = None,
) -> mpy.CompositeVideoClip:
    """
    Creates a video clip
    """

    video_width, video_height = video_dimensions
    background_clips = []

    # Specify the target aspect ratio (9:16)
    target_aspect_ratio = 9 / 16

    if video_mode:
        for background_clip_info in background_clip_paths:
            background_clip_path = background_clip_info[0]
            background_mirrored = background_clip_info[3]
            background_clip = mpy.VideoFileClip(background_clip_path).speedx(background_clip_speed)
            if background_mirrored == "True":
                background_clip = background_clip.fx(mpy.vfx.mirror_x)

            background_clip_time_offset = background_clip_info[1]
            background_clip_horizontal_offset = background_clip_info[2]

            background_clip_duration = (
                get_background_clip_duration(background_clip_path, background_clip_speed)
            ) - background_clip_time_offset

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
    else:
        background_clip = mpy.VideoFileClip(background_clip_paths[0][0])

        # Get the total number of frames
        total_frames = int(background_clip.fps * background_clip.duration)

        # Generate a random frame number
        random_frame_number = random.randint(1, total_frames)

        # Calculate the dimensions to fit the target aspect ratio
        current_aspect_ratio = background_clip.w / background_clip.h

        if current_aspect_ratio > target_aspect_ratio:
            # Video is wider than 9:16, so we need to crop the sides
            new_width = int(background_clip.h * target_aspect_ratio)
            horizontal_offset = (background_clip.w - new_width) // 2
            background_clip = background_clip.crop(x1=horizontal_offset, x2=horizontal_offset + new_width).resize(
                video_dimensions
            )

        # Seek to the random frame and capture it as an image
        random_frame = background_clip.get_frame(random_frame_number / background_clip.fps)

        # Specify the target aspect ratio (9:16)
        target_aspect_ratio = 9 / 16

        video_clip = mpy.ImageClip(random_frame)

    video_clip = video_clip.set_duration(final_clip_duration)
    text_duration = text_duration if text_duration is not None else final_clip_duration
    clips = [video_clip, shadow_clip, *text_clips] if shadow_clip is not None else [video_clip, *text_clips]
    final_video_clip = mpy.CompositeVideoClip(clips, use_bgclip=True).set_duration(final_clip_duration)

    if not video_mode:
        final_video_clip = final_video_clip.fadein(0.25).fadeout(0.25)

    return final_video_clip


def get_all_background_clip_paths(
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


def get_background_clip_duration(background_clip_path: str, background_clip_speed: float) -> float:
    return get_video_duration_seconds(background_clip_path) / background_clip_speed


def get_chapter_text(chapter):
    """
    Gets the text of a chapter from the Quran
    """

    return quran.get_sura(chapter, with_tashkeel=True)


def get_chapter_translation(chapter, language="en"):
    """
    Gets the translation of a chapter from the Quran
    """

    if language == "en":
        translation_id = 20
    elif language == "nl":
        translation_id = 235

    try:
        response = requests.get(
            f"https://api.quran.com/api/v4/quran/translations/{translation_id}?chapter_number={chapter}"
        )
        data = response.json()["translations"]
        translation = [
            re.sub("ḥ", "h", re.sub("ā", "a", re.sub(r"<.*?>*<.*?>", "", translation["text"]))) for translation in data
        ]
        return translation
    except Exception as error:
        colored_print(Fore.RED, f"Error: {error}")
        return None


def get_horizontal_offset_tuple(
    background_clip_info: list[str, float or int, int, str], max_horizontal_offset: int
) -> tuple[int, bool]:
    if (
        len(background_clip_info) > 2
        and isinstance(background_clip_info[2], int)
        and background_clip_info[2] <= max_horizontal_offset
    ):
        # Horizontal offset entry exists, is an int and is less than or equal to the max horizontal offset
        return (background_clip_info[2], True)
    else:
        return (get_random_horizontal_offset(max_horizontal_offset), False)


def get_loop_range(
    output_file_name: str, chapter_csv_lines: list[list[str]], chapter: int, start_line: int, end_line: int
):
    # Extract 'start' and 'end' values from the filename
    verse_range = (output_file_name.split(".")[1]).split(")")[0]
    start, end = verse_range.split("-") if "-" in verse_range else (verse_range, verse_range)

    # Find the corresponding lines in chapter_csv_lines
    for i, line in enumerate(chapter_csv_lines):
        if line[0] == f"{chapter}:{start}" and start_line is None:
            start_line = i + 1
        if line[0] == f"{chapter}:{end}":
            j = i + 1
            while j < len(chapter_csv_lines) and chapter_csv_lines[j][0] == "":
                j += 1
            if end_line is None:
                end_line = j

    if end_line < len(chapter_csv_lines):
        end_line += 1

    return (start_line, end_line)


def get_max_horizontal_offset(background_clip_width: int, video_width: int) -> int:
    """
    Gets the max horizontal offset for a background clip
    """

    return background_clip_width - video_width


def get_max_time_offset(background_clip_duration: float) -> float:
    """
    Gets the max time offset for a background clip
    """

    get_max_time_offset = background_clip_duration - MINIMAL_CLIP_DURATION

    return max(get_max_time_offset, 0)


def get_mirrored_tuple(
    background_clip_info: list[str, float or int, int, str], allow_mirrored_background_clips: bool
) -> tuple[str, bool]:
    if (
        len(background_clip_info) > 3
        and isinstance(background_clip_info[3], (str, bool))
        and background_clip_info[3] in ["True", "False", True, False]
    ):
        # Mirrored entry exists and is a string
        return (str(background_clip_info[3]), True)
    elif allow_mirrored_background_clips:
        return (str(random.choice([True, False])), False)
    else:
        return ("False", False)


def get_random_background_clip_path(all_background_clips_paths: list[str]) -> str:
    """
    Gets a random background clip path
    """

    return random.choice(all_background_clips_paths)


def get_random_horizontal_offset(max_horizontal_offset: int) -> int:
    """
    Returns a random horizontal offset
    """

    return random.randint(0, max_horizontal_offset)


def get_random_time_offset(max_time_offset: float) -> float:
    """
    Returns a random time offset rounded to 2 decimal places
    """

    return round(random.uniform(0, max_time_offset / 2), 2)


def get_seconds_from_timestamp(timestamp: str) -> float:
    if isinstance(timestamp, list):
        timestamp = timestamp[0]
    minutes, seconds = timestamp.split(":")
    seconds, milliseconds = seconds.split(".")
    return int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000


def get_stripped_timestamp(timestamp: str) -> str:
    return timestamp.strip().split(",")


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


def get_time_offset_tuple(
    background_clip_info: list[str, float or int, int, str], max_time_offset: float
) -> tuple[float, bool]:
    if (
        len(background_clip_info) > 1
        and (isinstance(background_clip_info[1], (float, int)))
        and background_clip_info[1] <= max_time_offset
    ):
        # Horizontal offset entry exists, is an int and is less than or equal to the max horizontal offset
        return (background_clip_info[1], True)
    else:
        return (get_random_time_offset(max_time_offset), False)


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
            background_clip_duration = get_background_clip_duration(background_clip_path, background_clips_speed)

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


def get_video_duration_seconds(video_path: str) -> float:
    """
    Get the duration of a video in seconds.
    """

    video = mpy.VideoFileClip(video_path)
    return video.duration


def modify_unsupported_arabic_letters(csv_file_path: str) -> None:
    # Define the column to modify
    column_to_modify = "ar"

    # Read and modify the CSV file
    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        fieldnames = csv_reader.fieldnames

        # Create a list to store modified rows
        modified_rows = []

        for row in csv_reader:
            if column_to_modify in row:
                # Replace the old_value with the new_value in the specified column
                row[column_to_modify] = row[column_to_modify].replace("ا۟", "ا")
                row[column_to_modify] = row[column_to_modify].replace("و۟", "و")

            modified_rows.append(row)

    # Write the modified data back to the same file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(modified_rows)

    colored_print(Fore.GREEN, "Modified unsupported arabic letters successfully")


def modify_unsupported_english_letters(csv_file_path: str) -> None:
    # Define the column to modify
    column_to_modify = "en"

    # Read and modify the CSV file
    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        fieldnames = csv_reader.fieldnames

        # Create a list to store modified rows
        modified_rows = []

        for row in csv_reader:
            if column_to_modify in row:
                # Replace the old_value with the new_value in the specified column
                row[column_to_modify] = row[column_to_modify].replace("ā", "a")
                row[column_to_modify] = row[column_to_modify].replace("ḥ", "h")
                row[column_to_modify] = row[column_to_modify].replace("ʿ", "'")

            modified_rows.append(row)

    # Write the modified data back to the same file
    with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(modified_rows)

    colored_print(Fore.GREEN, "Modified unsupported english letters successfully")


def offset_timestamp(timestamp: str, time_offset_seconds: int) -> str:
    # Parse the original time string into a timedelta object
    seconds = get_seconds_from_timestamp(timestamp)
    original_timedelta = timedelta(seconds=seconds)

    # Ensure the result remains non-negative
    new_timedelta = max(original_timedelta + timedelta(seconds=time_offset_seconds), timedelta(0))

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


def remove_substring(substring, sentence):
    ratio = fuzz.partial_ratio(substring.lower(), sentence.lower())
    threshold = 95  # Adjust as needed

    if ratio >= threshold and substring.lower() in sentence.lower():
        # Get the start and end indices of the matching substring
        start_index = sentence.lower().find(substring.lower())
        end_index = start_index + len(substring)

        # Remove the matching substring from the sentence
        modified_sentence = sentence[:start_index] + sentence[end_index:]
        return modified_sentence.strip()  # Remove leading/trailing whitespaces
    else:
        return sentence


def select_columns(csv_file_path: str, columns_to_select: list[str]) -> list[list[str]]:
    selected_data = []

    with open(csv_file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            selected_row = [row[column] for column in columns_to_select]
            selected_data.append(selected_row)

    return selected_data


def sort_nested_timestamps(timestamps):
    for i, timestamp in enumerate(timestamps):
        if isinstance(timestamp, list):
            timestamps[i] = sorted(timestamp, key=get_seconds_from_timestamp, reverse=True)
    return timestamps


if __name__ == "__main__":
    main()
