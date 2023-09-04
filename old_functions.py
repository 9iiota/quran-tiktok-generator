# def speech_to_text(file_name):
#     """
#     Transcribe an audio file to text using a speech-to-text API.

#     Args:
#         file_name (str): The path to the audio file to be transcribed.

#     Returns:
#         str: The transcribed text
#     """
#     api_url = "https://api-inference.huggingface.co/models/tarteel-ai/whisper-base-ar-quran"
#     headers = {"Authorization": "Bearer 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"}

#     while True:
#         try:
#             with open(file_name, "rb") as f:
#                 data = f.read()
#             response = requests.post(api_url, headers=headers, data=data)
#             json_response = response.json()

#             # Check if the response contains the "text" key
#             if "text" in json_response:
#                 return json_response["text"]
#             else:
#                 print(f"Error: {json_response['error']}")
#         except Exception as e:
#             print(f"Error: {e}")
#         print("Retrying in 10 seconds...")
#         sleep(10)

# def get_verse_key(text):
#     """
#     Get the verse key of a verse from the Quran.

#     Args:
#         text (str): The text of the verse.

#     Returns:
#         str: The verse key of the verse.
#     """
#     response = requests.get(f"https://api.quran.com/api/v4/search?q={text}")
#     return response.json()["search"]["results"][0]["verse_key"]