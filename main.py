from bs4 import BeautifulSoup
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.all import crop
from moviepy.editor import *
import requests
import json
import tempfile
import subprocess

API_URL = "https://api-inference.huggingface.co/models/tarteel-ai/whisper-base-ar-quran"
headers = {"Authorization": "Bearer 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"}

AUDIO_CLIP_PATH = r"C:\Users\Crazy\Desktop\GitHub\quran\audio\_1.mp3"
VIDEO_CLIP_PATH = r"C:\Users\Crazy\Desktop\GitHub\quran\clips\Koe no Katachi (95).mp4"

def main():
    # Get the Arabic text from the audio file
    arabic_text = speech_to_text(AUDIO_CLIP_PATH)

    # Get the verse key from the Arabic text
    verse_key = get_verse_key(arabic_text["text"])["search"]["results"][0]["verse_key"]

    # Get the tajweed of the verse
    tajweed = get_tajweed(verse_key)

    # Remove the verse number from the tajweed
    last_space_index = tajweed.rfind(" ")  # Find the index of the last space
    tajweed = tajweed[:last_space_index]  # Extract substring up to the last space

    # Get the translation of the verse
    translation = get_english_translation(verse_key)

    # Possibly edit the translation
    translation = edit_translation(translation)
    print(f"Translation: `{translation}`")

    # Create the video
    create_video(AUDIO_CLIP_PATH, VIDEO_CLIP_PATH, tajweed, translation, "final.mp4")

def speech_to_text(filename):
    try:
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")

def get_verse_key(text):
    response = requests.get(f"https://api.quran.com/api/v4/search?q={text}")
    return response.json()

def get_tajweed(verse_key):
    response = requests.get(f"https://api.quran.com/api/v4/quran/verses/uthmani_tajweed?verse_key={verse_key}")
    tajweed = response.json()["verses"][0]["text_uthmani_tajweed"]
    soup = BeautifulSoup(tajweed, "html.parser")
    clean_text = soup.get_text()
    return clean_text

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

def create_video(audio_clip_path, video_clip_path, tajweed, translation, output_path, shadow_opacity = 0.7, fade_duration = 0.5):
    # Load the audio and video clip
    audio_clip = AudioFileClip(audio_clip_path)
    video_clip = VideoFileClip(video_clip_path)

    # Resize the video to match the audio duration
    video_clip = video_clip.set_duration(audio_clip.duration)

    # Crop the video to keep only the left side
    cropped_video_clip = video_clip.crop(x1=0, x2=video_clip.h * .5625)

    # Create a shadow overlay clip for the cropped video
    shadow_color = (0, 0, 0)  # Black color for the shadow
    shadow_opacity = 0.7      # Opacity of the shadow (0 to 1)

    shadow_clip = ColorClip(size=cropped_video_clip.size, color=shadow_color, duration=cropped_video_clip.duration)
    shadow_clip = shadow_clip.set_opacity(shadow_opacity)

    # Create the top text
    top_text = tajweed
    top_text_clip = TextClip(
        top_text,
        fontsize=40,
        color='white',
        size=cropped_video_clip.size,
        bg_color='transparent',  # Set background to transparent
        method='caption'
    )

    # Create the bottom text
    bottom_text = f"\n\n\n\n{translation}"
    bottom_text_clip = TextClip(
        bottom_text,
        fontsize=20,
        color='white',
        size=cropped_video_clip.size,
        bg_color='transparent',  # Set background to transparent
        method='caption'
    )

    # Set the duration for the text overlay
    text_duration = cropped_video_clip.duration

    top_text_clip = top_text_clip.set_duration(text_duration)
    bottom_text_clip = bottom_text_clip.set_duration(text_duration)

    # Apply fade-in and fade-out to the text
    fade_duration = 0.5  # Duration of the fade effect in seconds

    top_text_clip = top_text_clip.crossfadein(fade_duration).crossfadeout(fade_duration)
    bottom_text_clip = bottom_text_clip.crossfadein(fade_duration).crossfadeout(fade_duration)

    # Overlay the shadow over the cropped video clip
    video_with_shadow = CompositeVideoClip([cropped_video_clip.set_position('center'), shadow_clip.set_position('center')])

    # Overlay the text on the cropped video clip with shadow
    video_with_text_and_shadow = CompositeVideoClip([video_with_shadow, top_text_clip.set_position('center')])
    video_with_text_and_shadow = CompositeVideoClip([video_with_text_and_shadow, bottom_text_clip.set_position('bottom')])

    # Set the audio of the video
    video_with_audio = video_with_text_and_shadow.set_audio(audio_clip)

    # Create the final video with shadow, text overlay, and audio
    output_path = output_path
    video_with_audio.write_videofile(output_path, codec='libx264')

if __name__ == "__main__":
    main()