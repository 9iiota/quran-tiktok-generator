import cv2
import moviepy.editor as mpy
import os
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from enum import Enum
from plyer import notification
from pyquran import quran
from time import sleep

ARABIC_FONT = "Fonts/Hafs.ttf"
ENGLISH_FONT = "Fonts/Butler_Regular.otf"

class MODES(Enum):
    DARK = 1
    LIGHT = 2

def main():
    create_video(
        timestamps_csv_file_path=r"Surahs\29 - Al-'Ankabut\Markers.csv",
        count=100,
        full_audio_path=r"Surahs\29 - Al-'Ankabut\Abdul Rahman Mossad - Al-'Ankabut.mp3",
        background_clip_directory="Background_Clips",
        output_path=r"Surahs\29 - Al-'Ankabut\Videos\Abdul Rahman Mossad - Al-'Ankabut test.mp4",
        mode=MODES.LIGHT
    )

    # create_video(
    #     timestamps_csv_file_path=r"Surahs\101 - Al-Qari'ah\Markers.csv",
    #     count=100,
    #     full_audio_path=r"Surahs\101 - Al-Qari'ah\Salim Bahanan - Al-Qari'ah.mp3",
    #     background_clip_directory="Background_Clips",
    #     output_path=r"Surahs\101 - Al-Qari'ah\Videos\Salim Bahanan - Al-Qari'ah 2.mp4",
    #     mode=MODES.DARK
    # )

def get_timestamps(timestamps_csv_file_path):
    """
    Get the timestamps from the timestamps file.

    Args:
        timestamps_file_path (str): The path to the timestamps file.
        output_file_path (str): The path to the output file.

    Returns:
        str: The path to the output file.
    """
    with open(timestamps_csv_file_path, "r", encoding="utf-8") as csv_file:
        lines = csv_file.readlines()[1:]
        output_file_path = timestamps_csv_file_path.replace("Markers.csv", "timestamps.txt")
        with open(output_file_path, "w", encoding="utf-8") as output_file:
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

    return output_file_path

def get_time_difference_seconds(time1, time2):
    """
    Calculate the time difference between two time strings in the format "MM:SS.SSS".

    Args:
        time1 (str): The first time string.
        time2 (str): The second time string.

    Returns:
        float: The time difference in seconds.
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

def get_video_duration_seconds(video_path):
    """
    Get the duration of a video in seconds.

    Args:
        video_path (str): The path to the video file.

    Returns:
        float: The duration of the video in seconds.
    """
    video = cv2.VideoCapture(video_path)
    return video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)

def get_verse_text(chapter, verse):
    """
    Get the text of a verse from the Quran.

    Args:
        verse_key (str): The verse key of the verse.

    Returns:
        str: The text of the verse.
    """
    return quran.get_verse(chapter, verse, with_tashkeel=True)

def get_verse_translation(chapter, verse):
    """
    Get the translation of a verse from the Quran.

    Args:
        verse_key (str): The verse key of the verse.

    Returns:
        str: The translation of the verse.
    """
    response = requests.get(f"https://api.quran.com/api/v4/quran/translations/20?verse_key={chapter}:{verse}")
    translation = response.json()["translations"][0]["text"]
    soup = BeautifulSoup(translation, "html.parser")
    clean_text = soup.get_text()
    return clean_text

def create_single_clip(video_duration, video_clip_path, verse_text, verse_translation, text_duration, shadow_color, verse_text_color, verse_translation_color, shadow_opacity, fade_duration):
    """
    Create a single clip with the given parameters.

    Args:
        video_duration (float): The duration of the video.
        video_clip_path (str): The path to the video clip.
        verse_text (str): The text of the verse.
        verse_translation (str): The translation of the verse.
        text_duration (float, optional): The duration of the text. Defaults to None.
        shadow_opacity (float, optional): The opacity of the shadow. Defaults to 0.7.
        fade_duration (float, optional): The duration of the fade in and fade out. Defaults to 0.5.
        mode (MODES, optional): The mode of the video. Defaults to None.
        shadow_color (str, optional): The color of the shadow. Defaults to "rgb(0, 0, 0)".
        verse_text_color (str, optional): The color of the verse text. Defaults to "rgb(255, 255, 255)".
        verse_translation_color (str, optional): The color of the verse translation. Defaults to "rgb(255, 255, 255)".

    Returns:
        moviepy.video.compositing.CompositeVideoClip: The final clip.
    """
    text_duration = video_duration if text_duration is None else text_duration
    
    video_clip = mpy.VideoFileClip(video_clip_path)

    # Get the offsets
    x_offset = random.randint(0, max(0, video_clip.w - 603))
    y_offset = random.randint(0, max(0, video_clip.h - 1072))

    video_clip = video_clip.set_duration(
        video_duration
    ).crop(
        x1=x_offset,
        y1=y_offset,
        x2=x_offset + 603,
        y2=y_offset + 1072
    )

    shadow_clip = mpy.ColorClip(
        size=video_clip.size,
        color=shadow_color,
        duration=video_clip.duration
    ).set_opacity(
        shadow_opacity
    )

    video_with_shadow = mpy.CompositeVideoClip(
        [
            video_clip,
            shadow_clip
        ], 
        use_bgclip=True
    )

    verse_text_clip = mpy.TextClip(
        txt=verse_text,
        size=video_clip.size,
        color=verse_text_color,
        bg_color="transparent",
        fontsize=45,
        font=ARABIC_FONT
    ).set_position(
        (0, -.05), relative=True
    ).set_duration(
        text_duration
    ).crossfadein(
        fade_duration
    ).crossfadeout(
        fade_duration
    )

    verse_translation_clip = mpy.TextClip(
        txt=verse_translation,
        size=video_clip.size,
        color=verse_translation_color,
        bg_color="transparent",
        fontsize=18,
        font=ENGLISH_FONT
    ).set_position(
        (0, 0), relative=True
    ).set_duration(
        text_duration
    ).crossfadein(
        fade_duration
    ).crossfadeout(
        fade_duration
    )

    final_clip = mpy.CompositeVideoClip(
        [
            video_with_shadow,
            verse_text_clip,
            verse_translation_clip
        ], 
        use_bgclip=True
    ).set_duration(
        video_duration
    ).set_fps(
        24
    )

    return final_clip

def create_video(timestamps_csv_file_path, count, full_audio_path, background_clip_directory, output_path, mode=None, shadow_color=(0, 0, 0), verse_text_color="rgb(255, 255, 255)", verse_translation_color="rgb(255, 255, 255)", shadow_opacity=0.7, fade_duration=0.5):
    """
    Create a video with the given parameters.

    Args:
        timestamps_csv_file_path (str): The path to the timestamps CSV file.
        count (int): The number of clips in the final video.
        full_audio_path (str): The path to the full audio file.
        background_clip_directory (str): The path to the directory containing the background clips.
        output_path (str): The path to the output video.
    """
    if mode == MODES.DARK:
        shadow_color = (0, 0, 0)
        verse_text_color = "rgb(255, 255, 255)"
        verse_translation_color = "rgb(255, 255, 255)"
    elif mode == MODES.LIGHT:
        shadow_color = (255, 255, 255)
        verse_text_color = "rgb(0, 0, 0)"
        verse_translation_color = "rgb(0, 0, 0)"

    array = []
    duration = 0

    # Get the timestamps from the timestamps file
    timestamps_txt_file_path = get_timestamps(timestamps_csv_file_path)

    # Get the verse key from the Arabic text
    chapter = int(input("Enter the chapter number: "))
    verse = int(input("Enter the verse number: "))

    with open("chapter_text.txt", "w", encoding="utf-8") as arabic_file, open("chapter_translation.txt", "w", encoding="utf-8"):
        pass

    with open("chapter_text.txt", "a", encoding="utf-8") as arabic_file, open("chapter_translation.txt", "a", encoding="utf-8") as english_file:
        for i in range(1, count + 1):
            try:
                text = get_verse_text(chapter, verse + i - 1)  # Fetch tajweed for this verse
                if text != "":
                    arabic_file.write(text + "\n")

                    translation = get_verse_translation(chapter, verse + i - 1)  # Fetch translation for this verse
                    english_file.write(translation + "\n")
                else:
                    arabic_file.writelines(arabic_file.readlines()[:-1])
                    english_file.writelines(english_file.readlines()[:-1])
                    break
            except:
                pass

    input("Appropriately edit the text files now...")

    with open("chapter_text.txt", "r", encoding="utf-8") as arabic_file, \
        open("chapter_translation.txt", "r", encoding="utf-8") as english_file, \
        open(timestamps_txt_file_path, "r", encoding="utf-8") as timestamps_file:
        arabic_lines = arabic_file.readlines()
        english_lines = english_file.readlines()
        timestamps2 = timestamps_file.readlines()
        used_video_clips = []
        for i in range(1, count + 1):
            try:
                text = arabic_lines[i - 1].strip()
                translation = english_lines[i - 1].strip()
                
                start_video = timestamps2[i - 1].strip().split(",")[0]
                end_video = timestamps2[i].strip().split(",")[0]
                try:
                    end_text = timestamps2[i].strip().split(",")[1]
                except:
                    end_text = None
                video_duration = get_time_difference_seconds(start_video, end_video)
                text_duration = get_time_difference_seconds(start_video, end_text) if end_text is not None else None

                while True:
                    video_clip_name = random.choice([file for file in os.listdir(background_clip_directory) if file.endswith(".mp4")])
                    video_clip_path = f"{background_clip_directory}/{video_clip_name}"
                    video_clip_duration = get_video_duration_seconds(video_clip_path)

                    if video_clip_path not in used_video_clips and video_clip_duration >= video_duration:
                        used_video_clips.append(video_clip_path)
                        break

                print(f"Creating clip {i} of {count}...")
                video = create_single_clip(
                    video_duration=video_duration,
                    video_clip_path=video_clip_path,
                    verse_text=text,
                    verse_translation=translation,
                    text_duration=text_duration,
                    shadow_color=shadow_color,
                    verse_text_color=verse_text_color,
                    verse_translation_color=verse_translation_color,
                    shadow_opacity=shadow_opacity,
                    fade_duration=fade_duration
                )
                array.append(video)

                # Update the duration
                duration += video.duration
            except:
                pass
    
    # Concatenate all the videos
    final_video = mpy.concatenate_videoclips(
        array,
        method="compose"
    ).set_audio(
        mpy.AudioFileClip(full_audio_path).subclip(timestamps2[0].strip().split(",")[0])
    ).set_duration(
        duration
    )
    final_video.write_videofile(
        output_path,
        codec="libx264", 
        audio_codec="aac"
    )

    create_notification("Video Creation Complete", "The video has been created successfully.")

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
        timeout=3
    )

if __name__ == "__main__":
    main()