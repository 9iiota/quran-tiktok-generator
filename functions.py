import contextlib
import csv
import moviepy.editor as mpy
import os
import random
import re
import requests

from colorama import Fore, Style
from compact_json import EolStyle, Formatter
from datetime import datetime, timedelta
from classes import (
    Account,
    AudioSettings,
    CSVColumnNames,
    TextClipInfo,
    TimeModifiers,
    VideoModes,
    VideoSettings,
    OptionalVideoSettings,
    Languages,
)
from fuzzywuzzy import fuzz
from pyquran import quran
from typing import Optional


def create_video(
    account: Account,
    audio_settings: AudioSettings,
    csv_column_names: CSVColumnNames,
    time_modifiers: TimeModifiers,
    video_settings: VideoSettings,
    output_video_verse_range: tuple[int, int],
    output_mp4_file_name: str,
    chapter_csv_file: str,
    timestamps_csv_file: str,
    optional_video_settings: Optional[OptionalVideoSettings] = OptionalVideoSettings(),
    verse_text_text_clip: Optional[TextClipInfo] = None,
    verse_translation_text_clip: Optional[TextClipInfo] = None,
    verse_number_text_clip: Optional[TextClipInfo] = None,
    reciter_name: Optional[str] = None,
    reciter_name_text_clip: Optional[TextClipInfo] = None,
    output_mp4_file: Optional[str] = None,
) -> None:
    """
    Create a video with the given parameters.

    Parameters
    ----------
    """

    if not isinstance(account, Account):
        account = account.value

    if not os.path.isfile(audio_settings.audio_mp3_file):
        raise FileNotFoundError(f"{audio_settings.audio_mp3_file} is not a file.")

    audio_mp3_file_directory_path = os.path.dirname(audio_settings.audio_mp3_file)

    if output_mp4_file:
        output_mp4_file = output_mp4_file.replace("\\", "/")

        try:
            output_directory_path = os.path.dirname(output_mp4_file)
        except Exception:
            raise NotADirectoryError(f"{output_directory_path} is not a valid directory.")
    else:
        output_directory_path = os.path.join(audio_mp3_file_directory_path, "Videos")
        output_mp4_file = os.path.join(output_directory_path, f"{output_mp4_file_name}.mp4")

    if not os.path.isdir(output_directory_path):
        os.mkdir(output_directory_path)

    chapter_csv_file = chapter_csv_file.replace("\\", "/")

    if not os.path.isfile(chapter_csv_file):
        column_names = [csv_column_names.verse_number, csv_column_names.verse_text]
        if create_csv_file(chapter_csv_file, column_names):
            colored_print(Fore.GREEN, f"Created {chapter_csv_file} with column names {column_names}.")

            if append_verse_texts_to_csv_file(
                chapter_csv_file,
                audio_settings.chapter_number,
                audio_settings.audio_verse_range,
                csv_column_names.verse_number,
                csv_column_names.verse_text,
            ):
                colored_print(Fore.GREEN, f"Added verse texts to {chapter_csv_file}.")

    if append_verse_translations_to_csv_file(
        chapter_csv_file,
        account.language,
        audio_settings.chapter_number,
        audio_settings.audio_verse_range,
        csv_column_names.timestamp,
    ):
        colored_print(Fore.GREEN, f"Added verse translations to {chapter_csv_file}.")

        return

    if not os.path.isfile(timestamps_csv_file):
        raise FileNotFoundError(f"{timestamps_csv_file} is not a valid path.")
    else:
        if update_csv_file_timestamps(chapter_csv_file, timestamps_csv_file, csv_column_names.timestamp):
            colored_print(Fore.GREEN, f"Added timestamps to {chapter_csv_file}.")

            if update_csv_file_verse_numbers(
                chapter_csv_file,
                audio_settings.chapter_number,
                audio_settings.audio_verse_range,
                csv_column_names.verse_number,
                csv_column_names.verse_text,
                csv_column_names.timestamp,
            ):
                colored_print(Fore.GREEN, f"Added verse numbers to {chapter_csv_file}.")

    language_abbreviation = account.language.value.abbreviation

    # TODO: A clip should be able to be created without language abbreviation column
    chapter_csv_lines = select_columns_from_csv_file(
        chapter_csv_file,
        [
            csv_column_names.verse_number,
            csv_column_names.verse_text,
            language_abbreviation,
            csv_column_names.timestamp,
        ],
    )

    start_line, end_line = get_loop_range(chapter_csv_lines, audio_settings.chapter_number, output_video_verse_range)

    video_width, video_height = video_settings.video_dimensions

    video_start_timestamp = chapter_csv_lines[start_line - 1][3].strip().split(",")[0]
    if time_modifiers.start_time_modifier:
        video_start = offset_timestamp(video_start_timestamp, time_modifiers.start_time_modifier)
    else:
        video_start = offset_timestamp(video_start_timestamp, time_modifiers.time_modifier)

    video_end_timestamp = chapter_csv_lines[end_line - 1][3].strip().split(",")[0]
    video_end = offset_timestamp(video_end_timestamp, time_modifiers.end_time_modifier)

    video_duration = get_time_difference_seconds(video_start, video_end)

    audio = mpy.AudioFileClip(audio_settings.audio_mp3_file).subclip(video_start, video_end)

    # TODO: Unsure if it is better to have absolute or relative paths
    # if video_map:
    #     video_map = convert_video_map_paths_to_absolute_paths(video_map)

    all_background_clips_paths = get_relative_mp4_paths(account.background_clips_directories)
    target_aspect_ratio = video_width / video_height
    text_clips_array = []
    used_background_clips_paths = []
    video_clips = []
    video_map_output = {}

    if optional_video_settings.video_map:
        optional_video_settings.video_map = {
            int(key): value for key, value in optional_video_settings.video_map.items()
        }

    loop_range = range(start_line, end_line)
    for line in loop_range:
        clip_index = line - start_line + 1
        current_line = chapter_csv_lines[line - 1]

        # TODO: A line should be able to exist without verse_translation
        verse_number, verse_text, verse_translation, timestamp = current_line

        colored_print(Fore.MAGENTA, f"Creating clip {clip_index}...")

        next_line = chapter_csv_lines[line]
        next_timestamp = next_line[3]

        if line == start_line:
            audio_start = video_start
        else:
            audio_start = offset_timestamp(strip_timestamp(timestamp)[0], time_modifiers.time_modifier)

        if line == end_line - 1:
            audio_end = video_end
        else:
            audio_end = offset_timestamp(strip_timestamp(next_timestamp)[0], time_modifiers.time_modifier)

        video_clip_duration = get_time_difference_seconds(audio_start, audio_end)

        try:
            text_end = offset_timestamp(strip_timestamp(next_timestamp)[1], time_modifiers.time_modifier)
            text_duration = get_time_difference_seconds(audio_start, text_end)
        except IndexError:
            text_duration = video_clip_duration

        if not optional_video_settings.single_background_video:
            total_background_clips_duration = 0
            video_clip_background_clip_paths = []

            if video_settings.video_mode == VideoModes.VIDEO:
                video_map_index = line - start_line + 1

                if optional_video_settings.video_map and video_map_index in optional_video_settings.video_map.keys():
                    background_clips_count = len(optional_video_settings.video_map[video_map_index])

                    for i in range(background_clips_count):
                        background_clip_info = optional_video_settings.video_map[video_map_index][i]

                        background_clip_path = background_clip_info[0]
                        background_clip = mpy.VideoFileClip(background_clip_path).speedx(
                            video_settings.background_clips_speed
                        )

                        background_clip_duration = calculate_clip_duration(
                            background_clip_path, video_settings.background_clips_speed
                        )

                        max_time_offset = calculate_clip_max_time_offset(
                            background_clip_duration, video_settings.minimal_background_clip_duration
                        )
                        background_clip_time_offset = get_background_clip_time_offset(
                            background_clip_info, max_time_offset
                        )

                        try:
                            if background_clip_time_offset != background_clip_info[1]:
                                colored_print(
                                    Fore.YELLOW,
                                    f"Verse {video_map_index} background clip {i + 1} time offset is invalid, using ({background_clip_time_offset}) instead",
                                )
                        except IndexError:
                            pass

                        max_horizontal_offset = calculate_clip_max_horizontal_offset(background_clip.w, video_width)

                        if max_horizontal_offset < 0:
                            raise ValueError(
                                f"Verse {video_map_index} Background clip {i + 1} width ({background_clip.w}) is less than video width ({video_width})"
                            )

                        background_clip_horizontal_offset = get_background_clip_horizontal_offset(
                            background_clip_info, max_horizontal_offset
                        )

                        try:
                            if background_clip_horizontal_offset != background_clip_info[2]:
                                colored_print(
                                    Fore.YELLOW,
                                    f"Verse {video_map_index} background clip {i + 1} horizontal offset is invalid, using ({background_clip_horizontal_offset}) instead",
                                )
                        except IndexError:
                            pass

                        background_clip_mirrored = get_background_clip_mirrored(
                            background_clip_info, video_settings.allow_mirrored_background_clips
                        )

                        try:
                            if background_clip_mirrored != background_clip_info[3]:
                                colored_print(
                                    Fore.YELLOW,
                                    f"Verse {video_map_index} background clip {i + 1} mirrored is invalid, using ({background_clip_mirrored}) instead",
                                )
                        except IndexError:
                            pass

                        adjusted_background_clip_duration = background_clip_duration - background_clip_time_offset

                        video_clip_leftover_duration = video_clip_duration - total_background_clips_duration
                        if validate_background_clip_duration(
                            adjusted_background_clip_duration,
                            video_settings.minimal_background_clip_duration,
                            video_clip_leftover_duration,
                        ):
                            video_clip_background_clip_paths.append(
                                [
                                    background_clip_path,
                                    background_clip_time_offset,
                                    background_clip_horizontal_offset,
                                    background_clip_mirrored,
                                ]
                            )
                            used_background_clips_paths.append(background_clip_path)

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
                            i,
                            used_background_clips_paths,
                            video_clip_background_clip_paths,
                            video_map_index,
                        ) = get_valid_background_clips(
                            all_background_clips_paths,
                            video_settings.allow_duplicate_background_clips,
                            video_settings.allow_mirrored_background_clips,
                            video_settings.background_clips_speed,
                            video_settings.minimal_background_clip_duration,
                            total_background_clips_duration,
                            used_background_clips_paths,
                            video_clip_background_clip_paths,
                            video_clip_duration,
                            optional_video_settings.video_map,
                            video_map_index,
                            video_width,
                            i,
                        )
                else:
                    (
                        used_background_clips_paths,
                        video_clip_background_clip_paths,
                        video_map_index,
                    ) = get_valid_background_clips(
                        all_background_clips_paths,
                        video_settings.allow_duplicate_background_clips,
                        video_settings.allow_mirrored_background_clips,
                        video_settings.background_clips_speed,
                        video_settings.minimal_background_clip_duration,
                        total_background_clips_duration,
                        used_background_clips_paths,
                        video_clip_background_clip_paths,
                        video_clip_duration,
                        optional_video_settings.video_map,
                        video_map_index,
                        video_width,
                    )[
                        1:
                    ]

                video_map_output[video_map_index] = video_clip_background_clip_paths
            else:
                background_clip_path = get_random_path(all_background_clips_paths)
                background_clip = mpy.VideoFileClip(background_clip_path)
                background_clip_duration = calculate_clip_duration(
                    background_clip_path, video_settings.background_clips_speed
                )

                max_time_offset = calculate_clip_max_time_offset(
                    background_clip_duration, video_settings.minimal_background_clip_duration
                )
                background_clip_time_offset = get_random_time_offset(max_time_offset)

                max_horizontal_offset = calculate_clip_max_horizontal_offset(background_clip.w, video_width)

                if max_horizontal_offset < 0:
                    raise ValueError(
                        f"Background clip {background_clip_path} width ({background_clip.w}) is less than video width ({video_width})"
                    )

                background_clip_horizontal_offset = get_random_horizontal_offset(max_horizontal_offset)

                background_clip_mirrored = get_background_clip_mirrored(
                    background_clip_path, video_settings.allow_mirrored_background_clips
                )

                video_clip_background_clip_paths.append(
                    [
                        background_clip_path,
                        background_clip_time_offset,
                        background_clip_horizontal_offset,
                        background_clip_mirrored,
                    ]
                )

        # Append text clips
        text_clips = []

        if verse_text_text_clip:
            verse_text_color = account.mode.value.verse_text_color
            verse_text_clip = verse_text_text_clip.create_text_clip(
                color=verse_text_color,
                duration=text_duration,
                font=account.verse_text_font_file,
                text=verse_text,
            )
            text_clips.append(verse_text_clip)

        if verse_translation_text_clip:
            verse_translation_color = account.mode.value.verse_translation_color
            verse_translation_clip = verse_translation_text_clip.create_text_clip(
                color=verse_translation_color,
                duration=text_duration,
                font=account.verse_translation_font_file,
                text=verse_translation,
            )
            text_clips.append(verse_translation_clip)

        # Append verse number text clip if it is a new verse
        if verse_number_text_clip and verse_number != "":
            verse_number_color = account.mode.value.verse_number_color
            verse_number_clip = verse_number_text_clip.create_text_clip(
                color=verse_number_color,
                duration=text_duration,
                font=account.verse_number_font_file,
                text=verse_number,
            )
            text_clips.append(verse_number_clip)

        # Append reciter name text clip if it is the first clip
        if line == start_line and reciter_name and reciter_name_text_clip:
            reciter_name_color = account.mode.value.reciter_name_color
            reciter_name_clip = reciter_name_text_clip.create_text_clip(
                color=reciter_name_color,
                duration=text_duration,
                font=account.reciter_name_font_file,
                text=reciter_name,
            )
            text_clips.append(reciter_name_clip)

        if not optional_video_settings.single_background_video:
            # Create shadow clip to put overlay on the video clip
            shadow_color = account.mode.value.shadow_color
            shadow_opacity = account.mode.value.shadow_opacity
            shadow_clip = create_shadow_clip(
                size=video_settings.video_dimensions,
                color=shadow_color,
                duration=video_clip_duration,
                opacity=shadow_opacity,
            )

            colored_print(Fore.CYAN, f"Using background clip(s):")

            for background_clip_path in video_clip_background_clip_paths:
                colored_print(Fore.CYAN, f"- {background_clip_path[0]}")

            video_clip = create_video_clip(
                background_clips_paths=video_clip_background_clip_paths,
                background_clips_speed=video_settings.background_clips_speed,
                final_clip_duration=video_clip_duration,
                target_aspect_ratio=target_aspect_ratio,
                text_clips=text_clips,
                video_dimensions=video_settings.video_dimensions,
                video_mode=video_settings.video_mode,
                shadow_clip=shadow_clip,
                text_duration=text_duration,
            )
            video_clips.append(video_clip)

            colored_print(Fore.GREEN, f"Created clip {clip_index}")
        else:
            # Set text clip start times if using a single background video
            text_start_time = get_time_difference_seconds(audio_start, video_start)

            text_clips[0] = text_clips[0].set_start(text_start_time)
            text_clips[1] = text_clips[1].set_start(text_start_time)

            # Append verse number text clip
            if verse_number != "":
                text_clips[2] = text_clips[2].set_start(text_start_time)

            # Append reciter name text clip if it is the first clip
            if line == start_line and reciter_name:
                text_clips[-1] = text_clips[-1].set_start(text_start_time)

            text_clips_array.extend(text_clips)

    if not optional_video_settings.single_background_video:
        final_video = mpy.concatenate_videoclips(clips=video_clips, method="chain").set_audio(audio)
    else:
        background_clip = mpy.VideoFileClip(optional_video_settings.single_background_video).subclip(video_start)

        background_clip_width, background_clip_height = background_clip.size
        current_aspect_ratio = background_clip_width / background_clip_height

        if current_aspect_ratio > target_aspect_ratio:
            new_width = int(background_clip_height * target_aspect_ratio)

            if not optional_video_settings.single_background_video_horizontal_offset:
                background_video_horizontal_offset = (background_clip_width - new_width) // 2
            else:
                background_video_horizontal_offset = optional_video_settings.single_background_video_horizontal_offset

            background_clip = background_clip.crop(
                x1=background_video_horizontal_offset,
                x2=background_video_horizontal_offset + new_width,
            ).resize(video_settings.video_dimensions)
        else:
            new_height = int(background_clip_width / target_aspect_ratio)

            if not optional_video_settings.single_background_video_vertical_offset:
                background_video_vertical_offset = (background_clip_height - new_height) // 2
            else:
                background_video_vertical_offset = optional_video_settings.single_background_video_vertical_offset

            background_clip = background_clip.crop(
                y1=background_video_vertical_offset, y2=background_video_vertical_offset + new_height
            ).resize(video_settings.video_dimensions)

        shadow_clip = create_shadow_clip(
            color=account.mode.value.shadow_color,
            duration=background_clip.duration,
            opacity=account.mode.value.shadow_opacity,
            size=video_settings.video_dimensions,
        )

        video = mpy.CompositeVideoClip([background_clip, shadow_clip])
        final_video = mpy.CompositeVideoClip([video, *text_clips_array], use_bgclip=True).set_audio(audio)

        video_map_output = optional_video_settings.single_background_video

    colored_print(Fore.GREEN, "Creating final video...")

    json_output_file_path = output_mp4_file.replace(".mp4", ".json")

    formatter = Formatter()
    formatter.use_tab_to_indent = True
    formatter.nested_bracket_padding = False
    formatter.max_inline_length = 300
    formatter.max_inline_complexity = 1
    formatter.json_eol_style = EolStyle.LF
    formatter.dont_justify_numbers = True

    formatter.dump(
        video_map_output,
        output_file=json_output_file_path,
        newline_at_eof=True,
    )

    try:
        if optional_video_settings.single_background_video:
            final_video.write_videofile(
                filename=output_mp4_file,
                fps=video.fps,
            )
        elif video_settings.video_mode == VideoModes.VIDEO:
            final_video.write_videofile(
                codec="libx264",
                filename=output_mp4_file,
            )
        elif video_settings.video_mode == VideoModes.IMAGE:
            final_video.write_videofile(
                codec="libx264",
                filename=output_mp4_file,
                fps=60,
            )

        colored_print(Fore.GREEN, "Created final video")
    except Exception as error:
        raise Exception(f"Failed to create final video: {error}") from error


def create_csv_file(chapter_csv_file_path: str, column_names: list[str]) -> bool:
    """
    Creates a CSV file.

    Parameters
    ----------
    chapter_csv_file_path : str
        The path of the CSV file to create.
    field_names : list[str]
        The names of the columns of the CSV file.

    Returns
    -------
    bool
        True if the CSV file was created successfully, False otherwise.
    """

    with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
        csv_dict_writer = csv.DictWriter(chapter_csv_file, fieldnames=column_names)
        csv_dict_writer.writeheader()

    return True


def append_verse_texts_to_csv_file(
    chapter_csv_file_path: str,
    chapter_number: int,
    entire_audio_verse_range: tuple[int, int],
    verse_number_column_name: str,
    verse_text_column_name: str,
) -> bool:
    """
    Appends the verse texts of a chapter from the Qur'an to a CSV file.

    Parameters
    ----------
    chapter_csv_file_path : str
        The path of the CSV file to append the verse texts to.
    chapter_number : int
        The chapter number of the chapter to get the verse texts of.
    start_verse : int
        The verse number of the first verse to get.
    verse_number_column_name : str
        The name of the column containing the verse numbers.
    verse_text_column_name : str
        The name of the column containing the verse texts.
    end_verse : int
        The verse number of the last verse to get.

    Returns
    -------
    bool
        True if the verse texts were appended successfully, False otherwise.
    """

    with open(chapter_csv_file_path, "r", encoding="utf-8") as chapter_csv_file:
        csv_dict_reader = csv.DictReader(chapter_csv_file)
        field_names = csv_dict_reader.fieldnames

        verse_column_index = field_names.index(verse_number_column_name)
        verse_text_column_index = field_names.index(verse_text_column_name)

        data = []
        start_verse, end_verse = entire_audio_verse_range
        verse_texts = get_chapter_text(chapter_number)[start_verse - 1 : end_verse]

        for i in range(len(verse_texts)):
            verse_number = f"{chapter_number}:{start_verse + i}"
            verse_text = verse_texts[i]

            if verse_text is not None:
                data.append(
                    {field_names[verse_column_index]: verse_number, field_names[verse_text_column_index]: verse_text}
                )

        with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
            csv_dict_writer = csv.DictWriter(chapter_csv_file, fieldnames=field_names)
            csv_dict_writer.writeheader()
            csv_dict_writer.writerows(data)

    if remove_empty_rows_from_csv_file(chapter_csv_file_path):
        return True


def append_verse_translations_to_csv_file(
    chapter_csv_file_path: str,
    language: Languages,
    chapter_number: int,
    entire_audio_verse_range: tuple[int, int],
    timestamp_column_name: str,
) -> bool:
    """
    Appends the verse translations of a chapter from the Qur'an to a CSV file.

    Parameters
    ----------
    chapter_csv_file_path : str
        The path of the CSV file to append the verse translations to.
    language : Language
        The language of the translation.
    chapter_number : int
        The chapter number of the chapter to get the verse translations of.
    start_verse : int
        The verse number of the first verse to get.
    end_verse : int
        The verse number of the last verse to get.

    Returns
    -------
    bool
        True if the verse translations were appended successfully, False otherwise.
    """

    with open(chapter_csv_file_path, "r", encoding="utf-8") as chapter_csv_file:
        csv_dict_reader = csv.DictReader(chapter_csv_file)
        field_names = csv_dict_reader.fieldnames

        if language.value.abbreviation not in field_names:
            data = list(csv_dict_reader)

            if timestamp_column_name in field_names:
                timestamp_column_index = field_names.index(timestamp_column_name)
                field_names.insert(timestamp_column_index, language.value.abbreviation)
            else:
                field_names.append(language.value.abbreviation)

            start_verse, end_verse = entire_audio_verse_range
            verse_translations = fetch_chapter_translation(chapter_number, language)[start_verse - 1 : end_verse]

            for i, verse_translation in enumerate(verse_translations):
                data[i][language.value.abbreviation] = verse_translation

            with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
                csv_dict_writer = csv.DictWriter(chapter_csv_file, fieldnames=field_names)
                csv_dict_writer.writeheader()
                csv_dict_writer.writerows(data)

            if remove_empty_rows_from_csv_file(chapter_csv_file_path):
                return True


def remove_empty_rows_from_csv_file(csv_file_path: str) -> bool:
    """
    Removes empty rows from a CSV file.

    Parameters
    ----------
    csv_file_path : str
        The path of the CSV file to remove the empty rows from.

    Returns
    -------
    bool
        True if the empty rows were removed successfully, False otherwise.
    """

    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = [row for row in csv_reader if any(cell.strip() != "" for cell in row)]

    with open(csv_file_path, mode="w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)

    return True


def select_columns_from_csv_file(csv_file_path: str, columns_to_select: list[str]) -> list[list[str]]:
    """
    Selects columns from a CSV file.

    Parameters
    ----------
    csv_file_path : str
        The path of the CSV file to select the columns from.
    columns_to_select : list[str]
        The names of the columns to select.

    Returns
    -------
    list[list[str]]
        A list of lists containing the selected columns.
    """

    with open(csv_file_path, "r", encoding="utf-8") as csv_file:
        csv_dict_reader = csv.DictReader(csv_file)

        selected_data = []

        for row in csv_dict_reader:
            selected_row = [row[column] for column in columns_to_select]
            selected_data.append(selected_row)

    return selected_data


def update_csv_file_timestamps(
    chapter_csv_file_path: str, timestamps_csv_file_path: str, timestamp_column_name: str
) -> bool:
    """
    Updates the timestamps of a CSV file containing the verses of a chapter from the Qur'an.

    Parameters
    ----------
    chapter_csv_file_path : str
        The path of the CSV file to update the timestamps of.
    timestamps_csv_file_path : str
        The path of the CSV file containing the timestamps.
    timestamp_column_name : str
        The name of the column containing the timestamps.

    Returns
    -------
    bool
        True if the timestamps were updated successfully, False otherwise.
    """

    with open(timestamps_csv_file_path, "r", encoding="utf-8") as timestamps_csv_file:
        lines = timestamps_csv_file.readlines()[1:]
        timestamps = []

        i = 0
        while i < len(lines):
            marker_time = lines[i].split("\t")[1]
            marker_type = lines[i].split("\t")[4]

            if marker_type == "Subclip":
                i += 1

                second_marker_time = lines[i].split("\t")[1]
                timestamps.append([second_marker_time, marker_time])
            else:
                timestamps.append(marker_time)

            i += 1

        sorted_nested_timestamps = sort_nested_timestamps(timestamps)
        sorted_timestamps = sorted(sorted_nested_timestamps, key=convert_timestamp_to_seconds)

        with open(chapter_csv_file_path, "r", encoding="utf-8") as chapter_csv_file:
            csv_dict_reader = csv.DictReader(chapter_csv_file)
            field_names = csv_dict_reader.fieldnames

            if timestamp_column_name not in field_names:
                field_names.append(timestamp_column_name)

            data = list(csv_dict_reader)

            while len(data) < len(sorted_timestamps):
                data.append({timestamp_column_name: sorted_timestamps[len(data)].strip()})

            for line in range(len(sorted_timestamps)):
                if isinstance(sorted_timestamps[line], list):
                    for i in range(len(sorted_timestamps[line])):
                        sorted_timestamps[line][i] = sorted_timestamps[line][i].strip()
                    data[line][timestamp_column_name] = ",".join(sorted_timestamps[line])
                else:
                    data[line][timestamp_column_name] = sorted_timestamps[line].strip()

            with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
                writer = csv.DictWriter(chapter_csv_file, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(data)

    if remove_empty_rows_from_csv_file(chapter_csv_file_path):
        return True


def update_csv_file_verse_numbers(
    chapter_csv_file_path: str,
    chapter_number: int,
    entire_audio_verse_range: tuple[int, int],
    verse_number_column_name: str,
    verse_text_column_name: str,
    timestamp_column_name: str,
) -> bool:
    """
    Updates the verse numbers of a CSV file containing the verses of a chapter from the Qur'an.

    Parameters
    ----------
    chapter_csv_file_path : str
        The path of the CSV file to update the verse numbers of.
    chapter_number : int
        The chapter number of the chapter to get the verse numbers of.
    start_verse : int
        The verse number of the first verse to get.
    verse_number_column_name : str
        The name of the column containing the verse numbers.
    verse_text_column_name : str
        The name of the column containing the verse texts.
    timestamp_column_name : str
        The name of the column containing the timestamps.
    end_verse : int
        The verse number of the last verse to get.

    Returns
    -------
    bool
        True if the verse numbers were updated successfully, False otherwise.
    """

    with open(chapter_csv_file_path, "r", encoding="utf-8") as chapter_csv_file:
        csv_dict_reader = csv.DictReader(chapter_csv_file)
        field_names = csv_dict_reader.fieldnames

        data = []
        existing_verses = set()
        start_verse, end_verse = entire_audio_verse_range
        verse_texts = get_chapter_text(chapter_number)[start_verse - 1 : end_verse]
        indexed_verse_texts = list(zip(range(start_verse, end_verse + 1), verse_texts))

        for row in csv_dict_reader:
            if row[verse_text_column_name] != "" or row[timestamp_column_name] == "":
                best_ratio, best_verse_number = (0, None)
                csv_text = row[verse_text_column_name]

                for tuple in indexed_verse_texts:
                    letter_difference = len(tuple[1]) - len(csv_text)

                    if letter_difference >= 0:
                        word_start_indexes = [0] + [
                            space_index + 1 for space_index, char in enumerate(tuple[1]) if char == " "
                        ]

                        for word_start_index in word_start_indexes:
                            match = tuple[1][word_start_index : len(csv_text) + word_start_index]
                            ratio = fuzz.ratio(csv_text, match)

                            if ratio > best_ratio:
                                best_ratio, best_verse_number = (ratio, tuple[0])

                            if ratio == 100:
                                break

                verse = f"{chapter_number}:{best_verse_number}"
                if verse not in existing_verses:
                    row[verse_number_column_name] = verse
                    existing_verses.add(verse)

                    with contextlib.suppress(IndexError):
                        if indexed_verse_texts[0][0] != best_verse_number:
                            indexed_verse_texts.pop(0)
                else:
                    row[verse_number_column_name] = ""

            data.append(row)
        with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
            csv_dict_writer = csv.DictWriter(chapter_csv_file, fieldnames=field_names)
            csv_dict_writer.writeheader()
            csv_dict_writer.writerows(data)

    if remove_empty_rows_from_csv_file(chapter_csv_file_path):
        return True


def get_loop_range(
    chapter_csv_lines: list[list[str]], chapter_number: int, verse_range: tuple[int, int]
) -> tuple[int, int]:
    """
    Get the loop range for the TikTok.

    Parameters
    ----------
    chapter_csv_lines : list[list[str]]
        The chapter CSV lines.
    chapter_number : int
        The chapter number.
    start_verse : int
        The start verse.
    end_verse : int
        The end verse.

    Returns
    -------
    tuple[int, int]
        The loop range.
    """

    verse_range_start, verse_range_end = verse_range
    verse_numbers = [row[0] for row in chapter_csv_lines]

    start_line = verse_numbers.index(f"{chapter_number}:{verse_range_start}") + 1

    end_line = verse_numbers.index(f"{chapter_number}:{verse_range_end}") + 1

    while end_line + 1 < len(verse_numbers) and verse_numbers[end_line + 1] == "":
        end_line += 1

    return (start_line, end_line + 1)


def get_time_difference_seconds(time1: str, time2: str) -> float:
    """
    Calculate the time difference between two time strings in the format "MM:SS.SSS"

    Parameters
    ----------
    time1 : str
        The first time string.
    time2 : str
        The second time string.

    Returns
    -------
    float
        The time difference in seconds.
    """

    time_format = "%M:%S.%f"

    time1 = datetime.strptime(time1, time_format)
    time2 = datetime.strptime(time2, time_format)

    time_difference = abs(time2 - time1)

    return time_difference.total_seconds()


def offset_timestamp(timestamp: str, time_offset_seconds: float) -> str:
    """
    Offset the timestamp by the given time offset.

    Parameters
    ----------
    timestamp : str
        The timestamp.
    time_offset_seconds : float
        The time offset in seconds.

    Returns
    -------
    str
        The offset timestamp.
    """

    seconds = convert_timestamp_to_seconds(timestamp)
    original_timedelta = timedelta(seconds=seconds)

    new_timedelta = max(original_timedelta + timedelta(seconds=time_offset_seconds), timedelta(0))

    return "{:02d}:{:02d}.{:03d}".format(
        new_timedelta.seconds // 60,
        new_timedelta.seconds % 60,
        new_timedelta.microseconds // 1000,
    )


def fetch_chapter_name(chapter_number: int) -> str:
    """
    Gets the name of a chapter from the Qur'an

    Parameters
    ----------
    chapter_number : int
        The chapter number of the chapter to get the name of.

    Returns
    -------
    str
        The name of the chapter.
    """

    url = "https://api.quran.com/api/v4/chapters"

    try:
        response = requests.get(url)
    except Exception as error:
        raise Exception("Failed to fetch chapters.") from error

    chapter_names = [chapter["name_simple"] for chapter in response.json()["chapters"]]

    return chapter_names[chapter_number - 1]


def fetch_chapter_translation(chapter_number: int, language: Languages) -> list[str]:
    """
    Gets the translation of a chapter from the Quran

    Parameters
    ----------
    chapter_number : int
        The chapter number of the chapter to get the translation of.
    language : Language
        The language of the translation.

    Returns
    -------
    list[str]
        A list of strings containing the translation of the chapter.
    """

    translation_id = language.value.translation_id
    url = f"https://api.quran.com/api/v4/quran/translations/{translation_id}?chapter_number={chapter_number}"

    try:
        response = requests.get(url)
    except Exception as error:
        raise Exception(
            f"Failed to fetch translation for chapter {chapter_number} in {language.value['abbreviation']}."
        ) from error

    return [
        re.sub(
            "ḥ",
            "h",
            re.sub("ā", "a", re.sub(r"<.*?>*<.*?>", "", translation["text"])),
        )
        for translation in response.json()["translations"]
    ]


def fetch_chapter_verse_count(chapter_number: int) -> int:
    """
    Gets the number of verses in a chapter from the Qur'an

    Parameters
    ----------
    chapter_number : int
        The chapter number of the chapter to get the number of verses of.

    Returns
    -------
    int
        The number of verses in the chapter.
    """

    url = f"https://api.quran.com/api/v4/chapters/{chapter_number}"

    try:
        response = requests.get(url)
    except Exception as error:
        raise Exception(f"Failed to fetch chapter {chapter_number}.") from error

    return response.json()["chapter"]["verses_count"]


def get_chapter_text(chapter_number: int) -> list[str]:
    """
    Gets the text of a chapter from the Qur'an

    Parameters
    ----------
    chapter_number : int
        The chapter number of the chapter to get the text of.

    Returns
    -------
    list[str]
        A list of strings containing the text of the chapter.
    """

    return quran.get_sura(chapter_number, with_tashkeel=True)


def colored_print(color: str, text: str) -> None:
    """
    Prints text in color.
    """

    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{current_time}] {text}{Style.RESET_ALL}")


def convert_video_map_paths_to_absolute_paths(
    video_map: dict[str, list[list[str, float or int, int, str]]]
) -> dict[str, list[list[str, float or int, int, str]]]:
    """
    Converts the paths in a video map to absolute paths.

    Parameters
    ----------
    video_map : dict[str, list[list[str, float or int, int, str]]]
        The video map to update.

    Returns
    -------
    dict[str, list[list[str, float, int, str]]]
        The updated video map.
    """

    updated_video_map = {}

    for key, value in video_map.items():
        absolute_paths = []

        for video_info in value:
            absolute_path = os.path.abspath(video_info[0])
            absolute_paths.append([absolute_path] + video_info[1:])

        updated_video_map[int(key)] = absolute_paths

    return updated_video_map


def dictionary_contains_value(dictionary: dict, value: str) -> bool:
    """
    Checks if a dictionary contains a value.

    Parameters
    ----------
    dictionary : dict
        The dictionary to check.
    value : str
        The value to check.

    Returns
    -------
    bool
        Whether or not the dictionary contains the value.
    """

    all_strings = list(
        filter(
            lambda value: isinstance(value[0], str), [value[0] for values in dictionary.values() for value in values]
        )
    )

    return value in all_strings


def get_absolute_mp4_paths(
    folder_paths: list[str],
) -> list[str]:
    """
    Gets the absolute paths of all mp4 files in a list of folders.

    Parameters
    ----------
    folder_paths : list[str]
        The paths to the folders.

    Returns
    -------
    list[str]
        The absolute paths of all mp4 files in the folders.
    """

    return [
        os.path.abspath(os.path.join(folder_path, file))
        for folder_path in folder_paths
        for file in os.listdir(folder_path)
        if file.endswith(".mp4")
    ]


def get_relative_mp4_paths(
    folder_paths: list[str],
) -> list[str]:
    """
    Gets the relative paths of all mp4 files in a list of folders.

    Parameters
    ----------
    folder_paths : list[str]
        The paths to the folders.

    Returns
    -------
    list[str]
        The relative paths of all mp4 files in the folders.
    """

    return [
        os.path.join(folder_path, file)
        for folder_path in folder_paths
        for file in os.listdir(folder_path)
        if file.endswith(".mp4")
    ]


def calculate_clip_duration(clip_path: str, clip_speed: float) -> float:
    """
    Gets the duration of a clip.

    Parameters
    ----------
    clip_path : str
        The path to the clip.
    clip_speed : float
        The speed of the clip.

    Returns
    -------
    float
        The duration of the clip.
    """

    return get_video_duration_seconds(clip_path) / clip_speed


def get_background_clip_horizontal_offset(
    background_clip_info: list[str, float or int, int, str], max_horizontal_offset: int
) -> int:
    """
    Gets a horizontal offset for a clip.

    Parameters
    ----------
    background_clip_info : list[str, float or int, int, str]
        The clip info.
    max_horizontal_offset : int
        The max horizontal offset.

    Returns
    -------
    int
        The horizontal offset.
    """

    if (
        len(background_clip_info) >= 3
        and isinstance(background_clip_info[2], int)
        and background_clip_info[2] <= max_horizontal_offset
    ):
        return background_clip_info[2]
    else:
        return get_random_horizontal_offset(max_horizontal_offset)


def calculate_clip_max_horizontal_offset(clip_width: int, video_width: int) -> int:
    """
    Gets the max horizontal offset for a clip

    Parameters
    ----------
    clip_width : int
        The width of the clip.
    video_width : int
        The width of the video.

    Returns
    -------
    int
        The max horizontal offset for the clip.
    """

    return clip_width - video_width


def calculate_clip_max_time_offset(clip_duration: float, minimal_clip_duration: float) -> float:
    """
    Gets the max time offset for a clip

    Parameters
    ----------
    clip_duration : float
        The duration of the clip.
    minimal_clip_duration : float
        The minimal duration of the clip.

    Returns
    -------
    float
        The max time offset for the clip.
    """

    return max(clip_duration - minimal_clip_duration, 0)


def get_background_clip_mirrored(
    background_clip_info: list[str, float or int, int, str], allow_mirrored_clips: bool
) -> str:
    """
    Gets a mirrored value for a clip.

    Parameters
    ----------
    clip_info : list[str, float or int, int, str]
        The clip info.
    allow_mirrored_clips : bool
        Whether or not mirrored clips are allowed.

    Returns
    -------
    str
        The mirrored value.
    """

    if (
        len(background_clip_info) >= 4
        and isinstance(background_clip_info[3], (str, bool))
        and background_clip_info[3] in ["True", "False", True, False]
    ):
        return str(background_clip_info[3])
    elif allow_mirrored_clips:
        return str(random.choice([True, False]))
    else:
        return "False"


def get_random_horizontal_offset(max_horizontal_offset: int) -> int:
    """
    Returns a random horizontal offset

    Parameters
    ----------
    max_horizontal_offset : int
        The max horizontal offset.

    Returns
    -------
    int
        The random horizontal offset.
    """

    return random.randint(0, max_horizontal_offset)


def get_random_path(all_paths: list[str]) -> str:
    """
    Returns a random path.

    Parameters
    ----------
    all_paths : list[str]
        All paths.

    Returns
    -------
    str
        The random path.
    """

    return random.choice(all_paths)


def get_random_time_offset(max_time_offset: float) -> float:
    """
    Returns a random time offset rounded to 2 decimals.

    Parameters
    ----------
    max_time_offset : float
        The max time offset.
    divide_by : int or float
        The number to divide the max time offset by.

    Returns
    -------
    float
        The random time offset.
    """

    return round(random.uniform(0, max_time_offset), 2)


def convert_timestamp_to_seconds(timestamp: str or list[str]) -> float:
    """
    Gets the number of seconds from a timestamp.

    Parameters
    ----------
    timestamp : str or list[str]
        The timestamp to get the number of seconds from.

    Returns
    -------
    float
        The number of seconds from the timestamp.
    """

    if isinstance(timestamp, list):
        timestamp = timestamp[0]

    minutes, seconds = timestamp.split(":")
    seconds, milliseconds = seconds.split(".")

    return int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000


def get_background_clip_time_offset(
    background_clip_info: list[str, float or int, int, str], max_time_offset: float
) -> float:
    """
    Gets a time offset for a clip.

    Parameters
    ----------
    background_clip_info : list[str, float or int, int, str]
        The clip info.
    max_time_offset : float
        The max time offset.

    Returns
    -------
    float
        The time offset.
    """
    if (
        len(background_clip_info) >= 2
        and (isinstance(background_clip_info[1], (float, int)))
        and background_clip_info[1] <= max_time_offset
    ):
        return background_clip_info[1]
    else:
        return get_random_time_offset(max_time_offset)


def get_video_duration_seconds(mp4_file_path: str) -> float:
    """
    Gets the duration of a video in seconds.

    Parameters
    ----------
    mp4_file_path : str
        The path to the video.

    Returns
    -------
    float
        The duration of the video in seconds.
    """

    return mpy.VideoFileClip(mp4_file_path).duration


def sort_nested_timestamps(timestamps: list[str or list[str]]) -> list[str or list[str]]:
    """
    Sorts a list of timestamps in ascending order.

    Parameters
    ----------
    timestamps : list[str or list[str]]
        The timestamps to sort.

    Returns
    -------
    list[str or list[str]]
        The sorted timestamps.
    """

    for i, timestamp in enumerate(timestamps):
        if isinstance(timestamp, list):
            timestamps[i] = sorted(timestamp, key=convert_timestamp_to_seconds, reverse=True)

    return timestamps


def strip_timestamp(timestamp: str) -> str:
    """
    Gets a stripped timestamp.

    Parameters
    ----------
    timestamp : str
        The timestamp to strip.

    Returns
    -------
    str
        The stripped timestamp.
    """

    return timestamp.strip().split(",")


####


def get_valid_background_clips(
    all_background_clips_paths: list[str],
    allow_duplicate_background_clips: bool,
    allow_mirrored_background_clips: bool,
    background_clips_speed: float,
    minimal_background_clip_duration: float,
    total_background_clips_duration: float,
    used_background_clips_paths: list[str],
    video_clip_background_clip_paths: list[list[str, float or int, int, str]],
    video_clip_duration: float,
    video_map: dict[str, list[list[str, float or int, int, str]]],
    video_map_index: int,
    video_width: int,
    x: int = 0,
):
    """
    Gets valid background clips for a video clip.

    Parameters
    ----------


    Returns
    -------
    """

    while True:
        # Get new background clips until the total duration of the background clips is long enough for the video clip
        background_clip_path = get_random_path(all_background_clips_paths)

        if len(used_background_clips_paths) == len(all_background_clips_paths):
            allow_duplicate_background_clips = True

        if allow_duplicate_background_clips or (
            not allow_duplicate_background_clips
            and background_clip_path not in used_background_clips_paths
            and (
                (video_map is not None and not dictionary_contains_value(video_map, background_clip_path))
                or video_map is None
            )
        ):
            background_clip_duration = calculate_clip_duration(background_clip_path, background_clips_speed)

            max_time_offset = calculate_clip_max_time_offset(
                background_clip_duration, minimal_background_clip_duration
            )
            background_clip_time_offset = get_random_time_offset(max_time_offset)

            background_clip_leftover_duration = background_clip_duration - background_clip_time_offset

            # TO BE ADDED WHEN DURATION IN VIDEO MAPS IS IMPLEMENTED
            # # Get a random clip duration between the minimal clip duration and the leftover duration
            # adjusted_background_clip_duration = max(
            #     MINIMAL_CLIP_DURATION,
            #     random.uniform(MINIMAL_CLIP_DURATION, min(background_clip_leftover_duration, video_clip_duration)),
            # )

            adjusted_background_clip_duration = min(background_clip_leftover_duration, video_clip_duration)

            video_clip_leftover_duration = video_clip_duration - total_background_clips_duration
            if validate_background_clip_duration(
                adjusted_background_clip_duration, minimal_background_clip_duration, video_clip_leftover_duration
            ):
                background_clip = mpy.VideoFileClip(background_clip_path)

                max_horizontal_offset = calculate_clip_max_horizontal_offset(background_clip.w, video_width)

                if max_horizontal_offset < 0:
                    raise ValueError(
                        f"Verse {video_map_index} Background clip {x + 1} width ({background_clip.w}) is less than video width ({video_width})"
                    )

                background_clip_horizontal_offset = get_random_horizontal_offset(max_horizontal_offset)

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

                total_background_clips_duration += adjusted_background_clip_duration
                x += 1

                if total_background_clips_duration >= video_clip_duration:
                    break

    return (
        x,
        used_background_clips_paths,
        video_clip_background_clip_paths,
        video_map_index,
    )


def validate_chapter_number(chapter_number: int) -> bool:
    """
    Checks if a chapter number is valid.

    Parameters
    ----------
    chapter_number : int
        The chapter number to check the validity of.

    Returns
    -------
    bool
        True if the chapter number is valid, False otherwise.
    """

    return isinstance(chapter_number, int) and chapter_number >= 1 and chapter_number <= 114


def validate_chapter_verse_range(chapter_number: int, start_verse: int, end_verse: int) -> bool:
    """
    Checks if a chapter verse range is valid.

    Parameters
    ----------
    start_verse : int
        The start verse number of the chapter verse range to check the validity of.
    end_verse_number : int
        The end verse number of the chapter verse range to check the validity of.

    Returns
    -------
    bool
        True if the chapter verse range is valid, False otherwise.
    """

    chapter_verse_count = fetch_chapter_verse_count(chapter_number)

    return (
        isinstance(start_verse, int)
        and isinstance(end_verse, int)
        and start_verse < end_verse
        and end_verse <= chapter_verse_count
    )


def validate_language(language: Languages, valid_languages: list[Languages] = Languages) -> bool:
    """
    Checks if a language is valid.

    Parameters
    ----------
    language : str
        The language to check the validity of.

    Returns
    -------
    bool
        True if the language is valid, False otherwise.
    """

    return isinstance(language, Languages) and language in valid_languages


def validate_background_clip_duration(
    background_clip_duration: float, minimal_background_clip_duration: float, final_clip_leftover_duration: float
) -> bool:
    """
    Checks if the duration of a sub clip is valid.

    Parameters
    ----------
    background_clip_duration : float
        The duration of the sub clip.
    minimal_background_clip_duration : float
        The minimal duration of the sub clip.
    final_clip_leftover_duration : float
        The leftover duration of the final clip.

    Returns
    -------
    bool
        True if the duration of the sub clip is valid, False otherwise.
    """

    return (
        final_clip_leftover_duration - background_clip_duration >= minimal_background_clip_duration
        or final_clip_leftover_duration - background_clip_duration <= 0
    )


def create_shadow_clip(
    color: tuple[int, int, int], duration: float, size: tuple[int, int], opacity: float
) -> mpy.ColorClip:
    """
    Creates a shadow clip

    Parameters
    ----------
    color : tuple[int, int, int]
        The color of the shadow.
    duration : float
        The duration of the shadow clip.
    size : tuple[int, int]
        The size of the shadow clip.
    opacity : float
        The opacity of the shadow clip.

    Returns
    -------
    mpy.ColorClip
        The shadow clip.
    """

    return mpy.ColorClip(color=color, duration=duration, size=size).set_opacity(opacity)


def create_text_clip(
    background_color: str,
    color: str,
    duration: float,
    fade_duration: float,
    font: str,
    fontsize: int,
    method: str,
    position: tuple[str or float, str or float],
    size: tuple,
    text: str,
) -> mpy.TextClip:
    """
    Creates a text clip

    Parameters
    ----------
    background_color : str
        The background color of the text.
    color : str
        The color of the text.
    duration : float
        The duration of the text clip.
    fade_duration : float
        The fade duration of the text clip.
    font : str
        The font of the text.
    fontsize : int
        The font size of the text.
    method : str
        The method of the text clip.
    position : tuple[str or float, str or float]
        The position of the text clip.
    size : tuple
        The size of the text clip.
    text : str
        The text of the text clip.

    Returns
    -------
    mpy.TextClip
        The text clip.
    """

    return (
        mpy.TextClip(
            bg_color=background_color,
            color=color,
            font=font,
            fontsize=fontsize,
            method=method,
            size=size,
            txt=text,
        )
        .set_duration(duration)
        .set_position(position, relative=True)
        .crossfadein(fade_duration)
        .crossfadeout(fade_duration)
    )


def create_video_clip(
    background_clips_paths: list[list[str, float or int, int, str]],
    background_clips_speed: float,
    final_clip_duration: float,
    target_aspect_ratio: float,
    text_clips: list[mpy.TextClip],
    video_dimensions: tuple[int, int],
    video_mode: VideoModes,
    shadow_clip: mpy.ColorClip = None,
    text_duration: float = None,
) -> mpy.CompositeVideoClip:
    """
    Creates a video clip

    Parameters
    ----------
    background_clip_paths : list[list[str, float or int, int, str]]
        The paths of the background clips.
    final_clip_duration : float
        The duration of the final clip.
    target_aspect_ratio : float
        The target aspect ratio.
    text_clips : list[mpy.TextClip]
        The text clips.
    video_mode : VideoMode
        The video mode.
    video_dimensions : tuple[int, int]
        The dimensions of the video.
    background_clip_speed : float
        The speed of the background clip.
    shadow_clip : mpy.ColorClip, optional
        The shadow clip, by default None
    text_duration : float, optional
        The duration of the text, by default None

    Returns
    -------
    mpy.CompositeVideoClip
        The video clip.
    """

    background_clips = []
    video_width, video_height = video_dimensions

    if video_mode == VideoModes.VIDEO:
        for background_clip_info in background_clips_paths:
            background_clip_path = background_clip_info[0]
            background_clip_time_offset = background_clip_info[1]
            background_clip_horizontal_offset = background_clip_info[2]
            background_mirrored = background_clip_info[3]

            background_clip = mpy.VideoFileClip(background_clip_path).speedx(background_clips_speed)
            if background_mirrored == "True":
                background_clip = background_clip.fx(mpy.vfx.mirror_x)

            background_clip_duration = (
                calculate_clip_duration(background_clip_path, background_clips_speed)
            ) - background_clip_time_offset

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

            current_aspect_ratio = background_clip.w / background_clip.h

            if current_aspect_ratio > target_aspect_ratio:
                new_width = int(background_clip.h * target_aspect_ratio)
                horizontal_offset = (background_clip.w - new_width) // 2
                background_clip = background_clip.crop(x1=horizontal_offset, x2=horizontal_offset + new_width).resize(
                    video_dimensions
                )

            background_clips.append(background_clip)

        video_clip = mpy.concatenate_videoclips(clips=background_clips, method="chain")
        # background_clip = background_clip.fx(mpy.vfx.colorx, 1.25) # Saturation
    elif video_mode == VideoModes.IMAGE:
        background_clip = mpy.VideoFileClip(background_clips_paths[0][0])
        total_frames = int(background_clip.fps * background_clip.duration)
        random_frame_number = random.randint(1, total_frames)

        current_aspect_ratio = background_clip.w / background_clip.h

        if current_aspect_ratio > target_aspect_ratio:
            new_width = int(background_clip.h * target_aspect_ratio)
            horizontal_offset = (background_clip.w - new_width) // 2
            background_clip = background_clip.crop(x1=horizontal_offset, x2=horizontal_offset + new_width).resize(
                video_dimensions
            )

        random_frame = background_clip.get_frame(random_frame_number / background_clip.fps)
        video_clip = mpy.ImageClip(random_frame)

    text_duration = text_duration if text_duration is not None else final_clip_duration
    video_clip = video_clip.set_duration(final_clip_duration)
    clips = [video_clip, shadow_clip, *text_clips] if shadow_clip is not None else [video_clip, *text_clips]
    final_video_clip = mpy.CompositeVideoClip(clips, use_bgclip=True).set_duration(final_clip_duration)

    if not video_mode:
        final_video_clip = final_video_clip.fadein(0.25).fadeout(0.25)

    return final_video_clip
