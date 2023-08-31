import moviepy.editor as mpy
import os
import random
import requests
import subprocess
import tempfile
from bs4 import BeautifulSoup
from enum import Enum

API_URL = "https://api-inference.huggingface.co/models/tarteel-ai/whisper-base-ar-quran"
headers = {"Authorization": "Bearer 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"}

ARABIC_FONT = "Fonts/Hafs.ttf"
ENGLISH_FONT = "Fonts/Butler_Regular.otf"

class OFFSETS(Enum):
    LEFT = 0
    MIDDLE = 420
    RIGHT = 840
OFFSET = OFFSETS.LEFT.value

def main():
    name = "29 - Al-'Ankabut"
    for i in range(1,4):
        audio_clip_path = f"Audio/{name}/{i}.mp3"
        video_clip_name = random.choice([file for file in os.listdir("Background_Clips") if file.endswith(".mp4")])
        video_clip_path = f"Background_Clips/{video_clip_name}"
        video_file_name = f"Videos/{name}_{i}.mp4"
        batch_video_creation(audio_clip_path, video_clip_path, video_file_name)

def speech_to_text(filename):
    try:
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        json_response = response.json()

        # Check if the response contains the "text" key
        if "text" in json_response:
            return json_response
        else:
            print(f"Error: {json_response['error']}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_verse_key(text):
    response = requests.get(f"https://api.quran.com/api/v4/search?q={text}")
    return response.json()

def get_tajweed(verse_key):
    response = requests.get(f"https://api.quran.com/api/v4/quran/verses/uthmani_tajweed?verse_key={verse_key}")
    tajweed = response.json()["verses"][0]["text_uthmani_tajweed"]
    soup = BeautifulSoup(tajweed, "html.parser")
    clean_text = soup.get_text()
    return clean_text

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

def get_english_translation(verse_key):
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

def create_single_video(audio_clip_path, video_clip_path, tajweed, translation, output_path, shadow_opacity=0.7, fade_duration=0.5):
    audio_clip = mpy.AudioFileClip(audio_clip_path)
    video_clip = mpy.VideoFileClip(video_clip_path)
    video_clip = video_clip.set_duration(
        audio_clip.duration
    ).crop(
        x1=OFFSET, 
        x2=OFFSET + video_clip.h * .5625
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

    shadow_video_with_tajweed_and_translation = mpy.CompositeVideoClip(
        [video_with_shadow, tajweed_text_clip, translation_text_clip], 
        use_bgclip=True
    )

    final_video_with_audio = shadow_video_with_tajweed_and_translation.set_audio(audio_clip)

    final_video_with_audio.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac", 
    )

def batch_video_creation(audio_clip_path, video_clip_path, video_file_name):
    # Get the Arabic text from the audio file
    while True:
        arabic_text = speech_to_text(audio_clip_path)
        if arabic_text is not None:
            break

    # Get the verse key from the Arabic text
    verse_key = get_verse_key(arabic_text["text"])["search"]["results"][0]["verse_key"]

    # Get the tajweed of the verse
    tajweed = get_tajweed(verse_key)

    # Possibly edit the tajweed
    tajweed = edit_tajweed(tajweed)
    print(f"Tajweed: `{tajweed}`")

    # Get the translation of the verse
    translation = get_english_translation(verse_key)

    # Possibly edit the translation
    translation = edit_translation(translation)
    print(f"Translation: `{translation}`")

    # Create the video
    create_single_video(audio_clip_path, video_clip_path, tajweed, translation, video_file_name)

if __name__ == "__main__":
    main()