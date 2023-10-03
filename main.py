import json
import os
import random
import uuid
from datetime import datetime
from enum import Enum

import cv2
import moviepy.editor as mpy
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from compact_json import EolStyle, Formatter
from plyer import notification
from pyquran import quran

from Tiktok_uploader import uploadVideo

ARABIC_FONT = "Fonts/Hafs.ttf"
MINIMAL_CLIP_DURATION = 0.75

# TODO: Add support for clips shorter than final clip with still frames
# TODO: Add support for background clips disjoint from audio timings
# TODO: Fix pictures mode
# TODO: FIX VERTICAL OFFSET
# TODO: FIX TIMINGS ALWAYS 0.0
# TODO: ADD DURATIONS IN VIDEO MAP AND UNCOMMENT CODE IN GET_VALID_BACKGROUND_CLIPS


def main() -> None:
    tiktok = PredefinedTikToks()
    tiktok.muhammad_al_luhaidan_al_furqan_26_30()
    tiktok.run()


class MODES(Enum):
    DARK = 1
    LIGHT = 2


class ACCOUNTS(Enum):
    QURAN_2_LISTEN = 1  # crazyshocklight@hotmail.com
    LOVE_QURAN77 = 2  # crazyshocklight2@gmail.com
    QURANIC_TIKTOKS = 3  # crazyshocky@hotmail.com


class PredefinedTikToks:
    def __init__(
        self,
        directory_path: str = None,
        output_file_name: str = None,
        chapter_text_file_path: str = None,
        chapter_translation_file_path: str = None,
        start_line: int = 1,
        end_line: int = None,
        chapter: int = None,
        start_verse: int = None,
        end_verse: int = None,
        background_clips_directory_paths: list[str] = ["Anime_Clips", "Anime_Clips_2"],
        single_background_clip: str = None,
        video_map: dict = None,
        pictures_mode: bool = False,
        allow_duplicate_background_clips: bool = False,
        video_dimensions: tuple[int, int] = (576, 1024),
        y_offset: int = 0,
        background_clips_speed: float = 1.0,
        shadow_opacity: float = 0.7,
        account: ACCOUNTS = ACCOUNTS.QURAN_2_LISTEN,
        mode: MODES = MODES.DARK,
    ) -> None:
        self.directory_path = directory_path
        self.output_file_name = output_file_name
        self.chapter_text_file_path = chapter_text_file_path
        self.chapter_translation_file_path = chapter_translation_file_path
        self.start_line = start_line
        self.end_line = end_line
        self.chapter = chapter
        self.start_verse = start_verse
        self.end_verse = end_verse
        self.background_clips_directory_paths = background_clips_directory_paths
        self.single_background_clip = single_background_clip
        self.video_map = video_map
        self.pictures_mode = pictures_mode
        self.allow_duplicate_background_clips = allow_duplicate_background_clips
        self.video_dimensions = video_dimensions
        self.y_offset = y_offset
        self.background_clips_speed = background_clips_speed
        self.shadow_opacity = shadow_opacity
        self.account = account
        self.mode = mode

    def run(self) -> None:
        create_tiktok(
            directory_path=self.directory_path,
            output_file_name=self.output_file_name,
            chapter_text_file_path=self.chapter_text_file_path,
            chapter_translation_file_path=self.chapter_translation_file_path,
            start_line=self.start_line,
            end_line=self.end_line,
            chapter=self.chapter,
            start_verse=self.start_verse,
            end_verse=self.end_verse,
            background_clips_directory_paths=self.background_clips_directory_paths,
            single_background_clip=self.single_background_clip,
            video_map=self.video_map,
            pictures_mode=self.pictures_mode,
            allow_duplicate_background_clips=self.allow_duplicate_background_clips,
            video_dimensions=self.video_dimensions,
            y_offset=self.y_offset,
            background_clips_speed=self.background_clips_speed,
            shadow_opacity=self.shadow_opacity,
            account=self.account,
            mode=self.mode,
        )

    def abdul_rahman_mossad_maryam_93_98(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 93-98 of Surah Maryam by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 19 - Maryam"
        self.output_file_name = f"{self.account.name}_93-98_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_translation.txt"

    def abdul_rahman_mossad_maryam_93_94(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 93-94 of Surah Maryam by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 19 - Maryam"
        self.output_file_name = f"{self.account.name}_93-94_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_translation.txt"
        self.start_line = 1
        self.end_line = 3

    def abdul_rahman_mossad_al_ankabut_54_60(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 54-60 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut"
        self.output_file_name = f"{self.account.name}_54-60_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_translation.txt"

    def abdul_rahman_mossad_al_ankabut_56_57(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-57 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut"
        self.output_file_name = f"{self.account.name}_56-57_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_translation.txt"
        self.start_line = 6
        self.end_line = 9

    def abdul_rahman_mossad_al_muzzammil_14_18(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-18 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil"
        self.output_file_name = f"{self.account.name}_14-18_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_translation.txt"

    def abdul_rahman_mossd_al_muzzammil_14_15(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-15 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil"
        self.output_file_name = f"{self.account.name}_14-15_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_translation.txt"
        self.start_line = 1
        self.end_line = 3

    def abdul_rahman_mossad_al_ghashiyah_10_26(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 10-26 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah"
        self.output_file_name = f"{self.account.name}_10-26_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\chapter_translation.txt"

    def abdul_rahman_mossad_al_ghashiyah_10_12(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 10-12 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah"
        self.output_file_name = f"{self.account.name}_10-12_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\chapter_translation.txt"
        self.start_line = 1
        self.end_line = 3

    def abdul_rahman_mossad_al_adiyat_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Al-'Adiyat by Abdul Rahman Mossad
        """

        self.directory_path = r"Surahs\Abdul Rahman Mossad - 100 - Al-'Adiyat"
        self.output_file_name = f"{self.account.name}_1-11_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Abdul Rahman Mossad - 100 - Al-'Adiyat\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Abdul Rahman Mossad - 100 - Al-'Adiyat\chapter_translation.txt"

    def ahmed_khedr_taha_14_16(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 14-16 of Surah Taha by Ahmed Khedr
        """

        self.directory_path = r"Surahs\Ahmed Khedr - 20 - Taha"
        self.output_file_name = f"{self.account.name}_14-16_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Ahmed Khedr - 20 - Taha\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Ahmed Khedr - 20 - Taha\chapter_translation.txt"

    def fatih_seferagic_ayatul_kursi_255(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 255 of Surah Al-Baqarah by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi"
        self.output_file_name = f"{self.account.name}_255_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi\chapter_translation.txt"

    def fatih_seferagic_an_nisa_155_160(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 155-160 of Surah An-Nisa by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 4 - An-Nisa"
        self.output_file_name = f"{self.account.name}_155-160_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 4 - An-Nisa\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 4 - An-Nisa\chapter_translation.txt"

    def fatih_seferagic_an_nur_35(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 35 of Surah An-Nur by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 24 - An-Nur"
        self.output_file_name = f"{self.account.name}_35_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 24 - An-Nur\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 24 - An-Nur\chapter_translation.txt"

    def fatih_seferagic_al_hujurat_10(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 10 of Surah Al-Hujurat by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 49 - Al-Hujurat"
        self.output_file_name = f"{self.account.name}_10_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\chapter_translation.txt"

    def fatih_seferagic_al_hashr_21_24(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 21-24 of Surah Al-Hashr by Fatih Seferagic
        """

        self.directory_path = r"Surahs\Fatih Seferagic - 59 - Al-Hashr"
        self.output_file_name = f"{self.account.name}_21-24_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Fatih Seferagic - 59 - Al-Hashr\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Fatih Seferagic - 59 - Al-Hashr\chapter_translation.txt"

    def mansour_as_salimi_maryam_27_33(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 27-33 of Surah Maryam by Mansour As Salimi
        """

        self.directory_path = r"Surahs\Mansour As Salimi - 19 - Maryam"
        self.output_file_name = f"{self.account.name}_27-33_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Mansour As Salimi - 19 - Maryam\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Mansour As Salimi - 19 - Maryam\chapter_translation.txt"

    def mansour_as_salimi_yusuf_1_5(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-5 of Surah Yusuf by Mansour As Salimi
        """

        self.directory_path = r"Surahs\Mansour As Salimi - 12 - Yusuf"
        self.output_file_name = f"{self.account.name}_1-5_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Mansour As Salimi - 12 - Yusuf\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Mansour As Salimi - 12 - Yusuf\chapter_translation.txt"

    def muhammad_al_luhaidan_al_baqarah_273_274(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 273-274 of Surah Al-Baqarah by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 2 - Al-Baqarah"
        self.output_file_name = f"{self.account.name}_273-274_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 2 - Al-Baqarah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 2 - Al-Baqarah\chapter_translation.txt"

    def muhammad_al_luhaidan_al_anam_27_30(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 27-30 of Surah Al-An'am by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am"
        self.output_file_name = f"{self.account.name}_27-30_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am\chapter_translation.txt"

    def muhammad_al_luhaidan_maryam_85_92(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 85-92 of Surah Maryam by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 19 - Maryam"
        self.output_file_name = f"{self.account.name}_85-92_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 19 - Maryam\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 19 - Maryam\chapter_translation.txt"

    def muhammad_al_luhaidan_taha_105_108(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 105-108 of Surah Taha by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 20 - Taha"
        self.output_file_name = f"{self.account.name}_105-108_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 20 - Taha\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 20 - Taha\chapter_translation.txt"

    def muhammad_al_luhaidan_al_furqan_26_30(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 25-30 of Surah Al-Furqan by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan - 2"
        self.output_file_name = f"{self.account.name}_26-30_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan - 2\chapter_text.txt"
        self.chapter_translation_file_path = (
            r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan - 2\chapter_translation.txt"
        )

    def muhammad_al_luhaidan_al_furqan_72_77(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 72-77 of Surah Al-Furqan by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan"
        self.output_file_name = f"{self.account.name}_72-77_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 25 - Al-Furqan\chapter_translation.txt"

    def muhammad_al_luhaidan_al_haqqah_29_33(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 29-33 of Surah Al-Haqqah by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 69 - Al-Haqqah"
        self.output_file_name = f"{self.account.name}_29-33_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 69 - Al-Haqqah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 69 - Al-Haqqah\chapter_translation.txt"

    def muhammad_al_luhaidan_al_insan_20_22(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 20-22 of Surah Al-Insan by Muhammad Al-Luhaidan
        """

        self.directory_path = r"Surahs\Muhammad Al-Luhaidan - 76 - Al-Insan"
        self.output_file_name = f"{self.account.name}_20-22_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammad Al-Luhaidan - 76 - Al-Insan\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammad Al-Luhaidan - 76 - Al-Insan\chapter_translation.txt"

    def muhammadloiq_qori_al_ahzab_35(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 35 of Surah Al-Ahzab by Muhammadloiq Qori
        """

        self.directory_path = r"Surahs\Muhammadloiq Qori - 33 - Al-Ahzab"
        self.output_file_name = f"{self.account.name}_353_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Muhammadloiq Qori - 33 - Al-Ahzab\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Muhammadloiq Qori - 33 - Al-Ahzab\chapter_translation.txt"

    def salim_bahanan_al_fatihah_2_7(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 2-7 of Surah Al-Fatihah by Salim Bahanan
        """

        self.directory_path = r"Surahs\Salim Bahanan - 1 - Al-Fatihah"
        self.output_file_name = f"{self.account.name}_2-7_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_translation.txt"

    def salim_bahanan_ad_duhaa_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Ad-Duhaa by Salim Bahanan
        """

        self.directory_path = r"Surahs\Salim Bahanan - 93 - Ad-Duhaa"
        self.output_file_name = f"{self.account.name}_1-11_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\chapter_translation.txt"

    def salim_bahanan_al_qariah_1_11(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-11 of Surah Al-Qariah by Salim Bahanan
        """

        self.directory_path = r"Surahs\Salim Bahanan - 101 - Al-Qariah"
        self.output_file_name = f"{self.account.name}_1-11_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Salim Bahanan - 101 - Al-Qariah\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Salim Bahanan - 101 - Al-Qariah\chapter_translation.txt"

    def salim_bahanan_at_tin_1_8(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 1-8 of Surah At-Tin by Salim Bahanan
        """

        self.directory_path = r"Surahs\Salim Bahanan - 95 - At-Tin"
        self.output_file_name = f"{self.account.name}_1-8_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Salim Bahanan - 95 - At-Tin\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Salim Bahanan - 95 - At-Tin\chapter_translation.txt"

    def unknown_al_furqan_72_75(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 72-75 of Surah Al-Furqan by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - 25 - Al-Furqan"
        self.output_file_name = f"{self.account.name}_72-75_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - 25 - Al-Furqan\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - 25 - Al-Furqan\chapter_translation.txt"

    def unknown_al_ankabut_56_58(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-58 of Surah Al-'Ankabut by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - 29 - Al-'Ankabut"
        self.output_file_name = f"{self.account.name}_56-58_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_translation.txt"

    def unknown_al_ankabut_56_57(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 56-57 of Surah Al-'Ankabut by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - 29 - Al-'Ankabut"
        self.output_file_name = f"{self.account.name}_56-57_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_translation.txt"
        self.start_line = 1
        self.end_line = 4

    def unknown_taha_124_126(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 124-126 of Surah Taha by an unknown reciter
        """

        self.directory_path = r"Surahs\Unknown - 20 - Taha"
        self.output_file_name = f"{self.account.name}_124-126_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Unknown - 20 - Taha\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Unknown - 20 - Taha\chapter_translation.txt"

    def yasser_al_dosari_al_muminun_34_39(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verses 34-39 of Surah Al-Mu'minun by Yasser Al-Dosari
        """

        self.directory_path = r"Surahs\Yasser Al-Dosari - 23 - Al-Mu'minun"
        self.output_file_name = f"{self.account.name}_34-39_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Yasser Al-Dosari - 23 - Al-Mu'minun\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Yasser Al-Dosari - 23 - Al-Mu'minun\chapter_translation.txt"

    def yasser_al_dosari_al_fath_29(self) -> None:
        """
        Modifies the parameters of the class for a TikTok video for verse 29 of Surah Al-Fath by Yasser Al-Dosari
        """

        self.directory_path = r"Surahs\Yasser Al-Dosari - 48 - Al-Fath"
        self.output_file_name = f"{self.account.name}_29_{str(uuid.uuid4()).split('-')[-1]}"
        self.chapter_text_file_path = r"Surahs\Yasser Al-Dosari - 48 - Al-Fath\chapter_text.txt"
        self.chapter_translation_file_path = r"Surahs\Yasser Al-Dosari - 48 - Al-Fath\chapter_translation.txt"


def create_tiktok(
    directory_path: str,
    output_file_name: str = None,
    output_file_path: str = None,
    audio_file_path: str = None,
    chapter_text_file_path: str = None,
    chapter_translation_file_path: str = None,
    start_line: int = 1,
    end_line: int = None,
    chapter: int = None,
    start_verse: int = None,
    end_verse: int = None,
    background_clips_directory_paths: list[str] = ["Anime_Clips"],
    single_background_clip: str = None,
    video_map: dict = None,
    pictures_mode: bool = False,
    allow_duplicate_background_clips: bool = False,
    video_dimensions: tuple[int, int] = (576, 1024),
    y_offset: int = 0,
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
        if output_file_name is None:
            output_file_path = os.path.join(
                directory_path,
                rf"Videos\{account.name}_{str(uuid.uuid4()).split('-')[-1]}.mp4",
            )
        else:
            output_file_path = os.path.join(directory_path, rf"Videos\{output_file_name}.mp4")
    else:
        output_directory = "\\".join(output_file_path.split("\\")[:-1])
        if os.path.isdir(output_directory):
            os.makedirs(output_directory, exist_ok=True)

    # Create audio file path if it doesn't exist
    if audio_file_path is None:
        for json_file in os.listdir(directory_path):
            if json_file.endswith(".mp3"):
                audio_file_path = os.path.join(directory_path, json_file)
                break

    # Change font based on account
    match account:
        case ACCOUNTS.QURAN_2_LISTEN:
            english_font = "Fonts/Butler_Regular.otf"
        case ACCOUNTS.LOVE_QURAN77:
            english_font = "Fonts/Sk-Modernist-Regular.otf"
        case ACCOUNTS.QURANIC_TIKTOKS:
            english_font = "Fonts/FreshStart.otf"

    # Change colors based on mode
    match mode:
        case MODES.DARK:
            shadow_color = (0, 0, 0)
            verse_text_color = "rgb(255, 255, 255)"
            verse_translation_color = "rgb(255, 255, 255)"
        case MODES.LIGHT:
            shadow_color = (255, 255, 255)
            verse_text_color = "rgb(0, 0, 0)"
            verse_translation_color = "rgb(0, 0, 0)"

    # Create chapter text file if it doesn't exist and populate it with the chapter text
    if chapter_text_file_path is None:
        new_chapter_text_file_path = os.path.join(directory_path, "chapter_text.txt")

        if not os.path.isfile(new_chapter_text_file_path):
            with open(new_chapter_text_file_path, "w", encoding="utf-8") as chapter_text_file:
                for verse in range(start_verse, end_verse + 1):
                    verse_text = get_verse_text(chapter, verse)

                    if verse_text is not None:
                        chapter_text_file.write(verse_text + "\n")
                    else:
                        break
    else:
        if not os.path.isfile(chapter_text_file_path):
            colored_print(Fore.RED, "Chapter text file not found")
            return

    # Create chapter translation file if it doesn't exist and populate it with the chapter translation
    if chapter_translation_file_path is None:
        new_chapter_translation_file_path = os.path.join(directory_path, "chapter_translation.txt")

        if not os.path.isfile(new_chapter_translation_file_path):
            with open(new_chapter_translation_file_path, "w", encoding="utf-8") as chapter_translation_file:
                for verse in range(start_verse, end_verse + 1):
                    verse_translation = get_verse_translation(chapter, verse)

                    if verse_translation is not None:
                        chapter_translation_file.write(verse_translation + "\n")
                    else:
                        break
    else:
        if not os.path.isfile(chapter_translation_file_path):
            colored_print(Fore.RED, "Chapter translation file not found")
            return

    # Await user input to edit text file(s) if they were just created
    if chapter_text_file_path is None or chapter_translation_file_path is None:
        colored_input(Fore.YELLOW, "Appropriately edit text file(s) now...")

    # Create timestamps text file if it doesn't exist and populate it with the timestamps or update it if it does exist
    if os.path.isdir(directory_path):
        timestamps_csv_file_path = os.path.join(directory_path, "Markers.csv")

        if os.path.isfile(timestamps_csv_file_path):
            create_timestamps_txt_file(timestamps_csv_file_path)

            timestamps_txt_file_path = timestamps_csv_file_path.replace("Markers.csv", "timestamps.txt")
        else:
            colored_print(Fore.RED, "Markers.csv file not found")
            return
    else:
        colored_print(Fore.RED, "Directory not found")
        return

    # Read text file(s)
    with open(chapter_text_file_path, "r", encoding="utf-8") as chapter_text_file, open(
        chapter_translation_file_path, "r", encoding="utf-8"
    ) as chapter_translation_file, open(timestamps_txt_file_path, "r", encoding="utf-8") as timestamps_file:
        chapter_text_lines = chapter_text_file.readlines()
        chapter_translation_lines = chapter_translation_file.readlines()
        timestamps_lines = timestamps_file.readlines()

        # Create the range of lines to loop through
        if end_line is None:
            end_line = len(chapter_text_lines)

        end_line += 1
        loop_range = range(start_line, end_line)

        # Get data for final video
        video_width, video_height = video_dimensions
        video_start = timestamps_lines[start_line - 1].strip().split(",")[0]
        video_end = timestamps_lines[end_line - 1].strip().split(",")[0]

        if single_background_clip is not None:
            background_clip = mpy.VideoFileClip(single_background_clip).subclip(video_start)

            # Specify the target aspect ratio (9:16)
            target_aspect_ratio = 9 / 16

            # Calculate the dimensions to fit the target aspect ratio without resizing
            background_clip_width, background_clip_height = background_clip.size
            current_aspect_ratio = background_clip_width / background_clip_height

            if current_aspect_ratio > target_aspect_ratio:
                # Video is wider than 9:16, so we need to crop the sides
                new_width = int(background_clip_height * target_aspect_ratio)
                horizontal_offset = (background_clip_width - new_width) // 2
                background_clip = background_clip.crop(x1=horizontal_offset, x2=horizontal_offset + new_width).resize(
                    video_dimensions
                )
            else:
                # Video is taller than 9:16, so we need to crop the top and bottom
                new_height = int(background_clip_width / target_aspect_ratio)
                y_offset = (background_clip_height - new_height) // 2
                background_clip = background_clip.crop(y1=y_offset, y2=y_offset + new_height).resize(video_dimensions)

            # Create shadow clip
            shadow_clip = create_shadow_clip(
                size=(background_clip_width, background_clip_height),
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
            verse_text = chapter_text_lines[i - 1].strip()
            verse_translation = chapter_translation_lines[i - 1].strip()

            audio_start = timestamps_lines[i - 1].strip().split(",")[0]
            audio_end = timestamps_lines[i].strip().split(",")[0]

            video_clip_duration = get_time_difference_seconds(audio_start, audio_end)

            # Get text duration
            try:
                text_end = timestamps_lines[i].strip().split(",")[1]
                text_duration = get_time_difference_seconds(audio_start, text_end)
            except IndexError:
                text_duration = video_clip_duration

            if single_background_clip is None:
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

                        # Delete video map entry
                        del video_map[i]

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

                    video_clip_background_clip_paths.append(
                        [
                            background_clip_path,
                            background_clip_time_offset,
                            background_clip_horizontal_offset,
                        ]
                    )

            # Start creating video clip
            colored_print(Fore.GREEN, f"Creating clip {i}...")

            # Create text clips
            text_clips = [
                create_text_clip(
                    text=verse_text,
                    size=video_dimensions,
                    color=verse_text_color,
                    fontsize=44,
                    font=ARABIC_FONT,
                    position=(0, -0.05),
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

            if single_background_clip:
                # Get start time of text clips
                text_start_time = get_time_difference_seconds(audio_start, video_start)

                text_clips[0] = text_clips[0].set_start(text_start_time)
                text_clips[1] = text_clips[1].set_start(text_start_time)

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
                    y_offset=y_offset,
                    text_duration=text_duration,
                    shadow_clip=shadow_clip,
                )

                video_clips.append(video_clip)

        audio = mpy.AudioFileClip(audio_file_path).set_start(video_start).subclip(video_start, video_end)

        if single_background_clip is not None:
            final_video = (
                mpy.CompositeVideoClip([video, *text_clips_array], use_bgclip=True)
                .set_start(video_start)
                .set_audio(audio)
            )

            video_map_output = single_background_clip
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
            if single_background_clip:
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
        except Exception as error:
            colored_print(Fore.RED, f"Error: {error}")
            return

        # Create notification to indicate that the video has been created
        create_notification(title="TikTok Video Created", message=f"Video created for {directory_path}")


def create_video_clip(
    background_clip_paths: list[list[str, float or None, int or None]],
    final_clip_duration: float,
    video_dimensions: tuple[int, int],
    text_clips: list[mpy.TextClip],
    still_frame: bool = False,
    background_clip_speed: float = 1.0,
    y_offset: int = 0,
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
            background_clip = mpy.VideoFileClip(background_clip_path).speedx(background_clip_speed)

            background_clip_time_offset = background_clip_info[1]
            background_clip_horizontal_offset = background_clip_info[2]

            background_clip_duration = (
                get_video_duration_seconds(background_clip_path) / background_clip_speed - background_clip_time_offset
            )

            # Crop, trim and set duration for background clip
            background_clip = (
                background_clip.crop(
                    x1=background_clip_horizontal_offset,
                    y1=y_offset,
                    x2=background_clip_horizontal_offset + video_width,
                    y2=y_offset + video_height,
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


def get_verse_translation(chapter, verse):
    """
    Gets the translation of a verse from the Quran
    """

    try:
        response = requests.get(f"https://api.quran.com/api/v4/quran/translations/20?verse_key={chapter}:{verse}")
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

    return random.uniform(0, max_time_offset)


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

                video_clip_background_clip_paths.append(
                    [
                        background_clip_path,
                        background_clip_time_offset,
                        background_clip_horizontal_offset,
                    ]
                )
                used_background_clips_paths.append(background_clip_path)

                background_clips_duration += adjusted_background_clip_duration
                j += 1

                if background_clips_duration >= video_clip_duration:
                    break

    return (used_background_clips_paths, i, video_clip_background_clip_paths, j)


if __name__ == "__main__":
    main()
