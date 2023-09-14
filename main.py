import cv2
import moviepy.editor as mpy
import os
import random
import requests
import uuid
from bs4 import BeautifulSoup
from colorama import Fore, Style
from datetime import datetime
from enum import Enum
from plyer import notification
from pyquran import quran
from Tiktok_uploader import uploadVideo

ARABIC_FONT = "Fonts/Hafs.ttf"

def main() -> None:
    PredefinedTikToks(
        account=ACCOUNTS.QURAN_2_LISTEN, 
    ).abdul_rahman_mossad_maryam_93_98()

class MODES(Enum):
    DARK = 1
    LIGHT = 2

class ACCOUNTS(Enum):
    QURAN_2_LISTEN = 1 # crazyshocklight@hotmail.com
    LOVE_QURAN77 = 2 # crazyshocklight2@gmail.com
    QURANIC_TIKTOKS = 3 # crazyshocky@hotmail.com

def colored_print(color: str, text: str) -> None:
    """
    Prints text in color
    """

    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{current_time}] {text}{Style.RESET_ALL}")

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

        # Convert the time difference to seconds as a float
        time_difference_seconds = time_difference.total_seconds()

        return time_difference_seconds

def get_video_duration_seconds(video_path: str) -> float:
        """
        Get the duration of a video in seconds.
        """

        video = cv2.VideoCapture(video_path)
        duration_seconds = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
        return duration_seconds

def create_notification(title: str, message: str) -> None:
        """
        Create a notification with the given parameters.
        """

        notification.notify(
            title=title,
            message=message,
            app_name="Python",
            timeout=1
        )

class Quran:
    def get_verse_text(self, chapter, verse):
        """
        Gets the text of a verse from the Quran
        """

        verse_text = quran.get_verse(chapter, verse, with_tashkeel=True)
        if verse_text is None or verse_text == "":
            colored_print(Fore.RED, f"Verse {verse} not found")
            return None
        return verse_text
    
    def get_verse_translation(self, chapter, verse):
        """
        Gets the translation of a verse from the Quran
        """

        try:
            response = requests.get(f"https://api.quran.com/api/v4/quran/translations/20?verse_key={chapter}:{verse}")
            translation = response.json()["translations"][0]["text"]
            soup = BeautifulSoup(translation, "html.parser")
            clean_text = soup.get_text()
            return clean_text
        except Exception as error:
            colored_print(Fore.RED, f"Error: {error}")
            return None

class PredefinedTikToks():
    def __init__(
            self,
            account: ACCOUNTS= ACCOUNTS.QURAN_2_LISTEN,
            background_clips_directory_path: str="Anime_Clips",
            background_clips_speed: float=1.0,
            hash_map: dict=None,
            mode: MODES=MODES.DARK,
            shadow_opacity: float=0.7,
            duplicates_allowed: bool=False,
            codec: str="libx264",
            dimensions: tuple[int, int]=(576, 1024),
            x_offset: int=0,
            y_offset: int=0
        ) -> None:
        self.account = account
        self.background_clips_directory_path = background_clips_directory_path
        self.background_clips_speed = background_clips_speed
        self.hash_map = hash_map
        self.mode = mode
        self.shadow_opacity = shadow_opacity
        self.duplicates_allowed = duplicates_allowed
        self.codec = codec
        self.dimensions = dimensions
        self.x_offset = x_offset
        self.y_offset = y_offset

    def abdul_rahman_mossad_maryam_93_98(self) -> None:
        """
        Creates a TikTok video for verses 93-98 of Surah Maryam by Abdul Rahman Mossad
        """

        create_tiktok(
            directory_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 19 - Maryam\Videos\{self.account}_93-98_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def abdul_rahman_mossad_al_ankabut_54_62(self) -> None:
        """
        Creates a TikTok video for verses 54-62 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        create_tiktok(
            directory_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\Videos\{self.account}_54-62_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def abdul_rahman_mossad_al_ankabut_56_57(self) -> None:
        """
        Creates a TikTok video for verses 56-57 of Surah Al-'Ankabut by Abdul Rahman Mossad
        """

        create_tiktok(
            directory_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\Videos\{self.account}_56-57_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_translation.txt",
            start_line=6,
            end_line=9,
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def abdul_rahman_mossad_al_muzzammil_14_18(self) -> None:
        """
        Creates a TikTok video for verses 14-18 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        create_tiktok(
            directory_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\Videos\{self.account}_14-18_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def abdul_rahman_mossd_al_muzzammil_14_15(self) -> None:
        """
        Creates a TikTok video for verses 14-15 of Surah Al-Muzzammil by Abdul Rahman Mossad
        """

        create_tiktok(
            directory_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\Videos\{self.account}_14-15_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_translation.txt",
            start_line=1,
            end_line=3,
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def abdul_rahman_mossad_al_ghashiyah_10_26(self) -> None:
        """
        Creates a TikTok video for verses 10-26 of Surah Al-Ghashiyah by Abdul Rahman Mossad
        """

        create_tiktok(
            directory_path=r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\Videos\{self.account}_10-26_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def fatih_seferagic_ayatul_kursi_255(self) -> None:
        """
        Creates a TikTok video for Ayatul Kursi by Fatih Seferagic
        """

        create_tiktok(
            directory_path=r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi",
            output_file_path=rf"Surahs\Fatih Seferagic - 2 - Ayatul Kursi\Videos\{self.account}_255_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Fatih Seferagic - 2 - Ayatul Kursi\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )
    
    def fatih_seferagic_al_hujurat_10(self) -> None:
        """
        Creates a TikTok video for verse 10 of Surah Al-Hujurat by Fatih Seferagic
        """

        create_tiktok(
            directory_path=r"Surahs\Fatih Seferagic - 49 - Al-Hujurat",
            output_file_path=rf"Surahs\Fatih Seferagic - 49 - Al-Hujurat\Videos\{self.account}_10_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )
    
    def fatih_seferagic_al_hashr_21_24(self) -> None:
        """
        Creates a TikTok video for verses 21-24 of Surah Al-Hashr by Fatih Seferagic
        """

        create_tiktok(
            directory_path=r"Surahs\Fatih Seferagic - 49 - Al-Hashr",
            output_file_path=rf"Surahs\Fatih Seferagic - 49 - Al-Hashr\Videos\{self.account}_21-24_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hashr\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hashr\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hashr\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def muhammad_al_luhaidan_al_anam_27_30(self) -> None:
        """
        Creates a TikTok video for verses 27-30 of Surah Al-An'am by Muhammad Al-Luhaidan
        """

        create_tiktok(
            directory_path=r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am",
            output_file_path=rf"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am\Videos\{self.account}_27-30_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Muhammad Al-Luhaidan - 6 - Al-An'am\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def salim_bahanan_al_fatihah_2_7(self) -> None:
        """
        Creates a TikTok video for verses 2-7 of Surah Al-Fatihah by Salim Bahanan
        """

        create_tiktok(
            directory_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah",
            output_file_path=rf"Surahs\Salim Bahanan - 1 - Al-Fatihah\Videos\{self.account}_2-7_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def salim_bahanan_ad_duhaa_1_11(self) -> None:
        """
        Creates a TikTok video for verses 1-11 of Surah Ad-Duhaa by Salim Bahanan
        """

        create_tiktok(
            directory_path=r"Surahs\Salim Bahanan - 93 - Ad-Duhaa",
            output_file_path=rf"Surahs\Salim Bahanan - 93 - Ad-Duhaa\Videos\{self.account}_1-11_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            hash_map=self.hash_map,
            mode=self.mode,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def salim_bahanan_al_qariah_1_11(self) -> None:
        """
        Creates a TikTok video for verses 1-11 of Surah Al-Qariah by Salim Bahanan
        """

        create_tiktok(
            directory_path=r"Surahs\Salim Bahanan - 101 - Al-Qariah",
            output_file_path=rf"Surahs\Salim Bahanan - 101 - Al-Qariah\Videos\{self.account}_1-11_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qariah\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qariah\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qariah\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def unknown_al_furqan_72_75(self) -> None:
        """
        Creates a TikTok video for verses 72-75 of Surah Al-Furqan by an unknown reciter
        """

        create_tiktok(
            directory_path=r"Surahs\Unknown - 25 - Al-Furqan",
            output_file_path=rf"Surahs\Unknown - 25 - Al-Furqan\Videos\{self.account}_72-75_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Unknown - 25 - Al-Furqan\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Unknown - 25 - Al-Furqan\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Unknown - 25 - Al-Furqan\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

    def unknown_al_ankabut_56_58(self) -> None:
        """
        Creates a TikTok video for verses 56-58 of Surah Al-'Ankabut by an unknown reciter
        """

        create_tiktok(
            directory_path=r"Surahs\Unknown - 29 - Al-'Ankabut",
            output_file_path=rf"Surahs\Unknown - 29 - Al-'Ankabut\Videos\{self.account}_56-58_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset
        )
    
    def unknown_al_ankabut_56_57(self) -> None:
        """
        Creates a TikTok video for verses 56-57 of Surah Al-'Ankabut by an unknown reciter
        """

        create_tiktok(
            directory_path=r"Surahs\Unknown - 29 - Al-'Ankabut",
            output_file_path=rf"Surahs\Unknown - 29 - Al-'Ankabut\Videos\{self.account}_56-57_{uuid.uuid4()}",
            audio_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\audio.mp3",
            account=self.account,
            chapter_text_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_translation.txt",
            start_line=1,
            end_line=4,
            background_clips_directory_path=self.background_clips_directory_path,
            background_clips_speed=self.background_clips_speed,
            shadow_opacity=self.shadow_opacity,
            duplicates_allowed=self.duplicates_allowed,
            codec=self.codec,
            dimensions=self.dimensions,
            x_offset=self.x_offset,
            y_offset=self.y_offset,
        )

def create_tiktok(
        directory_path: str,
        output_file_path: str,
        audio_file_path: str,
        account: ACCOUNTS= ACCOUNTS.QURAN_2_LISTEN,
        chapter_text_file_path: str="chapter_text.txt",
        chapter_translation_file_path: str="chapter_translation.txt",
        start_line: int=1,
        end_line: int=None,
        chapter: int=None,
        start_verse: int=None,
        end_verse: int=None,
        background_clips_directory_path: str="Anime_Clips",
        background_clips_speed: float=1.0,
        hash_map: dict=None,
        mode: MODES=MODES.DARK,
        shadow_opacity: float=0.7,
        duplicates_allowed: bool=False,
        codec: str="libx264",
        dimensions: tuple[int, int]=(576, 1024),
        x_offset: int=0,
        y_offset: int=0
    ) -> None:
    """
    Creates a TikTok video
    """

    if os.path.isdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, "timestamps.txt")):
            timestamps_txt_file_path = os.path.join(directory_path, "timestamps.txt")
        elif os.path.isfile(os.path.join(directory_path, "Markers.csv")):
            timestamps_csv_file_path = os.path.join(directory_path, "Markers.csv")
            create_timestamps_txt_file(timestamps_csv_file_path)
            timestamps_txt_file_path = timestamps_csv_file_path.replace("Markers.csv", "timestamps.txt")
        else:
            colored_print(Fore.RED, "Markers.csv file not found")
            return
    else:
        colored_print(Fore.RED, "Directory not found")
        return
    if codec == "libx264" or codec == "libx265" or codec == "mpeg4":
        output_file_path = output_file_path + ".mp4"
    elif codec == "rawvideo" or codec == "png":
        output_file_path = output_file_path + ".avi"
    if account == ACCOUNTS.QURAN_2_LISTEN:
        english_font = "Fonts/Butler_Regular.otf"
    elif account == ACCOUNTS.LOVE_QURAN77:
        english_font = "Fonts/Lato-Semibold.ttf"
    elif account == ACCOUNTS.QURANIC_TIKTOKS:
        english_font = "Fonts/Fontspring-DEMO-proximanovaexcn-regular.otf"
        session_id = "8877ca2daba37ca9acea9b798208e9b0"
    if mode == MODES.DARK:
        shadow_color = (0, 0, 0)
        verse_text_color = "rgb(255, 255, 255)"
        verse_translation_color = "rgb(255, 255, 255)"
    elif mode == MODES.LIGHT:
        shadow_color = (255, 255, 255)
        verse_text_color = "rgb(0, 0, 0)"
        verse_translation_color = "rgb(0, 0, 0)"
    if chapter_text_file_path == "chapter_text.txt":
        with open(chapter_text_file_path, "w", encoding="utf-8") as chapter_text_file:
            verse_text = Quran.get_verse_text(chapter, start_verse)
            if verse_text is None:
                return
            for current_verse in range(start_verse, end_verse + 1):
                verse_text = Quran.get_verse_text(chapter, current_verse)
                if verse_text is not None:
                    chapter_text_file.write(verse_text + "\n")
                else:
                    break
    else:
        if not os.path.isfile(chapter_text_file_path):
            colored_print(Fore.RED, "Chapter text file not found")
            return
    if chapter_translation_file_path == "chapter_translation.txt":
        with open(chapter_translation_file_path, "w", encoding="utf-8") as chapter_translation_file:
            verse_translation = Quran.get_verse_translation(chapter, start_verse)
            if verse_translation is None:
                return
            for current_verse in range(start_verse, end_verse + 1):
                verse_translation = Quran.get_verse_translation(chapter, current_verse)
                if verse_translation is not None:
                    chapter_translation_file.write(verse_translation + "\n")
                else:
                    break
    else:
        if not os.path.isfile(chapter_translation_file_path):
            colored_print(Fore.RED, "Chapter translation file not found")
            return
    used_background_clips = []
    video_clips = []
    with open(chapter_text_file_path, "r", encoding="utf-8") as chapter_text_file, \
    open(chapter_translation_file_path, "r", encoding="utf-8") as chapter_translation_file, \
    open(timestamps_txt_file_path, "r", encoding="utf-8") as timestamps_file:
        chapter_text_lines = chapter_text_file.readlines()
        chapter_translation_lines = chapter_translation_file.readlines()
        timestamps_lines = timestamps_file.readlines()
        if end_line is None:
            end_line = len(chapter_text_lines) + 1
        loop_range = range(start_line, end_line)
        for i in loop_range:
            verse_text = chapter_text_lines[i - 1].strip()
            verse_translation = chapter_translation_lines[i - 1].strip()
            audio_start = timestamps_lines[i - 1].strip().split(",")[0]
            audio_end = timestamps_lines[i].strip().split(",")[0]
            final_clip_duration = get_time_difference_seconds(audio_start, audio_end)
            try:
                text_end = timestamps_lines[i].strip().split(",")[1]
                text_duration = get_time_difference_seconds(audio_start, text_end)
            except IndexError:
                text_duration = final_clip_duration
            if hash_map is None or (hash_map is not None and i not in hash_map):
                all_background_clips = [clip for clip in os.listdir(background_clips_directory_path) if clip.endswith(".mp4")]
                while True:
                    background_clip = random.choice(all_background_clips)
                    if hash_map is None or (hash_map is not None and background_clip not in hash_map.values()):
                        background_clip_path = os.path.join(background_clips_directory_path, background_clip)
                        background_clip_duration = get_video_duration_seconds(background_clip_path)
                        if background_clip_duration / background_clips_speed >= final_clip_duration:
                            if duplicates_allowed or (not duplicates_allowed and background_clip not in used_background_clips):
                                used_background_clips.append(background_clip)
                                break
            else:
                background_clip_name = hash_map[i]
                background_clip_path = os.path.join(background_clips_directory_path, background_clip_name)
                background_clip_duration = get_video_duration_seconds(background_clip_path)
                if background_clip_duration / background_clips_speed < final_clip_duration:
                    colored_print(Fore.RED, f"Background clip duration is less than video clip duration for clip {i}")
                    return
                else:
                    used_background_clips.append(background_clip_name)
                    del hash_map[i]
            colored_print(Fore.GREEN, f"Creating clip {i}...")
            text_clips = [
                create_text_clip(
                    text=verse_text,
                    size=dimensions,
                    color=verse_text_color,
                    fontsize=45,
                    font=ARABIC_FONT,
                    position=(0, -.05),
                    duration=text_duration
                ),
                create_text_clip(
                    text=verse_translation,
                    size=(dimensions[0] * .6, None),
                    color=verse_translation_color,
                    fontsize=18,
                    font=english_font,
                    position=("center", .49),
                    method="caption",
                    duration=text_duration
                )
            ]
            shadow_clip = create_shadow_clip(
                size=dimensions,
                color=shadow_color,
                duration=final_clip_duration,
                opacity=shadow_opacity
            )
            video_clip = create_video_clip(
                background_clip_path=background_clip_path,
                final_clip_duration=final_clip_duration,
                dimensions=dimensions,
                text_clips=text_clips,
                background_clip_speed=background_clips_speed,
                x_offset=x_offset,
                y_offset=y_offset,
                text_duration=text_duration,
                shadow_clip=shadow_clip,
            )
            video_clips.append(video_clip)
        final_video_start = timestamps_lines[start_line - 1].strip().split(",")[0]
        final_video_end = timestamps_lines[end_line - 1].strip().split(",")[0]
        final_video_duration = get_time_difference_seconds(final_video_start, final_video_end)
        final_video = mpy.concatenate_videoclips(
            clips=video_clips,
            method="chain"
        ).set_audio(
            mpy.AudioFileClip(audio_file_path).set_start(final_video_start).subclip(final_video_start, final_video_end)
        ).set_duration(
            final_video_duration - .03
        )
        colored_print(Fore.GREEN, "Creating final video...")
        try:
            final_video.write_videofile(
                filename=output_file_path,
                codec=codec
            )
        except Exception as error:
            colored_print(Fore.RED, f"Error: {error}")
            return

def create_video_clip(
        background_clip_path: str,
        final_clip_duration: float,
        dimensions: tuple[int, int],
        text_clips: list[mpy.TextClip],
        background_clip_speed: float=1.0,
        x_offset: int=0,
        y_offset: int=0,
        text_duration: float=None,
        shadow_clip: mpy.ColorClip=None
    ) -> mpy.CompositeVideoClip:
    """
    Creates a video clip
    """

    background_clip = mpy.VideoFileClip(background_clip_path).speedx(background_clip_speed)
    x_offset = random.randint(0, max(0, (x_offset + background_clip.w - dimensions[0]) % (background_clip.w - dimensions[0])))
    y_offset = random.randint(0, max(0, (y_offset + background_clip.h - dimensions[1]) % (background_clip.h - dimensions[1])))
    background_clip = background_clip.set_duration(
        final_clip_duration
    ).crop(
        x1=x_offset,
        y1=y_offset,
        x2=x_offset + dimensions[0],
        y2=y_offset + dimensions[1]
    )
    text_duration = text_duration if text_duration is not None else final_clip_duration
    clips = [
        background_clip,
        shadow_clip,
        *text_clips
    ] if shadow_clip is not None else [
        background_clip,
        *text_clips
    ]
    final_clip = mpy.CompositeVideoClip(
        clips,
        use_bgclip=True
    ).set_duration(
        final_clip_duration
    )
    return final_clip

def create_shadow_clip(
        size: tuple[int, int],
        color: tuple[int, int, int],
        duration: float,
        opacity: float=0.7
    ) -> mpy.ColorClip:
    """
    Creates a shadow clip
    """

    shadow_clip = mpy.ColorClip(
        size=size,
        color=color,
        duration=duration
    ).set_opacity(
        opacity
    )
    return shadow_clip

def create_text_clip(
        text: str,
        size: tuple,
        color: str, # "rgb(int, int, int)"
        fontsize: int,
        font: str,
        duration: float,
        position: tuple[str or float, str or float],
        bg_color: str="transparent",
        method: str="label",
        fade_duration: float=0.5
    ) -> mpy.TextClip:
    """
    Creates a text clip
    """

    text_clip = mpy.TextClip(
        txt=text,
        size=size,
        color=color,
        bg_color=bg_color,
        fontsize=fontsize,
        font=font,
        method=method
    ).set_position(
        position,
        relative=True
    ).set_duration(
        duration
    ).crossfadein(
        fade_duration
    ).crossfadeout(
        fade_duration
    )
    return text_clip

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
                time = lines[i].split("\t")[1]
                type = lines[i].split("\t")[4]
                if type == "Subclip":
                    i += 1
                    time2 = lines[i].split("\t")[1]
                    output_file.write(f"{time2},{time}\n")
                else:
                    output_file.write(time)
                    if (i + 1) < len(lines):
                        output_file.write("\n")
                i += 1
    colored_print(Fore.GREEN, f"Successfully created '{timestamps_txt_file_path}'")

if __name__ == "__main__":
    main()