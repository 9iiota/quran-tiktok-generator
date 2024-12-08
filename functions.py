import concurrent.futures
from threading import Lock

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
    AdditionalVideoSettings,
    Languages,
)
from fuzzywuzzy import fuzz
from pyquran import quran
from typing import Optional


def create_video(
    account: Account,
    audioSettings: AudioSettings,
    csvColumnNames: CSVColumnNames,
    timeModifiers: TimeModifiers,
    videoSettings: VideoSettings,
    output_video_verse_range: tuple[int, int],
    outputFileName: str,
    chapterCsvFile: str,
    timestampsCsvFile: str,
    additionalVideoSettings: Optional[
        AdditionalVideoSettings
    ] = AdditionalVideoSettings(),
    verse_text_text_clip: Optional[TextClipInfo] = None,
    verse_translation_text_clip: Optional[TextClipInfo] = None,
    verse_number_text_clip: Optional[TextClipInfo] = None,
    reciter_name: Optional[str] = None,
    reciter_name_text_clip: Optional[TextClipInfo] = None,
    outputFile: Optional[str] = None,
) -> None:
    """
    Create a video with the given parameters.

    Parameters
    ----------
    """

    if not isinstance(account, Account):
        account = account.value

    if not os.path.isfile(audioSettings.audioFile):
        raise FileNotFoundError(f"{audioSettings.audioFile} is not a file.")

    audioFileDirectory = os.path.dirname(audioSettings.audioFile)

    if outputFile:
        outputFile = outputFile.replace("\\", "/")

        try:
            outputDirectory = os.path.dirname(outputFile)
        except Exception:
            raise NotADirectoryError(f"{outputDirectory} is not a valid directory.")
    else:
        outputDirectory = os.path.join(audioFileDirectory, "Videos")
        outputFile = os.path.join(outputDirectory, f"{outputFileName}.mp4")

    if not os.path.isdir(outputDirectory):
        os.mkdir(outputDirectory)

    chapterCsvFile = chapterCsvFile.replace("\\", "/")
    if not os.path.isfile(chapterCsvFile):
        # Create chapter CSV file and add verses
        columnNames = [csvColumnNames.verseNumber, csvColumnNames.verseText]
        if not CreateCsvFile(chapterCsvFile, columnNames):
            PrintColored(
                Fore.RED,
                f"Unable to create {chapterCsvFile} with column names {columnNames}.",
            )
            return
        PrintColored(
            Fore.GREEN,
            f"Created {chapterCsvFile} with column names {columnNames}.",
        )

        if not AddVerses(
            chapterCsvFile,
            audioSettings.chapterNumber,
            audioSettings.verseRange,
            csvColumnNames.verseNumber,
            csvColumnNames.verseText,
        ):
            PrintColored(Fore.RED, f"Unable to add verse texts to {chapterCsvFile}.")
            return
        PrintColored(Fore.GREEN, f"Added verse texts to {chapterCsvFile}.")

    if AddTranslations(
        chapterCsvFile,
        account.language,
        audioSettings.chapterNumber,
        audioSettings.verseRange,
        csvColumnNames.timestamp,
    ):
        PrintColored(Fore.GREEN, f"Added verse translations to {chapterCsvFile}.")
        return

    # TODO
    if not os.path.isfile(timestampsCsvFile):
        raise FileNotFoundError(f"{timestampsCsvFile} is not a valid path.")
    else:
        if UpdateCsvFileTimestamps(
            chapterCsvFile, timestampsCsvFile, csvColumnNames.timestamp
        ):
            PrintColored(Fore.GREEN, f"Added timestamps to {chapterCsvFile}.")

            if UpdateCsvFileVerseNumbers(
                chapterCsvFile,
                audioSettings.chapterNumber,
                audioSettings.verseRange,
                csvColumnNames.verseNumber,
                csvColumnNames.verseText,
                csvColumnNames.timestamp,
            ):
                PrintColored(Fore.GREEN, f"Added verse numbers to {chapterCsvFile}.")

    languageAbbreviation = account.language.value.abbreviation

    # TODO: A clip should be able to be created without language abbreviation column
    chapterCsvLines = SelectColumnsFromCsvFile(
        chapterCsvFile,
        [
            csvColumnNames.verseNumber,
            csvColumnNames.verseText,
            languageAbbreviation,
            csvColumnNames.timestamp,
        ],
    )

    startLine, endLine = GetLoopRange(
        chapterCsvLines,
        audioSettings.chapterNumber,
        output_video_verse_range,
        additionalVideoSettings.startLine,
        additionalVideoSettings.endLine,
    )

    videoWidth, videoHeight = videoSettings.videoDimensions

    videoStartTimestamp = chapterCsvLines[startLine - 1][3].strip().split(",")[0]
    if timeModifiers.startTimeModifier:
        videoStart = OffsetTimestamp(
            videoStartTimestamp, timeModifiers.startTimeModifier
        )
    else:
        videoStart = OffsetTimestamp(videoStartTimestamp, timeModifiers.timeModifier)

    videoEndTimestamp = chapterCsvLines[endLine - 1][3].strip().split(",")[0]
    videoEnd = OffsetTimestamp(videoEndTimestamp, timeModifiers.endTimeModifier)

    # video_duration = GetTimeDifferenceSeconds(videoStart, videoEnd)

    audio = mpy.AudioFileClip(audioSettings.audioFile).subclip(videoStart, videoEnd)

    # TODO: Unsure if it is better to have absolute or relative paths
    # if video_map:
    #     video_map = convert_video_map_paths_to_absolute_paths(video_map)

    allBackgroundClips = GetRelativeMp4Paths(account.clipDirectories)
    targetAspectRatio = videoWidth / videoHeight
    textClips = []
    usedBackgroundClips = []
    videoClipEntries = []
    videoMapOutput = {}

    if additionalVideoSettings.videoMap:
        additionalVideoSettings.videoMap = {
            int(key): value for key, value in additionalVideoSettings.videoMap.items()
        }

    videoClipEntriesLock = Lock()

    loopRange = range(startLine, endLine)

    PrintColored(Fore.MAGENTA, f"Creating clips in range {startLine}-{endLine - 1}...")

    def CreateClip(line):
        videoClipIndex = line - startLine + 1
        chapterCsvLine = chapterCsvLines[line - 1]

        # TODO: A line should be able to exist without verse_translation
        verseNumber, verseText, verseTranslation, timestamp = chapterCsvLine

        PrintColored(Fore.MAGENTA, f"Creating clip {videoClipIndex}...")

        nextLine = chapterCsvLines[line]
        nextTimestamp = nextLine[3]

        if line == startLine:
            audioStart = videoStart
        else:
            audioStart = OffsetTimestamp(
                StripTimestamp(timestamp)[0], timeModifiers.timeModifier
            )

        if line == endLine - 1:
            audioEnd = videoEnd
        else:
            audioEnd = OffsetTimestamp(
                StripTimestamp(nextTimestamp)[0], timeModifiers.timeModifier
            )

        maxVideoClipDuration = GetTimeDifferenceSeconds(audioStart, audioEnd)

        try:
            textEnd = OffsetTimestamp(
                StripTimestamp(nextTimestamp)[1], timeModifiers.timeModifier
            )
            textDuration = GetTimeDifferenceSeconds(audioStart, textEnd)
        except IndexError:
            textDuration = maxVideoClipDuration

        if not additionalVideoSettings.backgroundVideo:
            videoClipDuration = 0
            videoClipBackgroundClips = []

            if videoSettings.videoMode == VideoModes.VIDEO:
                while videoClipDuration < maxVideoClipDuration:
                    # Get new background clips until the total duration of the background clips is long enough for the video clip
                    backgroundClipPath = GetRandomChoice(allBackgroundClips)

                    # if len(usedBackgroundClips) == len(allBackgroundClips):
                    #     allowDuplicateBackgroundClips = True

                    if backgroundClipPath not in usedBackgroundClips:
                        clipDuration = GetClipDuration(
                            backgroundClipPath,
                            videoSettings.clipSpeed,
                        )
                        maxTimeOffset = GetMaxTimeOffset(
                            clipDuration,
                            videoSettings.minimumClipDuration,
                        )
                        timeOffset = get_random_time_offset(maxTimeOffset)
                        offsetClipDuration = clipDuration - timeOffset

                        # If the background clip remaining duration is longer than the video clip duration, set the adjusted background clip duration to the video clip duration
                        adjustedClipDuration = min(
                            maxVideoClipDuration, offsetClipDuration
                        )

                        remainingVideoClipDuration = (
                            maxVideoClipDuration - videoClipDuration
                        )

                        if (
                            remainingVideoClipDuration - adjustedClipDuration
                            >= videoSettings.minimumClipDuration
                            or remainingVideoClipDuration - adjustedClipDuration <= 0
                        ):
                            backgroundClip = mpy.VideoFileClip(backgroundClipPath)

                            maxHorizontalOffset = GetMaxHorizontalOffset(
                                backgroundClip.w, videoWidth
                            )
                            # if maxHorizontalOffset < 0:
                            #     raise ValueError(
                            #         f"Verse {videoMapIndex} Background clip {x + 1} width ({backgroundClip.w}) is less than video width ({video_width})"
                            #     )

                            horizontalOffset = GetHorizontalOffset(maxHorizontalOffset)

                            if videoSettings.allowMirroredClips:
                                isMirrored = str(random.choice([True, False]))
                            else:
                                isMirrored = "False"

                            videoClipBackgroundClips.append(
                                [
                                    backgroundClipPath,
                                    timeOffset,
                                    horizontalOffset,
                                    isMirrored,
                                ]
                            )
                            usedBackgroundClips.append(backgroundClipPath)

                            videoClipDuration += adjustedClipDuration

                videoMapOutput[videoClipIndex] = videoClipBackgroundClips
            else:
                backgroundClipPath = GetRandomChoice(allBackgroundClips)
                backgroundClip = mpy.VideoFileClip(backgroundClipPath)
                clipDuration = GetClipDuration(
                    backgroundClipPath, videoSettings.clipSpeed
                )

                maxTimeOffset = GetMaxTimeOffset(
                    clipDuration,
                    videoSettings.minimumClipDuration,
                )
                timeOffset = get_random_time_offset(maxTimeOffset)

                maxHorizontalOffset = GetMaxHorizontalOffset(
                    backgroundClip.w, videoWidth
                )

                if maxHorizontalOffset < 0:
                    raise ValueError(
                        f"Background clip {backgroundClipPath} width ({backgroundClip.w}) is less than video width ({videoWidth})"
                    )

                horizontalOffset = GetHorizontalOffset(maxHorizontalOffset)

                isMirrored = get_background_clip_mirrored(
                    backgroundClipPath,
                    videoSettings.allowMirroredClips,
                )

                videoClipBackgroundClips.append(
                    [
                        backgroundClipPath,
                        timeOffset,
                        horizontalOffset,
                        isMirrored,
                    ]
                )

        # Append text clips
        textClips = []

        if verse_text_text_clip:
            verse_text_color = account.mode.value.verse_text_color
            verse_text_clip = verse_text_text_clip.create_text_clip(
                color=verse_text_color,
                duration=textDuration,
                font=account.verseTextFontFile,
                text=verseText,
            )
            textClips.append(verse_text_clip)

        if verse_translation_text_clip:
            verse_translation_color = account.mode.value.verse_translation_color
            verse_translation_clip = verse_translation_text_clip.create_text_clip(
                color=verse_translation_color,
                duration=textDuration,
                font=account.verseTranslationFontFile,
                text=verseTranslation,
            )
            textClips.append(verse_translation_clip)

        # Append verse number text clip if it is a new verse
        if verse_number_text_clip and verseNumber != "":
            verse_number_color = account.mode.value.verse_number_color
            verse_number_clip = verse_number_text_clip.create_text_clip(
                color=verse_number_color,
                duration=textDuration,
                font=account.verseNumberFontFile,
                text=verseNumber,
            )
            textClips.append(verse_number_clip)

        # Append reciter name text clip if it is the first clip
        if line == startLine and reciter_name and reciter_name_text_clip:
            reciter_name_color = account.mode.value.reciter_name_color
            reciter_name_clip = reciter_name_text_clip.create_text_clip(
                color=reciter_name_color,
                duration=textDuration,
                font=account.reciterNameFontFile,
                text=reciter_name,
            )
            textClips.append(reciter_name_clip)

        if not additionalVideoSettings.backgroundVideo:
            # Create shadow clip to put overlay on the video clip
            shadow_color = account.mode.value.shadow_color
            shadow_opacity = account.mode.value.shadow_opacity
            shadow_clip = create_shadow_clip(
                size=videoSettings.videoDimensions,
                color=shadow_color,
                duration=maxVideoClipDuration,
                opacity=shadow_opacity,
            )

            PrintColored(Fore.CYAN, f"{videoClipIndex} Using background clip(s):")

            for backgroundClipPath in videoClipBackgroundClips:
                PrintColored(Fore.CYAN, f"- {backgroundClipPath[0]}")

            videoClipEntry = (
                videoClipIndex,
                CreateVideoClip(
                    background_clips_paths=videoClipBackgroundClips,
                    background_clips_speed=videoSettings.clipSpeed,
                    final_clip_duration=maxVideoClipDuration,
                    target_aspect_ratio=targetAspectRatio,
                    text_clips=textClips,
                    video_dimensions=videoSettings.videoDimensions,
                    video_mode=videoSettings.videoMode,
                    shadow_clip=shadow_clip,
                    text_duration=textDuration,
                ),
            )

            # Use lock when appending to the shared list
            with videoClipEntriesLock:
                videoClipEntries.append(videoClipEntry)

            PrintColored(Fore.GREEN, f"Created clip {videoClipIndex}")
        else:
            # Set text clip start times if using a single background video
            text_start_time = GetTimeDifferenceSeconds(audioStart, videoStart)

            textClips[0] = textClips[0].set_start(text_start_time)
            textClips[1] = textClips[1].set_start(text_start_time)

            # Append verse number text clip
            if verseNumber != "":
                textClips[2] = textClips[2].set_start(text_start_time)

            # Append reciter name text clip if it is the first clip
            if line == startLine and reciter_name:
                textClips[-1] = textClips[-1].set_start(text_start_time)

            textClips.extend(textClips)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(CreateClip, line) for line in loopRange]

        for future in concurrent.futures.as_completed(
            futures
        ):  # Process as they complete
            try:
                future.result()  # Raise any exception from the thread
            except Exception as e:
                print(f"Exception in thread: {e}")

    print("All tasks are completed. Proceeding to the next part.")

    videoClipEntries = sorted(videoClipEntries, key=lambda clip: clip[0])
    videoClips = [videoClipEntry[1] for videoClipEntry in videoClipEntries]

    if not additionalVideoSettings.backgroundVideo:
        final_video = mpy.concatenate_videoclips(
            clips=videoClips, method="chain"
        ).set_audio(audio)
    else:
        background_clip = mpy.VideoFileClip(
            additionalVideoSettings.backgroundVideo
        ).subclip(videoStart)

        background_clip_width, background_clip_height = background_clip.size
        current_aspect_ratio = background_clip_width / background_clip_height

        if current_aspect_ratio > targetAspectRatio:
            new_width = int(background_clip_height * targetAspectRatio)

            if not additionalVideoSettings.backgroundVideoHorizontalOffset:
                background_video_horizontal_offset = (
                    background_clip_width - new_width
                ) // 2
            else:
                background_video_horizontal_offset = (
                    additionalVideoSettings.backgroundVideoHorizontalOffset
                )

            background_clip = background_clip.crop(
                x1=background_video_horizontal_offset,
                x2=background_video_horizontal_offset + new_width,
            ).resize(videoSettings.videoDimensions)
        else:
            new_height = int(background_clip_width / targetAspectRatio)

            if not additionalVideoSettings.backgroundVideoVerticalOffset:
                background_video_vertical_offset = (
                    background_clip_height - new_height
                ) // 2
            else:
                background_video_vertical_offset = (
                    additionalVideoSettings.backgroundVideoVerticalOffset
                )

            background_clip = background_clip.crop(
                y1=background_video_vertical_offset,
                y2=background_video_vertical_offset + new_height,
            ).resize(videoSettings.videoDimensions)

        shadow_clip = create_shadow_clip(
            color=account.mode.value.shadow_color,
            duration=background_clip.duration,
            opacity=account.mode.value.shadow_opacity,
            size=videoSettings.videoDimensions,
        )

        video = mpy.CompositeVideoClip([background_clip, shadow_clip])
        final_video = mpy.CompositeVideoClip(
            [video, *textClips], use_bgclip=True
        ).set_audio(audio)

        videoMapOutput = additionalVideoSettings.backgroundVideo

    PrintColored(Fore.GREEN, "Creating final video...")

    json_output_file_path = outputFile.replace(".mp4", ".json")

    formatter = Formatter()
    formatter.use_tab_to_indent = True
    formatter.nested_bracket_padding = False
    formatter.max_inline_length = 300
    formatter.max_inline_complexity = 1
    formatter.json_eol_style = EolStyle.LF
    formatter.dont_justify_numbers = True

    formatter.dump(
        videoMapOutput,
        output_file=json_output_file_path,
        newline_at_eof=True,
    )

    try:
        if additionalVideoSettings.backgroundVideo:
            final_video.write_videofile(
                filename=outputFile,
                fps=video.fps,
            )
        elif videoSettings.videoMode == VideoModes.VIDEO:
            final_video.write_videofile(
                codec="libx264",
                filename=outputFile,
            )
        elif videoSettings.videoMode == VideoModes.IMAGE:
            final_video.write_videofile(
                codec="libx264",
                filename=outputFile,
                fps=60,
            )

        PrintColored(Fore.GREEN, "Created final video")
    except Exception as error:
        raise Exception(f"Failed to create final video: {error}") from error


def adjust_timestamps(input_file, output_file, seconds_to_add):
    try:
        with open(input_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            fieldnames = reader.fieldnames

            data = list(reader)
            for line in range(len(data)):
                data[line]["Start"] = OffsetTimestamp(
                    data[line]["Start"], seconds_to_add
                )

            with open(output_file, "w", encoding="utf-8") as output_csvfile:
                writer = csv.DictWriter(
                    output_csvfile, fieldnames=fieldnames, delimiter="\t"
                )
                writer.writeheader()
                writer.writerows(data)

        RemoveEmptyRows(output_file)

        print(f"Timestamps modified and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def CreateCsvFile(path: str, columnNames: list[str]) -> bool:
    """
    Creates a CSV file using the given column names.
    """

    with open(path, "w", encoding="utf-8") as file:
        dictWriter = csv.DictWriter(file, fieldnames=columnNames)

        try:
            dictWriter.writeheader()

            return True
        except Exception:
            return False


def AddVerses(
    csvFilePath: str,
    chapterNumber: int,
    verseRange: tuple[int, int],
    verseNumberColumnName: str,
    verseTextColumnName: str,
) -> bool:
    """
    Adds verses to the CSV file.
    """

    try:
        with open(csvFilePath, "r", encoding="utf-8") as file:
            dictReader = csv.DictReader(file)

            fieldNames = dictReader.fieldnames
            verseNumberColumnIndex = fieldNames.index(verseNumberColumnName)
            verseTextColumnIndex = fieldNames.index(verseTextColumnName)

            rows = []
            startVerse, endVerse = verseRange
            verseTexts = GetChapterText(chapterNumber)[startVerse - 1 : endVerse]
            for index, verseText in enumerate(verseTexts):
                verseNumber = f"{chapterNumber}:{startVerse + index}"
                if verseText is not None:
                    rows.append(
                        {
                            fieldNames[verseNumberColumnIndex]: verseNumber,
                            fieldNames[verseTextColumnIndex]: verseText,
                        }
                    )

        with open(csvFilePath, "w", encoding="utf-8") as file:
            dictWriter = csv.DictWriter(file, fieldnames=fieldNames)
            dictWriter.writeheader()
            dictWriter.writerows(rows)

        if RemoveEmptyRows(csvFilePath):
            return True
    except Exception:
        return False


def AddTranslations(
    csvFilePath: str,
    language: Languages,
    chapterNumber: int,
    verseRange: tuple[int, int],
    timestampColumnName: str,
) -> bool:
    """
    Appends the verse translations of a chapter from the Qur'an to a CSV file
    """

    try:
        with open(csvFilePath, "r", encoding="utf-8") as file:
            dictReader = csv.DictReader(file)

            fieldNames = dictReader.fieldnames
            if language.value.abbreviation not in fieldNames:
                if timestampColumnName in fieldNames:
                    # Insert the translation column before the timestamp column
                    timestampColumnIndex = fieldNames.index(timestampColumnName)
                    fieldNames.insert(timestampColumnIndex, language.value.abbreviation)
                else:
                    # Append the translation column to the end
                    fieldNames.append(language.value.abbreviation)

                rows = list(dictReader)
                startVerse, endVerse = verseRange
                verseTranslations = GetChapterTranslation(chapterNumber, language)[
                    startVerse - 1 : endVerse
                ]
                for index, verseTranslation in enumerate(verseTranslations):
                    rows[index][language.value.abbreviation] = verseTranslation

        with open(csvFilePath, "w", encoding="utf-8") as file:
            dictWriter = csv.DictWriter(file, fieldnames=fieldNames)
            dictWriter.writeheader()
            dictWriter.writerows(rows)

        if RemoveEmptyRows(csvFilePath):
            return True
    except Exception:
        return False


def RemoveEmptyRows(csvFilePath: str) -> bool:
    """
    Removes empty rows from a CSV file
    """

    try:
        with open(csvFilePath, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = [row for row in reader if any(cell.strip() != "" for cell in row)]

        with open(csvFilePath, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return True
    except Exception:
        return False


def SelectColumnsFromCsvFile(
    csv_file_path: str, columns_to_select: list[str]
) -> list[list[str]]:
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


def UpdateCsvFileTimestamps(
    chapter_csv_file_path: str,
    timestamps_csv_file_path: str,
    timestamp_column_name: str,
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
        sorted_timestamps = sorted(
            sorted_nested_timestamps, key=convert_timestamp_to_seconds
        )

        with open(chapter_csv_file_path, "r", encoding="utf-8") as chapter_csv_file:
            csv_dict_reader = csv.DictReader(chapter_csv_file)
            field_names = csv_dict_reader.fieldnames

            if timestamp_column_name not in field_names:
                field_names.append(timestamp_column_name)

            data = list(csv_dict_reader)

            while len(data) < len(sorted_timestamps):
                data.append(
                    {timestamp_column_name: sorted_timestamps[len(data)].strip()}
                )

            for line in range(len(sorted_timestamps)):
                if isinstance(sorted_timestamps[line], list):
                    for i in range(len(sorted_timestamps[line])):
                        sorted_timestamps[line][i] = sorted_timestamps[line][i].strip()
                    data[line][timestamp_column_name] = ",".join(
                        sorted_timestamps[line]
                    )
                else:
                    data[line][timestamp_column_name] = sorted_timestamps[line].strip()

            with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
                writer = csv.DictWriter(chapter_csv_file, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(data)

    if RemoveEmptyRows(chapter_csv_file_path):
        return True


def UpdateCsvFileVerseNumbers(
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
        verse_texts = GetChapterText(chapter_number)[start_verse - 1 : end_verse]
        indexed_verse_texts = [
            list(item) for item in zip(range(start_verse, end_verse + 1), verse_texts)
        ]

        for row in csv_dict_reader:
            if row[verse_text_column_name] != "" or row[timestamp_column_name] == "":
                best_ratio, best_verse_number = (0, None)
                csv_text = row[verse_text_column_name]

                for tuple in indexed_verse_texts:
                    letter_difference = len(tuple[1]) - len(csv_text)

                    # Here we check if the indexed verse text is long or equal to the CSV text
                    # We do this so we can skip over texts that would definitely not match due to being too short
                    if letter_difference >= 0:
                        # Here we get the indexes of the start of each word in the indexed verse text
                        # We do this because we're comparing words, so there's no need to start checking in the middle of a word or at a space
                        word_start_indexes = [0] + [
                            space_index + 1
                            for space_index, char in enumerate(tuple[1])
                            if char == " "
                        ]

                        for word_start_index in word_start_indexes:
                            # Here we check the match ratio of the CSV text and the indexed verse text starting at each word
                            # We do this to find the best match
                            match = tuple[1][
                                word_start_index : len(csv_text) + word_start_index
                            ]
                            ratio = fuzz.ratio(csv_text, match)

                            # Replace the previous ratio if this one is better
                            if ratio > best_ratio:
                                best_ratio, best_verse_number = (ratio, tuple[0])

                            # If it's a perfect match, we don't need to continue
                            if ratio == 100:
                                break

                    # If it's a perfect match, we don't need to continue
                    if best_ratio == 100:
                        break

                if best_ratio >= 90:
                    verse = f"{chapter_number}:{best_verse_number}"
                    if verse not in existing_verses:
                        row[verse_number_column_name] = verse
                        existing_verses.add(verse)
                    else:
                        row[verse_number_column_name] = ""

                    with contextlib.suppress(IndexError):
                        indexed_verse_texts[0][1] = re.sub(
                            match, "", indexed_verse_texts[0][1]
                        ).strip()

                        if indexed_verse_texts[0][1] == "":
                            indexed_verse_texts.pop(0)
                        # if indexed_verse_texts[0][0] != best_verse_number:
                        #     indexed_verse_texts.pop(0)
                else:
                    row[verse_number_column_name] = ""

            data.append(row)
        with open(chapter_csv_file_path, "w", encoding="utf-8") as chapter_csv_file:
            csv_dict_writer = csv.DictWriter(chapter_csv_file, fieldnames=field_names)
            csv_dict_writer.writeheader()
            csv_dict_writer.writerows(data)

    if RemoveEmptyRows(chapter_csv_file_path):
        return True


def GetLoopRange(
    chapter_csv_lines: list[list[str]],
    chapter_number: int,
    verse_range: tuple[int, int],
    start_line: int = None,
    end_line: int = None,
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

    if not start_line:
        start_line = verse_numbers.index(f"{chapter_number}:{verse_range_start}") + 1

    if not end_line:
        end_line = verse_numbers.index(f"{chapter_number}:{verse_range_end}") + 1

        while end_line < len(verse_numbers) and verse_numbers[end_line] == "":
            end_line += 1
        end_line = min(len(chapter_csv_lines), end_line + 1)
    else:
        end_line += 1

    return (start_line, end_line)


def GetTimeDifferenceSeconds(time1: str, time2: str) -> float:
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


def OffsetTimestamp(timestamp: str, time_offset_seconds: float) -> str:
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

    new_timedelta = max(
        original_timedelta + timedelta(seconds=time_offset_seconds), timedelta(0)
    )

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


def GetChapterTranslation(chapterNumber: int, language: Languages) -> list[str]:
    """
    Gets the translation of a chapter from the Qur'an
    """

    try:
        translationId = language.value.translation_id
        response = requests.get(
            f"https://api.quran.com/api/v4/quran/translations/{translationId}?chapter_number={chapterNumber}"
        )

        return [
            re.sub(
                "’",
                "'",
                re.sub(
                    "ʿ",
                    "'",
                    re.sub(
                        "ū",
                        "u",
                        re.sub(
                            "صَۣ",
                            "صَ",
                            re.sub(
                                "ḥ",
                                "h",
                                re.sub(
                                    "ā",
                                    "a",
                                    re.sub(r"<.*?>*<.*?>", "", translation["text"]),
                                ),
                            ),
                        ),
                    ),
                ),
            )
            for translation in response.json()["translations"]
        ]
    except Exception as error:
        raise Exception(
            f"Failed to fetch translation for chapter {chapterNumber} in {language.value['abbreviation']}."
        ) from error


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


def GetChapterText(chapterNumber: int) -> list[str]:
    """
    Gets the text of a chapter from the Qur'an
    """

    try:
        response = requests.get(
            f"https://api.quran.com/api/v4/quran/verses/uthmani?chapter_number={chapterNumber}"
        )

        return [
            re.sub("ا۟", "ا", verse["text_uthmani"])
            for verse in response.json()["verses"]
        ]
    except Exception as error:
        raise Exception(f"Failed to fetch text for chapter {chapterNumber}.") from error


def PrintColored(color: str, text: str) -> None:
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
            lambda value: isinstance(value[0], str),
            [value[0] for values in dictionary.values() for value in values],
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


def GetRelativeMp4Paths(
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


def GetClipDuration(clipPath: str, clipSpeed: float) -> float:
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

    return GetVideoDurationSeconds(clipPath) / clipSpeed


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
        return GetHorizontalOffset(max_horizontal_offset)


def GetMaxHorizontalOffset(clip_width: int, video_width: int) -> int:
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


def GetMaxTimeOffset(clip_duration: float, minimal_clip_duration: float) -> float:
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


def GetHorizontalOffset(max_horizontal_offset: int) -> int:
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


def GetRandomChoice(all_paths: list[str]) -> str:
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


def GetVideoDurationSeconds(mp4File: str) -> float:
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

    return mpy.VideoFileClip(mp4File).duration


def sort_nested_timestamps(
    timestamps: list[str or list[str]],
) -> list[str or list[str]]:
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
            timestamps[i] = sorted(
                timestamp, key=convert_timestamp_to_seconds, reverse=True
            )

    return timestamps


def StripTimestamp(timestamp: str) -> str:
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
    videoClipDuration: float,
    used_background_clips_paths: list[str],
    video_clip_background_clip_paths: list[list[str, float or int, int, str]],
    maxVideoClipDuration: float,
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
        background_clip_path = GetRandomChoice(all_background_clips_paths)

        if len(used_background_clips_paths) == len(all_background_clips_paths):
            allow_duplicate_background_clips = True

        if allow_duplicate_background_clips or (
            not allow_duplicate_background_clips
            and background_clip_path not in used_background_clips_paths
            and (
                (
                    video_map is not None
                    and not dictionary_contains_value(video_map, background_clip_path)
                )
                or video_map is None
            )
        ):
            background_clip_duration = GetClipDuration(
                background_clip_path, background_clips_speed
            )

            max_time_offset = GetMaxTimeOffset(
                background_clip_duration, minimal_background_clip_duration
            )
            background_clip_time_offset = get_random_time_offset(max_time_offset)
            time_offsetted_background_clip_duration = (
                background_clip_duration - background_clip_time_offset
            )

            # TO BE ADDED WHEN DURATION IN VIDEO MAPS IS IMPLEMENTED
            # # Get a random clip duration between the minimal clip duration and the leftover duration
            # adjusted_background_clip_duration = max(
            #     MINIMAL_CLIP_DURATION,
            #     random.uniform(MINIMAL_CLIP_DURATION, min(background_clip_leftover_duration, video_clip_duration)),
            # )

            # If the background clip remaining duration is longer than the video clip duration, set the adjusted background clip duration to the video clip duration
            adjusted_background_clip_duration = min(
                time_offsetted_background_clip_duration, maxVideoClipDuration
            )

            remainingVideoClipDuration = maxVideoClipDuration - videoClipDuration

            if validate_background_clip_duration(
                adjusted_background_clip_duration,
                minimal_background_clip_duration,
                remainingVideoClipDuration,
            ):
                background_clip = mpy.VideoFileClip(background_clip_path)

                max_horizontal_offset = GetMaxHorizontalOffset(
                    background_clip.w, video_width
                )

                if max_horizontal_offset < 0:
                    raise ValueError(
                        f"Verse {video_map_index} Background clip {x + 1} width ({background_clip.w}) is less than video width ({video_width})"
                    )

                background_clip_horizontal_offset = GetHorizontalOffset(
                    max_horizontal_offset
                )

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

                videoClipDuration += adjusted_background_clip_duration
                x += 1

                if videoClipDuration >= maxVideoClipDuration:
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

    return (
        isinstance(chapter_number, int)
        and chapter_number >= 1
        and chapter_number <= 114
    )


def validate_chapter_verse_range(
    chapter_number: int, start_verse: int, end_verse: int
) -> bool:
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


def validate_language(
    language: Languages, valid_languages: list[Languages] = Languages
) -> bool:
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
    clipDuration: float,
    minimumClipDuration: float,
    remainingVideoClipDuration: float,
) -> bool:
    """
    Checks if the duration of a background clip is valid.

    Parameters
    ----------
    background_clip_duration : float
        The duration of the sub clip to check the validity of.
    minimal_background_clip_duration : float
        The minimal duration of the sub clip to check the validity of.
    video_clip_remaining_duration : float
        The remaining duration of the video clip.

    Returns
    -------
    bool
        True if the duration of the sub clip is valid, False otherwise.
    """

    return (
        remainingVideoClipDuration - clipDuration >= minimumClipDuration
        or remainingVideoClipDuration - clipDuration <= 0
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


def CreateVideoClip(
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

            background_clip = mpy.VideoFileClip(background_clip_path).speedx(
                background_clips_speed
            )
            if background_mirrored == "True":
                background_clip = background_clip.fx(mpy.vfx.mirror_x)

            background_clip_duration = (
                GetClipDuration(background_clip_path, background_clips_speed)
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
                background_clip = background_clip.crop(
                    x1=horizontal_offset, x2=horizontal_offset + new_width
                ).resize(video_dimensions)

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
            background_clip = background_clip.crop(
                x1=horizontal_offset, x2=horizontal_offset + new_width
            ).resize(video_dimensions)

        random_frame = background_clip.get_frame(
            random_frame_number / background_clip.fps
        )
        video_clip = mpy.ImageClip(random_frame)

    text_duration = text_duration if text_duration is not None else final_clip_duration
    video_clip = video_clip.set_duration(final_clip_duration)
    clips = (
        [video_clip, shadow_clip, *text_clips]
        if shadow_clip is not None
        else [video_clip, *text_clips]
    )
    final_video_clip = mpy.CompositeVideoClip(clips, use_bgclip=True).set_duration(
        final_clip_duration
    )

    if not video_mode:
        final_video_clip = final_video_clip.fadein(0.25).fadeout(0.25)

    return final_video_clip
