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

def colored_print(color: str, text: str):
    """
    Prints text in color

    Args:
        color (str): Colorama color
        text (str): Text to print
    """
    print(f"{color}{text}{Style.RESET_ALL}")

def get_time_difference_seconds(time1, time2):
        """
        Calculate the time difference between two time strings in the format "MM:SS.SSS"

        Args:
            time1 (str): The first time string
            time2 (str): The second time string

        Returns:
            float: The time difference in seconds
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

def create_notification(title, message):
        """
        Create a notification with the given parameters.

        Args:
            title (str): The title of the notification.
            message (str): The message of the notification.
        """
        notification.notify(
            title=title,
            message=message,
            app_name="Python",
            timeout=1
        )

def get_video_duration_seconds(video_path):
        """
        Get the duration of a video in seconds.

        Args:
            video_path (str): The path to the video file.

        Returns:
            float: The duration of the video in seconds.
        """
        video = cv2.VideoCapture(video_path)
        duration_seconds = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
        return duration_seconds

class TikTok:
    class MODES(Enum):
        DARK = 1
        LIGHT = 2
        MEDIUMSEAGREEN = 3
        CORNFLOWERBLUE = 4
        VIOLET = 5
        WHEAT = 6
        IVORY = 7

    class ACCOUNTS(Enum):
        QURAN_2_LISTEN = 1 # crazyshocklight@hotmail.com
        QURAN_LOVE77 = 2 # crazyshocklight2@gmail.com
        QURANIC_TIKTOKS = 3 # crazyshocky@hotmail.com

    DIMENSIONS = (576, 1024)
    
    def __init__(
            self,
            account: ACCOUNTS,
            timestamps_csv_file_path: str,
            audio_file_path: str,
            output_file_path: str,
            chapter_text_file_path: str = "chapter_text.txt",
            chapter_translation_file_path: str = "chapter_translation.txt",
            background_clips_directory_path: str = "Anime_Clips",
            single_frames: bool=False,
            background_clip_speed: float = 1.0,
            codec: str = "libx264",
            mode: MODES = MODES.DARK,
            shadow_opacity: float = 0.7,
            text_fade_duration: float = 0.5,
            start_line: int = None,
            end_line: int = None,
            chapter: int = None,
            start_verse: int = None,
            end_verse: int = None,
            duplicates_allowed: bool = False,
            hash_map: dict = None
        ):
        if account == ACCOUNTS.QURAN_2_LISTEN:
            self.ENGLISH_FONT = "Fonts/Butler_Regular.otf"
        elif account == ACCOUNTS.LOVE_QURAN77:
            self.ENGLISH_FONT = "Fonts/Lato-Semibold.ttf"
        elif account == ACCOUNTS.QURANIC_TIKTOKS:
            self.ENGLISH_FONT = "Fonts/Fontspring-DEMO-proximanovaexcn-regular.otf"
            self.session_id = "8877ca2daba37ca9acea9b798208e9b0"
        elif account == "":
            self.ENGLISH_FONT = "Fonts/Berlingske Serif Bold.otf"
        self.start_line = start_line
        self.end_line = end_line
        if chapter_text_file_path == "chapter_text.txt" and chapter_translation_file_path == "chapter_translation.txt":
            if chapter < 1 or chapter > 114:
                colored_print(Fore.RED, "Chapter must be between 1 and 114")
                return
            self.chapter = chapter
            if end_verse < start_verse:
                colored_print(Fore.RED, "End verse must be greater than or equal to start verse")
                return
        self.start_verse = start_verse
        self.end_verse = end_verse
        self.timestamps_csv_file_path = timestamps_csv_file_path
        self.timestamps_txt_file_path = self.timestamps_csv_file_path.replace("Markers.csv", "timestamps.txt")
        self.background_clips_directory_path = background_clips_directory_path
        self.single_frames = single_frames
        self.background_clip_speed = background_clip_speed
        self.audio_file_path = audio_file_path
        self.output_file_path = output_file_path
        self.codec = codec
        if self.codec == "rawvideo" or self.codec == "png":
            self.output_file_path = self.output_file_path = self.output_file_path + ".avi"
        elif self.codec == "libx264" or self.codec == "libx265" or self.codec == "mpeg4":
            self.output_file_path = self.output_file_path = self.output_file_path + ".mp4"
        self.chapter_text_file_path = chapter_text_file_path
        self.chapter_translation_file_path = chapter_translation_file_path
        self.mode = mode
        if self.mode == MODES.DARK:
            self.shadow_color = (0, 0, 0)
            self.verse_text_color = "rgb(255, 255, 255)"
            self.verse_translation_color = "rgb(255, 255, 255)"
        elif self.mode == MODES.LIGHT:
            self.shadow_color = (255, 255, 255)
            self.verse_text_color = "rgb(0, 0, 0)"
            self.verse_translation_color = "rgb(0, 0, 0)"
        elif self.mode == TikTok.MODES.MEDIUMSEAGREEN:
            self.shadow_color = (60,179,113)
            self.verse_text_color = "rgb(255, 255, 255)"
            self.verse_translation_color = "rgb(255, 255, 255)"
        elif self.mode == TikTok.MODES.CORNFLOWERBLUE:
            self.shadow_color = (100,149,237)
            self.verse_text_color = "rgb(255, 255, 255)"
            self.verse_translation_color = "rgb(255, 255, 255)"
        elif self.mode == TikTok.MODES.VIOLET:
            self.shadow_color = (238,130,238)
            self.verse_text_color = "rgb(255, 255, 255)"
            self.verse_translation_color = "rgb(255, 255, 255)"
        elif self.mode == TikTok.MODES.WHEAT:
            self.shadow_color = (245,222,179)
            self.verse_text_color = "rgb(255, 255, 255)"
            self.verse_translation_color = "rgb(255, 255, 255)"
        elif self.mode == TikTok.MODES.IVORY:
            self.shadow_color = (255,255,240)
            self.verse_text_color = "rgb(255, 255, 255)"
            self.verse_translation_color = "rgb(255, 255, 255)"
        self.shadow_opacity = shadow_opacity
        self.text_fade_duration = text_fade_duration
        self.duplicates_allowed = duplicates_allowed
        self.hash_map = hash_map

    def create_video(self):
        try:
            self.create_timestamps_txt_file()
        except FileNotFoundError:
            colored_print(Fore.RED, "timestamps.csv file not found")
            return

        if self.chapter_text_file_path == "chapter_text.txt" and self.chapter_translation_file_path == "chapter_translation.txt":
            with open(self.chapter_text_file_path, "w", encoding="utf-8") as chapter_text_file, \
            open(self.chapter_translation_file_path, "w", encoding="utf-8") as chapter_translation_file:
                verse_text = self.get_verse_text(self.start_verse)
                if verse_text is None:
                    return
                for current_verse in range(self.start_verse, self.end_verse + 1):
                    verse_text = self.get_verse_text(current_verse)
                    if verse_text is not None:
                        chapter_text_file.write(verse_text + "\n")
                        verse_translation = self.get_verse_translation(current_verse)
                        chapter_translation_file.write(verse_translation + "\n")
                    else:
                        break

            input("Appropriately edit text files now...")

        with open(self.chapter_text_file_path, "r", encoding="utf-8") as chapter_text_file, \
        open(self.chapter_translation_file_path, "r", encoding="utf-8") as chapter_translation_file, \
        open(self.timestamps_txt_file_path, "r", encoding="utf-8") as timestamps_file:
            chapter_text_lines = chapter_text_file.readlines()
            chapter_translation_lines = chapter_translation_file.readlines()
            timestamps_lines = timestamps_file.readlines()
            used_background_clips = []
            video_clips = []
            if self.start_line is not None:
                start = self.start_line
            else:
                start = 1
            if self.end_line is not None:
                end = self.end_line + 1
            else:
                end = len(chapter_text_lines) + 1
            loop_range = range(start, end)
            for i in loop_range:
                verse_text = chapter_text_lines[i - 1].strip()
                verse_translation = chapter_translation_lines[i - 1].strip()
                audio_start = timestamps_lines[i - 1].strip().split(",")[0]
                audio_end = timestamps_lines[i].strip().split(",")[0]
                try:
                    text_end = timestamps_lines[i].strip().split(",")[1]
                except IndexError:
                    text_end = None
                video_clip_duration = get_time_difference_seconds(audio_start, audio_end)
                text_duration = get_time_difference_seconds(audio_start, text_end) if text_end is not None else None
                if not self.single_frames:
                    if self.hash_map is None or (self.hash_map is not None and i not in self.hash_map):
                        all_background_clips = [clip for clip in os.listdir(self.background_clips_directory_path) if clip.endswith(".mp4")]
                        while True:
                            background_clip = random.choice(all_background_clips)
                            if self.hash_map is None or (self.hash_map is not None and background_clip not in self.hash_map.values()):
                                background_clip_path = os.path.join(self.background_clips_directory_path, background_clip)
                                background_clip_duration = get_video_duration_seconds(background_clip_path)
                                if background_clip_duration / self.background_clip_speed >= video_clip_duration:
                                    if self.duplicates_allowed or (not self.duplicates_allowed and background_clip not in used_background_clips):
                                        used_background_clips.append(background_clip)
                                        break
                    else:
                        background_clip_name = self.hash_map[i]
                        background_clip_path = os.path.join(self.background_clips_directory_path, background_clip_name)
                        background_clip_duration = get_video_duration_seconds(background_clip_path)
                        if background_clip_duration < video_clip_duration:
                            colored_print(Fore.RED, f"Background clip duration is less than video clip duration for clip {i}")
                            return
                        elif background_clip_name not in used_background_clips:
                            used_background_clips.append(background_clip_name)
                        del self.hash_map[i]
                else:
                    all_background_clips = [clip for clip in os.listdir(self.background_clips_directory_path) if clip.endswith(".mp4")]
                    background_clip = random.choice(all_background_clips)
                    background_clip_path = os.path.join(self.background_clips_directory_path, background_clip)
                    video_clip = mpy.VideoFileClip(background_clip_path)

                    # Get the total number of frames
                    total_frames = int(video_clip.fps * video_clip.duration)

                    # Generate a random frame number
                    random_frame_number = random.randint(1, total_frames)

                    # Seek to the random frame and capture it as an image
                    background_clip_path = video_clip.get_frame(random_frame_number / video_clip.fps)
                colored_print(Fore.GREEN, f"Creating clip {i}...")
                video_clip = self.create_video_clip(
                    background_clip_path=background_clip_path,
                    background_clip_duration=video_clip_duration,
                    text_duration=text_duration,
                    verse_text=verse_text,
                    verse_translation=verse_translation,
                    single_frame=self.single_frames
                )
                video_clips.append(video_clip)
            final_video_start = timestamps_lines[start - 1].strip().split(",")[0]
            final_video_end = timestamps_lines[end - 1].strip().split(",")[0]
            final_video_duration = get_time_difference_seconds(final_video_start, final_video_end)
            final_video = mpy.concatenate_videoclips(
                clips=video_clips,
                method="chain"
            ).set_audio(
                mpy.AudioFileClip(self.audio_file_path).set_start(final_video_start).subclip(final_video_start, final_video_end)
            ).set_duration(
                final_video_duration - .03
            )
            colored_print(Fore.GREEN, "Creating final video...")
            if not self.single_frames:
                try:
                    final_video.write_videofile(
                        self.output_file_path,
                        codec=self.codec,
                        fps=24,
                    )
                except Exception as error:
                    colored_print(Fore.RED, f"Error: {error}")
                    return
            else:
                try:
                    final_video.write_videofile(
                        self.output_file_path,
                        codec=self.codec,
                        fps=60,
                    )
                except Exception as error:
                    colored_print(Fore.RED, f"Error: {error}")
                    return
            # 'libx264' (default codec for file extension .mp4) makes well-compressed videos (quality tunable using 'bitrate').
            # 'mpeg4' (other codec for extension .mp4) can be an alternative to 'libx264', and produces higher quality videos by default.
            # 'rawvideo' (use file extension .avi) will produce a video of perfect quality, of possibly very huge size.
            # png (use file extension .avi) will produce a video of perfect quality, of smaller size than with rawvideo.
            # 'libvorbis' (use file extension .ogv) is a nice video format, which is completely free/ open source. However not everyone has the codecs installed by default on their machine.
            # 'libvpx' (use file extension .webm) is tiny a video format well indicated for web videos (with HTML5). Open source.

            create_notification(
                title="TikTok",
                message="Video successfully created!"
            )

    def create_video_clip(self, background_clip_path, background_clip_duration, text_duration, verse_text, verse_translation, x_offset=0, y_offset=0, single_frame=False):
        if not single_frame:
            video_clip = mpy.VideoFileClip(
                background_clip_path
            ).speedx(
                self.background_clip_speed
            ).set_duration(
                background_clip_duration
            )
        else:
            video_clip = mpy.ImageClip(
                background_clip_path
            ).set_duration(
                background_clip_duration
            ).set_fps(
                60
            )

            video_clip = Zoom(
                video_clip,
                mode='in',
                position='center',
                speed=1.1
            )

        x_offset = random.randint(0, max(0, video_clip.w - self.DIMENSIONS[0])) if x_offset == 0 else x_offset
        y_offset = random.randint(0, max(0, video_clip.h - self.DIMENSIONS[1])) if y_offset == 0 else y_offset
        
        video_clip = video_clip.crop(
            x1=x_offset,
            y1=y_offset,
            x2=x_offset + self.DIMENSIONS[0],
            y2=y_offset + self.DIMENSIONS[1]
        )
        shadow_clip = mpy.ColorClip(
            size=video_clip.size,
            color=self.shadow_color,
            duration=video_clip.duration
        ).set_opacity(
            self.shadow_opacity
        )

        video_with_shadow = mpy.CompositeVideoClip(
            [
                video_clip,
                shadow_clip
            ], 
            use_bgclip=True
        )

        text_duration = background_clip_duration if text_duration is None else text_duration

        verse_text_clip = mpy.TextClip(
            txt=verse_text,
            size=video_clip.size,
            color=self.verse_text_color,
            bg_color="transparent",
            fontsize=45,
            font=ARABIC_FONT
        ).set_position(
            (0, -.05), relative=True
        ).set_duration(
            text_duration
        ).crossfadein(
            self.text_fade_duration
        ).crossfadeout(
            self.text_fade_duration
        )

        verse_translation_clip = mpy.TextClip(
            txt=verse_translation,
            size=(video_clip.size[0] * .6, None),
            color=self.verse_translation_color,
            bg_color="transparent",
            fontsize=18,
            font=self.ENGLISH_FONT,
            method="caption"
        ).set_position(
            ("center", .49), relative=True
        ).set_duration(
            text_duration
        ).crossfadein(
            self.text_fade_duration
        ).crossfadeout(
            self.text_fade_duration
        )

        final_clip = mpy.CompositeVideoClip(
            [
                video_with_shadow,
                verse_text_clip,
                verse_translation_clip
            ], 
            use_bgclip=True
        ).set_duration(
            background_clip_duration
        )

        return final_clip

    def create_timestamps_txt_file(self):
        """
        Creates text file with timestamps from csv file with timestamps
        """
        with open(self.timestamps_csv_file_path, "r", encoding="utf-8") as csv_file:
            lines = csv_file.readlines()[1:]
            with open(self.timestamps_txt_file_path, "w", encoding="utf-8") as output_file:
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
        colored_print(Fore.GREEN, f"Successfully created '{self.timestamps_txt_file_path}'")

    def get_verse_text(self, verse):
        """
        Gets the text of a verse from the Quran

        Args:
            verse (int): Verse number

        Returns:
            str: Verse text or None if verse not found
        """
        verse_text = quran.get_verse(self.chapter, verse, with_tashkeel=True)
        if verse_text is None or verse_text == "":
            colored_print(Fore.RED, f"Verse {verse} not found")
            return None
        return verse_text

    def get_verse_translation(self, verse):
        """
        Gets the translation of a verse from the Quran

        Args:
            verse (int): Verse number

        Returns:
            str: Verse translation or None if verse not found
        """
        try:
            response = requests.get(f"https://api.quran.com/api/v4/quran/translations/20?verse_key={self.chapter}:{verse}")
            translation = response.json()["translations"][0]["text"]
            soup = BeautifulSoup(translation, "html.parser")
            clean_text = soup.get_text()
            return clean_text
        except Exception as error:
            colored_print(Fore.RED, f"Error: {error}")
            return None

class Quran:
    def get_verse_text(self, chapter, verse):
        verse_text = quran.get_verse(chapter, verse, with_tashkeel=True)
        if verse_text is None or verse_text == "":
            colored_print(Fore.RED, f"Verse {verse} not found")
            return None
        return verse_text
    
    def get_verse_translation(self, chapter, verse):
        try:
            response = requests.get(f"https://api.quran.com/api/v4/quran/translations/20?verse_key={chapter}:{verse}")
            translation = response.json()["translations"][0]["text"]
            soup = BeautifulSoup(translation, "html.parser")
            clean_text = soup.get_text()
            return clean_text
        except Exception as error:
            colored_print(Fore.RED, f"Error: {error}")
            return None

class MODES(Enum):
    DARK = 1
    LIGHT = 2

class ACCOUNTS(Enum):
    QURAN_2_LISTEN = 1 # crazyshocklight@hotmail.com
    LOVE_QURAN77 = 2 # crazyshocklight2@gmail.com
    QURANIC_TIKTOKS = 3 # crazyshocky@hotmail.com

def Video(
        directory_path: str,
        output_file_path: str,
        audio_file_path: str,
        account: ACCOUNTS= ACCOUNTS.QURAN_2_LISTEN,
        chapter_text_file_path: str="chapter_text.txt",
        chapter_translation_file_path: str="chapter_translation.txt",
        start: int=1,
        end: int=None,
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
    ):
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
        if end is None:
            end = len(chapter_text_lines) + 1
        loop_range = range(start, end)
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
                Text_Clip(
                    text=verse_text,
                    size=dimensions,
                    color=verse_text_color,
                    fontsize=45,
                    font=ARABIC_FONT,
                    position=(0, -.05),
                    duration=text_duration
                ),
                Text_Clip(
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
            shadow_clip = Shadow_Clip(
                size=dimensions,
                color=shadow_color,
                duration=final_clip_duration,
                opacity=shadow_opacity
            )
            video_clip = Video_Clip(
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
        final_video_start = timestamps_lines[start - 1].strip().split(",")[0]
        final_video_end = timestamps_lines[end - 1].strip().split(",")[0]
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

def create_timestamps_txt_file(timestamps_csv_file_path):
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

def Video_Clip(
        background_clip_path: str,
        final_clip_duration: float,
        dimensions: tuple[int, int],
        text_clips: list[mpy.TextClip],
        background_clip_speed: float=1.0,
        x_offset: int=0,
        y_offset: int=0,
        text_duration: float=None,
        shadow_clip: mpy.ColorClip=None
    ):
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
        text_clips
    ] if shadow_clip is not None else [
        background_clip,
        text_clips
    ]
    final_clip = mpy.CompositeVideoClip(
        clips,
        use_bgclip=True
    ).set_duration(
        final_clip_duration
    )
    return final_clip

def Shadow_Clip(
        size: tuple[int, int],
        color: tuple[int, int, int],
        duration: float,
        opacity: float=0.7
    ):
    shadow_clip = mpy.ColorClip(
        size=size,
        color=color,
        duration=duration
    ).set_opacity(
        opacity
    )
    return shadow_clip

def Text_Clip(
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
    ):
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

class TikToks():
    def __init__(
            self, 
            account: ACCOUNTS, 
            mode: MODES=MODES.DARK,
            background_clips_directory_path: str="Anime_Clips", 
            background_clip_speed: float=1.0, 
            single_frames: bool=False, 
        ):
        self.account = account
        self.mode = mode
        self.background_clips_directory_path = background_clips_directory_path
        self.background_clip_speed = background_clip_speed
        self.single_frames = single_frames

    def abdul_rahman_mossad_maryam_93_98(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\Markers.csv",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\audio.mp3",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 19 - Maryam\Videos\{self.account}_93-98_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
        ).create_video()

    def abdul_rahman_mossad_al_ankabut_54_62(self):
        TikTok(
            account=self.account, 
            timestamps_csv_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\Markers.csv", 
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\audio.mp3", 
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\Videos\{self.account}_54-62_{uuid.uuid4()}", 
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_text.txt", 
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_translation.txt", 
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
        ).create_video()

    def abdul_rahman_mossad_al_ankabut_56_57(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\Markers.csv",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\audio.mp3",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\Videos\{self.account}_54-62_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 29 - Al-'Ankabut\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
            start_line=6,
            end_line=9,
        ).create_video()

    def abdul_rahman_mossd_al_muzzammil_14_18(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\Markers.csv",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\audio.mp3",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\Videos\{self.account}_14-18_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
        ).create_video()

    def abdul_rahman_mossd_al_muzzammil_14_15(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\Markers.csv",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\audio.mp3",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\Videos\{self.account}_14-18_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 73 - Al-Muzzammil\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
            start_line=1,
            end_line=3,
        ).create_video()

    def abdul_rahman_mossd_al_ghashiyah_10_26(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\Markers.csv",
            audio_file_path=r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\audio.mp3",
            output_file_path=rf"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\Videos\{self.account}_10-26_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 88 - Al-Ghashiyah\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
        ).create_video()

    def fatih_seferagic_ayatul_kursi_255(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Fatih Seferagic - 2 - Al-Baqarah\Markers.csv",
            audio_file_path=r"Surahs\Fatih Seferagic - 2 - Al-Baqarah\audio.mp3",
            output_file_path=rf"Surahs\Fatih Seferagic - 2 - Al-Baqarah\Videos\{self.account}_255_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Fatih Seferagic - 2 - Al-Baqarah\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Fatih Seferagic - 2 - Al-Baqarah\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
        ).create_video()

    def fatih_seferagic_al_hujurat_10(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\Markers.csv",
            audio_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\audio.mp3",
            output_file_path=rf"Surahs\Fatih Seferagic - 49 - Al-Hujurat\Videos\{self.account}_10_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Fatih Seferagic - 49 - Al-Hujurat\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
        ).create_video()

    def fatih_seferagic_al_hashr_21_24(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Fatih Seferagic - 59 - Al-Hashr\Markers.csv",
            audio_file_path=r"Surahs\Fatih Seferagic - 59 - Al-Hashr\audio.mp3",
            output_file_path=rf"Surahs\Fatih Seferagic - 59 - Al-Hashr\Videos\{self.account}_21-24_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Fatih Seferagic - 59 - Al-Hashr\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Fatih Seferagic - 59 - Al-Hashr\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            mode=self.mode,
        ).create_video()

    def salim_bahanan_al_fatihah_2_7(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\Markers.csv",
            audio_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\audio.mp3",
            output_file_path=rf"Surahs\Salim Bahanan - 1 - Al-Fatihah\Videos\{self.account}_2-7_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            mode=self.mode,
        ).create_video()

    def salim_bahanan_ad_duhaa_1_11(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\Markers.csv",
            audio_file_path=r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\audio.mp3",
            output_file_path=rf"Surahs\Salim Bahanan - 93 - Ad-Duhaa\Videos\{self.account}_1-11_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Salim Bahanan - 93 - Ad-Duhaa\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            mode=self.mode,
        ).create_video()

    def salim_bahanan_al_qariah_1_11(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\Markers.csv",
            audio_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\audio.mp3",
            output_file_path=rf"Surahs\Salim Bahanan - 101 - Al-Qari'ah\Videos\{self.account}_1-11_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            mode=self.mode,
        ).create_video()

    def unknown_al_ankabut_56_58(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\Markers.csv",
            audio_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\audio.mp3",
            output_file_path=rf"Surahs\Unknown - 29 - Al-'Ankabut\Videos\{self.account}_56-58_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            mode=self.mode,
        ).create_video()

    def unknown_al_ankabut_56_57(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\Markers.csv",
            audio_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\audio.mp3",
            output_file_path=rf"Surahs\Unknown - 29 - Al-'Ankabut\Videos\{self.account}_56-58_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Unknown - 29 - Al-'Ankabut\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
            start_line=1,
            end_line=4,
        ).create_video()
    
    def unknown_al_furqan_72_75(self):
        TikTok(
            account=self.account,
            timestamps_csv_file_path=r"Surahs\Unknown - 25 - Al-Furqan\Markers.csv",
            audio_file_path=r"Surahs\Unknown - 25 - Al-Furqan\audio.mp3",
            output_file_path=rf"Surahs\Unknown - 25 - Al-Furqan\Videos\{self.account}_72-75_{uuid.uuid4()}",
            chapter_text_file_path=r"Surahs\Unknown - 25 - Al-Furqan\chapter_text.txt",
            chapter_translation_file_path=r"Surahs\Unknown - 25 - Al-Furqan\chapter_translation.txt",
            background_clips_directory_path=self.background_clips_directory_path,
            background_clip_speed=self.background_clip_speed,
            single_frames=self.single_frames,
            mode=self.mode,
        ).create_video()

import numpy as np
def Zoom(clip,mode='in',position='center',speed=1):
    fps = clip.fps
    duration = clip.duration
    total_frames = int(duration*fps)
    def main(getframe,t):
        frame = getframe(t)
        h,w = frame.shape[:2]
        i = t*fps
        if mode == 'out':
            i = total_frames-i
        zoom = 1+(i*((0.1*speed)/total_frames))
        positions = {
            'center':[(w-(w*zoom))/2,(h-(h*zoom))/2],
            'left':[0,(h-(h*zoom))/2],
            'right':[(w-(w*zoom)),(h-(h*zoom))/2],
            'top':[(w-(w*zoom))/2,0],
            'topleft':[0,0],
            'topright':[(w-(w*zoom)),0],
            'bottom':[(w-(w*zoom))/2,(h-(h*zoom))],
            'bottomleft':[0,(h-(h*zoom))],
            'bottomright':[(w-(w*zoom)),(h-(h*zoom))]
        }
        tx,ty = positions[position]
        M = np.array([[zoom,0,tx], [0,zoom,ty]])
        frame = cv2.warpAffine(frame,M,(w,h))
        return frame
    return clip.fl(main)

if __name__ == "__main__":
    # tiktok = TikTok(
    #     account=TikTok.ACCOUNTS.QURAN_2_LISTEN,
    #     timestamps_csv_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\Markers.csv",
    #     audio_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\audio.mp3",
    #     output_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\Videos\quran_2_listen-3",
    #     chapter_text_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_text.txt",
    #     chapter_translation_file_path=r"Surahs\Salim Bahanan - 1 - Al-Fatihah\chapter_translation.txt",
    #     hash_map={
    #         3: "Hyouka - E22(42)..mp4",
    #         10: "Weathering With You (145).mp4",
    #         1: "Weathering With You (328).mp4",
    #         11: "Violet Evergarden - NCOP1 (10).mp4",
    #         16: "Kimi No Nawa (274).mp4"

    #     }
    # )
    # tiktok.create_video()

    # joe = input("Would you like to upload the video to TikTok? (y/n): ")
    # if joe.lower() == "y":
    #     title = input("Enter a title for the video: ")
    #     tags = input("Enter tags for the video (separated by commas): ").split(",")
    #     uploadVideo(
    #         session_id=tiktok.session_id,
    #         video_path=tiktok.output_file_path,
    #         title=title,
    #         tags=tags,
    #         verbose=True
    #     )
    # else:
    #     colored_print(Fore.RED, "Video not uploaded")
    # video = Video(
    #     output_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\Videos\1",
    #     timestamps_txt_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\timestamps.txt",
    #     chapter_text_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\chapter_text.txt",
    #     chapter_translation_file_path=r"Surahs\Salim Bahanan - 101 - Al-Qari'ah\chapter_translation.txt",
    # ).create_video()
    
    # TikToks(TikTok.ACCOUNTS.QURAN_2_LISTEN).abdul_rahman_mossad_maryam_93_98.create_video()
    # TikToks(TikTok.ACCOUNTS.QURAN_2_LISTEN).salim_bahanan_al_fatihah_2_7()
    # Video(
    #     directory_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam",
    #     output_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\Videos\1",
    #     audio_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\audio.mp3",
    #     chapter_text_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_text.txt",
    #     chapter_translation_file_path=r"Surahs\Abdul Rahman Mossad - 19 - Maryam\chapter_translation.txt"
    # )
    # TikToks(
    #     ACCOUNTS.QURAN_2_LISTEN,
    #     background_clip_speed=1
    # ).abdul_rahman_mossad_al_ankabut_56_57()
    # TikToks(
    #     account=ACCOUNTS.LOVE_QURAN77,
    #     background_clips_directory_path="Real_Clips",
    # ).abdul_rahman_mossd_al_ghashiyah_10_26()
    # TikToks(
    #     account=ACCOUNTS.QURANIC_TIKTOKS,
    #     background_clips_directory_path="Real_Clips",
    # ).unknown_al_ankabut_56_57()
    TikToks(
        account=ACCOUNTS.QURAN_2_LISTEN
    ).unknown_al_furqan_72_75()