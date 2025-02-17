import os

import json 

with open("config.json", "r") as file: 
    api_key = json.load(file)['api_key']
    pass


# os.environ['OPENAI_API_KEY'] = 
os.environ['HTTP_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"
os.environ['HTTPS_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"
from openai import OpenAI

client = OpenAI(
    api_key=api_key  # This is the default and can be omitted
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say I love JieNI Bai with a romantic story",
#         }
#     ],
#     model="gpt-4o",
# )
# msg = chat_completion.choices[0].message
# print(msg)

# from openai import OpenAI
#
# client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Give me a Color"}],
    stream=True,
)
for chunk in stream:
    if chunk.choice:
        print(chunk.choices[0].delta.content, end="")
