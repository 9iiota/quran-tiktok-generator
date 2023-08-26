import requests
import json

API_URL = "https://api-inference.huggingface.co/models/tarteel-ai/whisper-base-ar-quran"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query(r"C:\Users\Crazy\Desktop\94\_1.mp3")

def joe(text):
    response = requests.get(f"https://api.quran.com/api/v4/search?q={text}")
    return response.json()

with open("output.json", "w") as f:
    json.dump(joe(output), f, indent=4)