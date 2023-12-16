import os
import re

from datetime import datetime
from enums import Account, AudioSettings, CSVColumnNames, TextClipInfo, TimeModifiers, VideoMode, VideoSettings
from rework import create_video, fetch_chapter_name


def main():
    tiktok = TikTokInfo(Account.QURAN_2_LISTEN)
    tiktok.create_tiktok(r"Surahs\Ahmed Wael - As-Saffat (37.91-93)", (91, 93), video_map={})


class TikTokInfo:
    def __init__(
        self,
        account: Account,
        video_settings: VideoSettings = VideoSettings(
            allow_duplicate_background_clips=False,
            allow_mirrored_background_clips=True,
            background_clips_speed=1.0,
            video_dimensions=(576, 1024),
            video_mode=VideoMode.VIDEO,
        ),
        background_clips_directories_list: list[str] = None,
    ):
        self.account = account
        self.video_settings = video_settings
        self.background_clips_directories_list = background_clips_directories_list

    def create_tiktok(
        self,
        audio_directory_path: str,
        output_video_verse_range: tuple[int, int],
        time_modifiers: TimeModifiers = TimeModifiers(time_modifier=-0.2, end_time_modifier=0.0),
        video_map: dict[str, list[list[str, float, int, str]]] = None,
        output_mp4_file_path: str = None,
    ):
        for file in os.listdir(audio_directory_path):
            if file.endswith(".mp3"):
                audio_mp3_file_path = os.path.join(audio_directory_path, file)
                break

        pattern = r"\d+"
        match = re.findall(pattern, audio_directory_path)

        chapter_number = int(match[0])
        start_to_end_timestamp_verse_range = (int(match[1]), int(match[-1]))

        audio_settings = AudioSettings(
            audio_mp3_file_path=audio_mp3_file_path,
            chapter_number=chapter_number,
            start_to_end_timestamp_verse_range=start_to_end_timestamp_verse_range,
        )

        chapter_name = fetch_chapter_name(chapter_number)
        reciter_name = audio_directory_path.split(" - ")[0].split("\\")[-1]
        language_abbreviation = self.account.value.language.value.abbreviation
        start_verse, end_verse = output_video_verse_range
        output_mp4_file_name = f"{chapter_name} ({chapter_number}.{start_verse}-{end_verse}) - {reciter_name} {self.account.name.lower()} {language_abbreviation} {datetime.now().strftime('%d-%m-%Y %H.%M.%S')}"

        chapter_csv_file_path = os.path.join(audio_directory_path, "chapter.csv")
        timestamps_csv_file_path = os.path.join(audio_directory_path, "Markers.csv")

        csv_column_names = CSVColumnNames(verse_number="verse", verse_text="ar", timestamp="timestamps")

        verse_text_text_clip = TextClipInfo(
            text_background_color="transparent",
            text_fade_duration=0.5,
            text_font_size=44,
            text_method="caption",
            text_position=("center", 0.41),
            text_size=(self.video_settings.video_dimensions[0] * 0.9, None),
        )

        verse_translation_text_clip = TextClipInfo(
            text_background_color="transparent",
            text_fade_duration=0.5,
            text_font_size=20,
            text_method="caption",
            text_position=("center", 0.49),
            text_size=(self.video_settings.video_dimensions[0] * 0.6, None),
        )

        verse_number_text_clip = TextClipInfo(
            text_background_color="transparent",
            text_fade_duration=0.5,
            text_font_size=20,
            text_method="caption",
            text_position=("center", 0.75),
            text_size=(self.video_settings.video_dimensions[0] * 0.6, None),
        )

        reciter_name = None if reciter_name.casefold() == "unknown" else reciter_name
        reciter_name_text_clip = TextClipInfo(
            text_background_color="transparent",
            text_fade_duration=0.5,
            text_font_size=20,
            text_method="caption",
            text_position=("center", 0.20),
            text_size=(self.video_settings.video_dimensions[0] * 0.6, None),
        )

        create_video(
            account=self.account,
            audio_settings=audio_settings,
            csv_column_names=csv_column_names,
            time_modifiers=time_modifiers,
            video_settings=self.video_settings,
            output_video_verse_range=output_video_verse_range,
            output_mp4_file_name=output_mp4_file_name,
            chapter_csv_file_path=chapter_csv_file_path,
            timestamps_csv_file_path=timestamps_csv_file_path,
            verse_text_text_clip=verse_text_text_clip,
            verse_translation_text_clip=verse_translation_text_clip,
            verse_number_text_clip=verse_number_text_clip,
            reciter_name=reciter_name,
            reciter_name_text_clip=reciter_name_text_clip,
            video_map=video_map,
            background_clips_directories_list=self.background_clips_directories_list,
            output_mp4_file_path=output_mp4_file_path,
        )


if __name__ == "__main__":
    main()
