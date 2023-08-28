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

def get_arabic_text(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def get_verse_key(text):
    response = requests.get(f"https://api.quran.com/api/v4/search?q={text}")
    return response.json()

def get_tajweed(verse_key):
    response = requests.get(f"https://api.quran.com/api/v4/quran/verses/uthmani_tajweed?verse_key={verse_key}")
    tajweed = response.json()["verses"][0]["text_uthmani_tajweed"]
    soup = BeautifulSoup(tajweed, "html.parser")
    clean_text = soup.get_text()
    return clean_text

def get_translation(verse_key):
    response = requests.get(f"https://api.quran.com/api/v4/quran/translations/20?verse_key={verse_key}")
    translation = response.json()["translations"][0]["text"]
    soup = BeautifulSoup(translation, "html.parser")
    clean_text = soup.get_text()
    return clean_text

def main():
    arabic_text = get_arabic_text(r"C:\Users\Crazy\Desktop\94\_1.mp3")
    verse_key = get_verse_key(arabic_text["text"])["search"]["results"][0]["verse_key"]

    tajweed = get_tajweed(verse_key)
    last_space_index = tajweed.rfind(" ")  # Find the index of the last space
    tajweed = tajweed[:last_space_index]  # Extract substring up to the last space

    translation = get_translation(verse_key)

    # Create a temporary text file and open it with the default text editor
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(translation)
        temp_file_path = temp_file.name

    # Open the temporary text file with the default text editor
    subprocess.run(["notepad.exe", temp_file_path], shell=True)

    # Read the modified text from the temporary file
    with open(temp_file_path, "r", encoding="utf-8") as temp_file:
        translation = temp_file.read()

    # Print the modified text
    print(f"Translation: `{translation}`")

    # Clean up: Delete the temporary file
    os.remove(temp_file_path)

    # Load the audio clip
    audio_path = r"C:\Users\Crazy\Desktop\GitHub\quran\audio\_1.mp3"
    audio_clip = AudioFileClip(audio_path)

    # Create a shadow overlay clip
    shadow_color = (0, 0, 0)  # Black color for the shadow
    shadow_opacity = 0.5      # Opacity of the shadow (0 to 1)

    # Load the video clip
    video_path = r"C:\Users\Crazy\Desktop\GitHub\quran\video3.mp4"
    video_clip = VideoFileClip(video_path)

    # Ensure the video duration matches the audio duration
    video_duration = audio_clip.duration

    # Resize the video to match the audio duration
    video_clip = video_clip.set_duration(video_duration)

    # Create a shadow overlay clip
    shadow_clip = ColorClip(size=video_clip.size, color=shadow_color, duration=video_clip.duration)
    shadow_clip = shadow_clip.set_opacity(shadow_opacity)

    # Create a white text clip
    top_text = f"{tajweed}"
    top_txt_clip = TextClip(
        top_text,
        fontsize=40,
        color='white',
        size=video_clip.size,
        bg_color='transparent',  # Set background to transparent
        method='caption'
    )

    bottom_text = f"\n\n\n\n{translation}"
    bottom_txt_clip = TextClip(
        bottom_text,
        fontsize=20,
        color='white',
        size=video_clip.size,
        bg_color='transparent',  # Set background to transparent
        method='caption'
    )

    # Set the duration for the text overlay
    top_txt_clip = top_txt_clip.set_duration(video_clip.duration)
    bottom_txt_clip = bottom_txt_clip.set_duration(video_clip.duration)

    # Apply fade-in and fade-out to the text
    fade_duration = .5  # Duration of the fade effect in seconds
    top_txt_clip = top_txt_clip.crossfadein(fade_duration).crossfadeout(fade_duration)
    bottom_txt_clip = bottom_txt_clip.crossfadein(fade_duration).crossfadeout(fade_duration)

    # Overlay the shadow and video clips
    video_with_shadow = CompositeVideoClip([video_clip.set_position('center'), shadow_clip.set_position('center')])

    # Overlay the text on the video with shadow
    video_with_text_and_shadow = CompositeVideoClip([video_with_shadow, top_txt_clip.set_position('center')])
    video_with_text_and_shadow = CompositeVideoClip([video_with_text_and_shadow, bottom_txt_clip.set_position('bottom')])

    # Set the audio of the video
    video_with_audio = video_with_text_and_shadow.set_audio(audio_clip)

    # Write the final video with shadow, text overlay, and audio
    output_path = "output_video_with_all.mp4"
    video_with_audio.write_videofile(output_path, codec='libx264')

if __name__ == "__main__":
    main()