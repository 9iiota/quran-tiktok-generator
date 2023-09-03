import asyncio
import cv2
import moviepy.editor as mpy
import os
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from plyer import notification
from pyquran import quran
from time import sleep

API_URL = "https://api-inference.huggingface.co/models/tarteel-ai/whisper-base-ar-quran"
headers = {"Authorization": "Bearer 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"}

ARABIC_FONT = "Fonts/Hafs.ttf"
ENGLISH_FONT = "Fonts/Butler_Regular.otf"

def main():
    create_video(
        timestamps_csv_file_path=r"Audio\101 - Al-Qari'ah\Markers.csv",
        timestamps_output_path=r"Audio\101 - Al-Qari'ah\timestamps.txt",
        count=11,
        full_audio_path=r"Audio\101 - Al-Qari'ah\Salim Bahanan - Al-Qari'ah.mp3",
        background_clip_directory="Background_Clips",
        output_path="Videos/Salim Bahanan - Al-Qari'ah.mp4"
    )
    # create_video(
    #     timestamps_csv_file_path="Markers.csv",
    #     timestamps_txt_file_path="timestamps.txt",
    #     count=20,
    #     full_audio_path="Audio/29 - Al-'Ankabut/Abdul Rahman Mossad - Al-'Ankabut.mp3",
    #     background_clip_directory="Background_Clips",
    #     output_path="Videos/Final6.mp4",
    #     arabic_file_path="verse_text.txt",
    #     english_file_path="verse_translation.txt"
    # )

def get_timestamps(timestamps_file_path, output_file_path):
    """
    Get the timestamps from the timestamps file.

    Args:
        timestamps_file_path (str): The path to the timestamps file.
        output_file_path (str): The path to the output file.
    """
    with open(timestamps_file_path, "r", encoding="utf-8") as timestamps_file:
        lines = timestamps_file.readlines()[1:]
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
                return json_response["text"]
            else:
                print(f"Error: {json_response['error']}")
        except Exception as e:
            print(f"Error: {e}")
        print("Retrying in 10 seconds...")
        sleep(10)

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

def get_verse_key(text):
    """
    Get the verse key of a verse from the Quran.

    Args:
        text (str): The text of the verse.

    Returns:
        str: The verse key of the verse.
    """
    response = requests.get(f"https://api.quran.com/api/v4/search?q={text}")
    return response.json()["search"]["results"][0]["verse_key"]

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

def create_single_clip(video_duration, video_clip_path, verse_text, verse_translation, text_duration=None, shadow_opacity=0.7, fade_duration=0.5):
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

    Returns:
        moviepy.video.compositing.CompositeVideoClip: The final clip.
    """
    print(f"Video duration: {video_duration}\tVideo clip path: {video_clip_path}\tVerse text: {verse_text}\tVerse translation: {verse_translation}\tText duration: {text_duration}\tShadow opacity: {shadow_opacity}\tFade duration: {fade_duration}")
    text_duration = video_duration if text_duration is None else text_duration
    
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
        text_duration
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
        text_duration
    ).crossfadein(
        fade_duration
    ).crossfadeout(
        fade_duration
    )

    final_clip = mpy.CompositeVideoClip(
        [
            video_with_shadow,
            tajweed_text_clip,
            translation_text_clip
        ], 
        use_bgclip=True
    ).set_duration(
        video_duration
    ).set_fps(
        24
    )

    return final_clip

def create_video(timestamps_csv_file_path, timestamps_output_path, count, full_audio_path, background_clip_directory, output_path):
    """
    Create a video with the given parameters.

    Args:
        timestamps_csv_file_path (str): The path to the timestamps CSV file.
        timestamps_txt_file_path (str): The path to the timestamps TXT file.
        count (int): The number of clips in the final video.
        full_audio_path (str): The path to the full audio file.
        background_clip_directory (str): The path to the directory containing the background clips.
        output_path (str): The path to the output video.
    """
    array = []
    duration = 0
    
    # Get the timestamps from the timestamps file
    get_timestamps(timestamps_csv_file_path, timestamps_output_path)

    # Get the Arabic text from the audio file
    # arabic_text = speech_to_text(full_audio_path)

    # Get the verse key from the Arabic text
    verse_key = "101:1" # get_verse_key(arabic_text)
    chapter, verse = map(int, verse_key.split(":"))

    with open("verse_text.txt", "w", encoding="utf-8") as arabic_file, open("verse_translation.txt", "w", encoding="utf-8"):
        pass

    with open("verse_text.txt", "a", encoding="utf-8") as arabic_file, open("verse_translation.txt", "a", encoding="utf-8") as english_file:
        for i in range(1, count + 1):
            try:
                tajweed = get_verse_text(f"{chapter}:{verse + i - 1}")  # Fetch tajweed for this verse
                arabic_file.write(tajweed + "\n")

                translation = get_verse_translation(f"{chapter}:{verse + i - 1}")  # Fetch translation for this verse\
                english_file.write(translation + "\n")
            except:
                pass

    input("Appropriately edit the text files now...")

    with open("verse_text.txt", "r", encoding="utf-8") as arabic_file, \
        open("verse_translation.txt", "r", encoding="utf-8") as english_file, \
        open(timestamps_output_path, "r", encoding="utf-8") as timestamps_file:
        arabic_lines = arabic_file.readlines()
        english_lines = english_file.readlines()
        timestamps2 = timestamps_file.readlines()
        used_video_clips = []
        for i in range(1, count + 1):
            tajweed = arabic_lines[i - 1].strip()
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

            video = create_single_clip(video_duration, video_clip_path, tajweed, translation, text_duration)
            array.append(video)

            # Update the duration
            duration += video.duration
    
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

# def get_sentence_not_working(full_audio_path, start_time, end_time):
#     # Load the full audio file
#     audio = AudioSegment.from_mp3(full_audio_path)

#     # # Extract the desired segment
#     start_time = start_time.replace(":", "").replace(".", "")
#     end_time = end_time.replace(":", "").replace(".", "")
#     audio_segment = audio[int(start_time):int(end_time)]

#     # Export the segment as a temporary MP3 file
#     temp_mp3_file = "temp.mp3"
#     audio_segment.export(temp_mp3_file, format="mp3")
#     speechtotext = speech_to_text(temp_mp3_file)

#     # Clean up the temporary WAV file
#     if os.path.exists(temp_mp3_file):
#         os.remove(temp_mp3_file)

#     verse_key = get_verse_key(speechtotext)
#     pyquran = get_verse_text(verse_key)

#     jart = []
#     for i in range(len(pyquran)):
#         for j in range(i, len(pyquran)):
#             sentence = pyquran[i:j]
#             # Create a CountVectorizer to convert sentences to vectors
#             vectorizer = CountVectorizer().fit_transform([speechtotext, sentence])

#             # Calculate the cosine similarity between the two sentences
#             cosine_sim = cosine_similarity(vectorizer)

#             # Calculate the Jaccard similarity between the two sentences
#             jaccard_sim = textdistance.algorithms.jaccard(speechtotext, sentence)

#             jart.append((cosine_sim[0][1], jaccard_sim, sentence, speechtotext))
#     jart.sort(key=lambda x: x[0], reverse=True)

#     deeetz = [item for item in jart if item[0] == jart[0][0]]
#     deeetz.sort(key=lambda x: x[1], reverse=True)

#     best = deeetz[0][2]

#     return best

if __name__ == "__main__":
    main()