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
        full_audio_name="Abdul Rahman Mossad - Al-'Ankabut.mp3",
        count=11,
        audio_clip_directory="Audio/29 - Al-'Ankabut",
        background_clip_directory="Background_Clips",
        output_path="Videos/Final2.mp4"
    )

def speech_to_text(file_name):
    """
    Transcribe an audio file to text using a speech-to-text API.

    Args:
        file_name (str): The path to the audio file to be transcribed.

    Returns:
        str or None: The transcribed text if successful, or None on failure.
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

def get_verse_key(text):
    response = requests.get(f"https://api.quran.com/api/v4/search?q={text}")
    return response.json()

def get_verse_text(verse_key):
    chapter, verse = map(int, verse_key.split(":"))
    return quran.get_verse(chapter, verse, with_tashkeel=True)

def edit_tajweed(tajweed):
    # Create a temporary text file and open it with the default text editor
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(tajweed)
        temp_file_path = temp_file.name

    # Open the temporary text file with the default text editor
    subprocess.run(["notepad.exe", temp_file_path], shell=True)

    # Read the modified text from the temporary file
    with open(temp_file_path, "r", encoding="utf-8") as temp_file:
        tajweed = temp_file.read()

    # Clean up: Delete the temporary file
    os.remove(temp_file_path)

    return tajweed

def get_verse_translation(verse_key):
    response = requests.get(f"https://api.quran.com/api/v4/quran/translations/20?verse_key={verse_key}")
    translation = response.json()["translations"][0]["text"]
    soup = BeautifulSoup(translation, "html.parser")
    clean_text = soup.get_text()
    return clean_text

def edit_translation(translation):
    # Create a temporary text file and open it with the default text editor
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(translation)
        temp_file_path = temp_file.name

    # Open the temporary text file with the default text editor
    subprocess.run(["notepad.exe", temp_file_path], shell=True)

    # Read the modified text from the temporary file
    with open(temp_file_path, "r", encoding="utf-8") as temp_file:
        translation = temp_file.read()

    # Clean up: Delete the temporary file
    os.remove(temp_file_path)

    return translation

def create_single_video(video_duration, video_clip_path, tajweed, translation, shadow_opacity=0.7, fade_duration=0.5):
    video_clip = mpy.VideoFileClip(video_clip_path)

    # Get the offsets
    x_offset = random.randint(0, max(0, video_clip.w - 720))
    y_offset = random.randint(0, max(0, video_clip.h - 1080))

    video_clip = video_clip.set_duration(
        video_duration
    ).crop(
        x1=x_offset,
        y1=y_offset,
        x2=x_offset+720,
        y2=y_offset+1080
    )

    shadow_clip = mpy.ColorClip(
        size=video_clip.size, 
        color=(0, 0, 0), 
        duration=video_clip.duration
    ).set_opacity(
        shadow_opacity
    )

    video_with_shadow = mpy.CompositeVideoClip(
        [video_clip, shadow_clip], 
        use_bgclip=True
    )

    tajweed_text_clip = mpy.TextClip(
        txt=tajweed,
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
        txt=translation,
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
        [video_with_shadow, tajweed_text_clip, translation_text_clip], 
        use_bgclip=True
    ).set_fps(
        24
    )

    return final_video

def batch_video_creation(timestamps, full_audio_name, count, audio_clip_directory, background_clip_directory, output_path):
    array = []
    duration = 0
    
    # Get the Arabic text from the audio file
    arabic_text = speech_to_text(f"{audio_clip_directory}/{full_audio_name}")

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
        for i in range(1, count + 1):
            tajweed = arabic_lines[i - 1].strip()
            translation = english_lines[i - 1].strip()
            
            # Get the start and end times
            start_time = timestamps[i - 1]
            end_time = timestamps[i]

            # Convert the time strings to timedelta objects
            time_format = "%M:%S.%f"  # Define the format of the time strings
            time1 = datetime.strptime(start_time, time_format)
            time2 = datetime.strptime(end_time, time_format)

            # Calculate the time difference (subtraction)
            time_difference = time2 - time1

            # Convert the time difference to seconds as a float
            time_difference_seconds = time_difference.total_seconds()

            while True:
                video_clip_name = random.choice([file for file in os.listdir(background_clip_directory) if file.endswith(".mp4")])
                video_clip_path = f"{background_clip_directory}/{video_clip_name}"

                video_clip = cv2.VideoCapture(video_clip_path)
                video_clip_duration = video_clip.get(cv2.CAP_PROP_FRAME_COUNT) / video_clip.get(cv2.CAP_PROP_FPS)

                if video_clip_duration >= time_difference_seconds:
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
        mpy.AudioFileClip(f"{audio_clip_directory}/{full_audio_name}")
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