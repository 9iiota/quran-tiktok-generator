import cv2
import json
import moviepy.editor as mpy
import os
import random
import requests
import subprocess
import tempfile
from bs4 import BeautifulSoup
from datetime import datetime
from pyquran import quran
from time import sleep

API_URL = "https://api-inference.huggingface.co/models/tarteel-ai/whisper-base-ar-quran"
headers = {"Authorization": "Bearer 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"}

ARABIC_FONT = "Fonts/Hafs.ttf"
ENGLISH_FONT = "Fonts/Butler_Regular.otf"

joe = [
    "0:00.000",
    "0:03.109",
    "0:12.663",
    "0:17.819",
    "0:21.551",
    "0:29.377",
    "0:34.930",
    "0:39.339",
    "0:43.669",
    "0:53.157",
    "0:59.928",
    "1:06.474",
    "1:10.931",
    "1:16.820",
    "1:22.579",
    "1:29.240",
    "1:36.121",
    "1:42.845",
    "1:52.458",
    "1:57.544",
    "2:00.442"
]

def main():
    batch_video_creation(
        timestamps=joe,
        count=11,
        full_audio_path="Audio/29 - Al-'Ankabut/Abdul Rahman Mossad - Al-'Ankabut.mp3",
        background_clip_directory="Background_Clips",
        output_path="Videos/Final.mp4"
    )

def speech_to_text(file_name):
    """
    Transcribe an audio file to text using a speech-to-text API.

    Args:
        file_name (str): The path to the audio file to be transcribed.

    Returns:
        str: The transcribed text
    """
    while True:
        try:
            with open(file_name, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            json_response = response.json()

            # Check if the response contains the "text" key
            if "text" in json_response:
                return json_response
            else:
                print(f"Error: {json_response['error']}")
        except Exception as e:
            print(f"Error: {e}")
        print("Retrying in 10 seconds...")
        sleep(10)

def get_time_difference_seconds(audio_duration, video_duration):
    """
    Calculate the time difference between two time strings in the format "MM:SS.SSS".

    Args:
        audio_duration (str): The duration of the audio clip.
        video_duration (str): The duration of the video clip.

    Returns:
        float: The time difference in seconds.
    """
    # Convert the time strings to timedelta objects
    time_format = "%M:%S.%f"
    audio_duration = datetime.strptime(audio_duration, time_format)
    video_duration = datetime.strptime(video_duration, time_format)
    
    # Calculate the time difference (subtraction)
    time_difference = video_duration - audio_duration

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

def get_verse_key(text):
    """
    Get the verse key of a verse from the Quran.

    Args:
        text (str): The text of the verse.

    Returns:
        str: The verse key of the verse.
    """
    response = requests.get(f"https://api.quran.com/api/v4/search?q={text}")
    return response.json()

def get_verse_text(verse_key):
    """
    Get the text of a verse from the Quran.

    Args:
        verse_key (str): The verse key of the verse.

    Returns:
        str: The text of the verse.
    """
    chapter, verse = map(int, verse_key.split(":"))
    return quran.get_verse(chapter, verse, with_tashkeel=True)

def get_verse_translation(verse_key):
    """
    Get the translation of a verse from the Quran.

    Args:
        verse_key (str): The verse key of the verse.

    Returns:
        str: The translation of the verse.
    """
    response = requests.get(f"https://api.quran.com/api/v4/quran/translations/20?verse_key={verse_key}")
    translation = response.json()["translations"][0]["text"]
    soup = BeautifulSoup(translation, "html.parser")
    clean_text = soup.get_text()
    return clean_text

def create_single_video(video_duration, video_clip_path, verse_text, verse_translation, shadow_opacity=0.7, fade_duration=0.5):
    """
    Create a single video with the given parameters.

    Args:
        video_duration (float): The duration of the video.
        video_clip_path (str): The path to the video clip.
        verse_text (str): The text of the verse.
        verse_translation (str): The translation of the verse.
        shadow_opacity (float, optional): The opacity of the shadow. Defaults to 0.7.
        fade_duration (float, optional): The duration of the fade in and fade out. Defaults to 0.5.

    Returns:
        moviepy.video.compositing.CompositeVideoClip: The final video.
    """
    video_clip = mpy.VideoFileClip(video_clip_path)

    # Get the offsets
    x_offset = random.randint(0, max(0, video_clip.w - 720))
    y_offset = random.randint(0, max(0, video_clip.h - 1080))

    video_clip = video_clip.set_duration(
        video_duration
    ).crop(
        x1=x_offset,
        y1=y_offset,
        x2=x_offset + 720,
        y2=y_offset + 1080
    )

    shadow_clip = mpy.ColorClip(
        size=video_clip.size, 
        color=(0, 0, 0), 
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

    tajweed_text_clip = mpy.TextClip(
        txt=verse_text,
        size=video_clip.size,
        color="white",
        bg_color="transparent",
        fontsize=45,
        font=ARABIC_FONT
    ).set_position(
        (0, -.05), relative=True
    ).set_duration(
        video_clip.duration
    ).crossfadein(
        fade_duration
    ).crossfadeout(
        fade_duration
    )

    translation_text_clip = mpy.TextClip(
        txt=verse_translation,
        size=video_clip.size,
        color="white",
        bg_color="transparent",
        fontsize=18,
        font=ENGLISH_FONT
    ).set_position(
        (0, 0), relative=True
    ).set_duration(
        video_clip.duration
    ).crossfadein(
        fade_duration
    ).crossfadeout(
        fade_duration
    )

    final_video = mpy.CompositeVideoClip(
        [
            video_with_shadow,
            tajweed_text_clip,
            translation_text_clip
        ], 
        use_bgclip=True
    ).set_fps(
        24
    )

    return final_video

def batch_video_creation(timestamps, count, full_audio_path, background_clip_directory, output_path):
    """
    Create a batch of videos with the given parameters.

    Args:
        timestamps (list): The timestamps of the verses.
        count (int): The number of clips in the final video.
        full_audio_path (str): The path to the full audio file.
        background_clip_directory (str): The path to the directory containing the background clips.
        output_path (str): The path to the output video.

    Returns:
        moviepy.video.compositing.concatenate.ConcatenatedClips: The final video.
    """
    array = []
    duration = 0
    
    # Get the Arabic text from the audio file
    arabic_text = speech_to_text(full_audio_path)

    # Get the verse key from the Arabic text
    verse_key = get_verse_key(arabic_text["text"])["search"]["results"][0]["verse_key"]
    chapter, verse = map(int, verse_key.split(":"))

    with open("arabic.txt", "w", encoding="utf-8") as arabic_file, open("english.txt", "w", encoding="utf-8"):
        pass

    with open("arabic.txt", "a", encoding="utf-8") as arabic_file, open("english.txt", "a", encoding="utf-8") as english_file:
        for i in range(1, count + 1):
            tajweed = get_verse_text(f"{chapter}:{verse + i - 1}")  # Fetch tajweed for this verse
            translation = get_verse_translation(f"{chapter}:{verse + i - 1}")  # Fetch translation for this verse

            arabic_file.write(tajweed + "\n")
            english_file.write(translation + "\n")

    input("Appropriately edit the text files now...")

    with open("arabic.txt", "r", encoding="utf-8") as arabic_file, open("english.txt", "r", encoding="utf-8") as english_file:
        arabic_lines = arabic_file.readlines()
        english_lines = english_file.readlines()
        used_video_clips = []
        for i in range(1, count + 1):
            tajweed = arabic_lines[i - 1].strip()
            translation = english_lines[i - 1].strip()
            
            time_difference_seconds = get_time_difference_seconds(timestamps[i - 1], timestamps[i])

            while True:
                video_clip_name = random.choice([file for file in os.listdir(background_clip_directory) if file.endswith(".mp4")])
                video_clip_path = f"{background_clip_directory}/{video_clip_name}"
                video_clip_duration = get_video_duration_seconds(video_clip_path)

                if video_clip_path not in used_video_clips and video_clip_duration >= time_difference_seconds:
                    used_video_clips.append(video_clip_path)
                    break

            video = create_single_video(time_difference_seconds, video_clip_path, tajweed, translation)
            array.append(video)

            # Update the duration
            duration += video.duration
    
    # Concatenate all the videos
    final_video = mpy.concatenate_videoclips(
        array,
        method="compose"
    ).set_audio(
        mpy.AudioFileClip(full_audio_path)
    ).set_duration(
        duration
    )
    final_video.write_videofile(
        output_path,
        codec="libx264", 
        audio_codec="aac"
    )

if __name__ == "__main__":
    main()