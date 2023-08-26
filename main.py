from bs4 import BeautifulSoup
import requests
import json

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

arabic_text = get_arabic_text(r"C:\Users\Crazy\Desktop\94\_1.mp3")

verse_key = get_verse_key(arabic_text["text"])["search"]["results"][0]["verse_key"]

tajweed = get_tajweed(verse_key)
translation = get_translation(verse_key)

print(tajweed)
print(translation)