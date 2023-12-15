import os

from config import VERSE_TEXT_FONT_FILE_PATH
from datetime import datetime
from enums import Account
from rework import create_video, fetch_chapter_name


def main():
    # TODO: Add verse_range alongside start_verse and end_verse so you can choose which of the verses to include in the video
    tiktok = TikTokInfo(Account.QURAN_2_LISTEN)
    tiktok.create_tiktok(r"E:\GitHub\quran\Surahs\Abdul Rahman Mossad - Al-'Adiyat (100.1-11) - Copy", 1, 11, (1, 2))


class TikTokInfo:
    def __init__(
        self,
        account: Account,
        video_dimensions: tuple[int, int] = (576, 1024),
        allow_mirrored_background_clips: bool = True,
        allow_duplicate_background_clips: bool = False,
        background_clips_directories_list: list[str] = None,
    ):
        self.account = account
        self.video_dimensions = video_dimensions
        self.allow_mirrored_background_clips = allow_mirrored_background_clips
        self.allow_duplicate_background_clips = allow_duplicate_background_clips
        self.background_clips_directories_list = background_clips_directories_list

    def create_tiktok(
        self,
        audio_directory_path: str,
        start_verse: int,
        end_verse: int,
        verse_range: tuple[int, int],
        time_modifier: float = -0.2,
        end_time_modifier: float = 0.0,
        video_map: dict[str, list[list[str, float, int, str]]] = None,
        background_clips_speed: float = 1.0,
        video_mode: bool = True,
        start_line: int = None,
        end_line: int = None,
        background_video: str = None,
        background_video_horizontal_offset: int = None,
        background_video_vertical_offset: int = None,
        output_mp4_file_path: str = None,
        start_time_modifier: float = None,
    ):
        for file in os.listdir(audio_directory_path):
            if file.endswith(".mp3"):
                audio_mp3_file_path = os.path.join(audio_directory_path, file)
                break
        chapter_number = int(audio_directory_path.split(" (")[1].split(".")[0])
        chapter_name = fetch_chapter_name(chapter_number)
        reciter_name = audio_directory_path.split(" - ")[0].split("\\")[-1]
        language_abbreviation = self.account.value.language.value.abbreviation
        output_mp4_file_name = f"{chapter_name} ({chapter_number}.{start_verse}-{end_verse}) - {reciter_name} {self.account.name.lower()} {language_abbreviation} {datetime.now().strftime('%d-%m-%Y %H.%M.%S')}"

        chapter_csv_file_path = os.path.join(audio_directory_path, "chapter.csv")
        timestamps_csv_file_path = os.path.join(audio_directory_path, "Markers.csv")

        verse_number_column_name = "verse"
        verse_text_column_name = "ar"
        timestamp_column_name = "timestamps"

        verse_text_background_color = "transparent"
        verse_text_fade_duration = 0.5
        verse_text_font_file_path = VERSE_TEXT_FONT_FILE_PATH
        verse_text_font_size = 44
        verse_text_method = "caption"
        verse_text_position = ("center", 0.41)
        verse_text_size = (self.video_dimensions[0] * 0.9, None)

        verse_translation_background_color = "transparent"
        verse_translation_fade_duration = 0.5
        verse_translation_font_size = 20
        verse_translation_method = "caption"
        verse_translation_position = ("center", 0.49)
        verse_translation_size = (self.video_dimensions[0] * 0.6, None)

        verse_number_background_color = "transparent"
        verse_number_fade_duration = 0.5
        verse_number_font_file_path = self.account.value.verse_translation_font_file_path
        verse_number_font_size = 20
        verse_number_method = "caption"
        verse_number_position = ("center", 0.75)
        verse_number_size = (self.video_dimensions[0] * 0.6, None)

        reciter_name_background_color = "transparent"
        reciter_name_fade_duration = 0.5
        reciter_name_font_file_path = self.account.value.verse_translation_font_file_path
        reciter_name_font_size = 20
        reciter_name_method = "caption"
        reciter_name_position = ("center", 0.20)
        reciter_name_size = (self.video_dimensions[0] * 0.6, None)

        create_video(
            account=self.account,
            audio_mp3_file_path=audio_mp3_file_path,
            chapter_number=chapter_number,
            start_verse=start_verse,
            end_verse=end_verse,
            verse_range=verse_range,
            time_modifier=time_modifier,
            end_time_modifier=end_time_modifier,
            output_mp4_file_name=output_mp4_file_name,
            chapter_csv_file_path=chapter_csv_file_path,
            timestamps_csv_file_path=timestamps_csv_file_path,
            verse_number_column_name=verse_number_column_name,
            verse_text_column_name=verse_text_column_name,
            timestamp_column_name=timestamp_column_name,
            background_clips_speed=background_clips_speed,
            video_dimensions=self.video_dimensions,
            video_mode=video_mode,
            allow_mirrored_background_clips=self.allow_mirrored_background_clips,
            allow_duplicate_background_clips=self.allow_duplicate_background_clips,
            verse_text_background_color=verse_text_background_color,
            verse_text_fade_duration=verse_text_fade_duration,
            verse_text_font_file_path=verse_text_font_file_path,
            verse_text_font_size=verse_text_font_size,
            verse_text_method=verse_text_method,
            verse_text_position=verse_text_position,
            verse_text_size=verse_text_size,
            verse_translation_background_color=verse_translation_background_color,
            verse_translation_fade_duration=verse_translation_fade_duration,
            verse_translation_font_size=verse_translation_font_size,
            verse_translation_method=verse_translation_method,
            verse_translation_position=verse_translation_position,
            verse_translation_size=verse_translation_size,
            verse_number_background_color=verse_number_background_color,
            verse_number_fade_duration=verse_number_fade_duration,
            verse_number_font_size=verse_number_font_size,
            verse_number_method=verse_number_method,
            verse_number_position=verse_number_position,
            verse_number_size=verse_number_size,
            start_line=start_line,
            end_line=end_line,
            background_clips_directories_list=self.background_clips_directories_list,
            video_map=video_map,
            background_video=background_video,
            background_video_horizontal_offset=background_video_horizontal_offset,
            background_video_vertical_offset=background_video_vertical_offset,
            output_mp4_file_path=output_mp4_file_path,
            start_time_modifier=start_time_modifier,
            verse_number_font_file_path=verse_number_font_file_path,
            reciter_name=reciter_name,
            reciter_name_background_color=reciter_name_background_color,
            reciter_name_fade_duration=reciter_name_fade_duration,
            reciter_name_font_file_path=reciter_name_font_file_path,
            reciter_name_font_size=reciter_name_font_size,
            reciter_name_method=reciter_name_method,
            reciter_name_position=reciter_name_position,
            reciter_name_size=reciter_name_size,
        )


if __name__ == "__main__":
    main()
