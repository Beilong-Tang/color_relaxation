from pathlib import Path
from openai import OpenAI
import json 
import os
import time
with open("config.json", "r") as file: 
    api_key = json.load(file)['api_key']
    pass

# os.environ['OPENAI_API_KEY'] = 
os.environ['HTTP_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"
os.environ['HTTPS_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"

with open(f"config.json", 'r') as file:
    key = json.load(file)['api_key']

client = OpenAI(api_key= key)
speech_file_path = Path(__file__).parent / "speech.wav"

print(f"begin inferencing")
start = time.time()
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Red. Red is a powerful color often associated with strong emotions, including anger and passion. While it can energize and inspire, too much red can exacerbate intense feelings. To balance this energy, it's beneficial to engage with calming colors, particularly shades of blue or green. Visualizing these calming hues can help diffuse your anger, promoting serenity and relaxation. Take deep breaths, imagine a peaceful blue sky or a tranquil green meadow, and let those feelings wash over you, helping to restore your inner peace.",
)
print(f"finished in {time.time() - start}")
response.stream_to_file(speech_file_path)
