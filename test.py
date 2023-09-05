import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from datetime import datetime
from enum import Enum
from pyquran import quran

def colored_print(color: str, text: str):
    """
    Prints text in color

    Args:
        color (str): Colorama color
        text (str): Text to print
    """
    print(f"{color}{text}{Style.RESET_ALL}")

class TikTok:
    class MODES(Enum):
        DARK = 1
        LIGHT = 2
    
    def __init__(
            self,
            timestamps_csv_file_path: str,
            shadow_opacity: float,
            text_fade_duration: float,
            mode: MODES = MODES.DARK,
            chapter: int = None,
            start_verse: int = None,
            end_verse: int = None
        ):
        self.timestamps_csv_file_path = timestamps_csv_file_path
        self.timestamps_txt_file_path = self.timestamps_csv_file_path.replace("Markers.csv", "timestamps.txt")
        if chapter < 1 or chapter > 114:
            colored_print(Fore.RED, "Chapter must be between 1 and 114")
            return
        self.chapter = chapter
        if end_verse < start_verse:
            colored_print(Fore.RED, "End verse must be greater than or equal to start verse")
            return
        self.start_verse = start_verse
        self.end_verse = end_verse
        self.chapter_text_file_path = "chapter_text.txt"
        self.chapter_translation_file_path = "chapter_translation.txt"
        self.shadow_opacity = shadow_opacity
        self.text_fade_duration = text_fade_duration
        self.mode = mode
        if self.mode == TikTok.MODES.DARK:
            self.shadow_color = (0, 0, 0)
            self.verse_text_color = "rgb(255, 255, 255)"
            self.verse_translation_color = "rgb(255, 255, 255)"
        elif self.mode == TikTok.MODES.LIGHT:
            self.shadow_color = (255, 255, 255)
            self.verse_text_color = "rgb(0, 0, 0)"
            self.verse_translation_color = "rgb(0, 0, 0)"

    def create_video(self):
        try:
            self.create_timestamps_txt_file()
        except FileNotFoundError:
            colored_print(Fore.RED, "timestamps.csv file not found")
            return

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
            for i in range(len(chapter_text_lines)):
                verse_text = chapter_text_lines[i - 1].strip()
                verse_translation = chapter_translation_lines[i - 1].strip()
                audio_start = timestamps_lines[i - 1].strip().split(",")[0]
                audio_end = timestamps_lines[i].strip().split(",")[0]
                try:
                    text_end = timestamps_lines[i].strip().split(",")[1]
                except IndexError:
                    text_end = None
                video_duration = self.get_time_difference_seconds(audio_start, audio_end)
                text_duration = self.get_time_difference_seconds(audio_start, text_end) if text_end is not None else None

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

if __name__ == "__main__":
    tiktok = TikTok(
        timestamps_csv_file_path="joe.csv",
        shadow_opacity=0.5,
        text_fade_duration=0.5,
        mode=TikTok.MODES.DARK
    )
    tiktok.create_video()