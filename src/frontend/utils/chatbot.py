"""
This file serves as the communication of chatGPT 
author: Beilong Tang
date: Feb 17, 2025
"""
from typing import Union

from pathlib import Path
import json
from utils.logger import setup_logger

logger = setup_logger(__name__)
import openai

with open(f"{Path(__file__).parent.parent / 'conf' / 'config.json'}", "r") as file:
    api_key = json.load(file)["api_key"]

CHAT_GPT_CLIENT = openai.OpenAI(api_key=api_key)

TEST = True # If this is True, in debug mode, chatGPT request will not be triggered -> to save API money :)


def get_color_and_content(user_prompt: str) -> Union[str, str]:
    """
    This function is called to identify the color of user prompt
    """
    logger.info(f"processing the request")
    if TEST is not True:
        response = CHAT_GPT_CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer",
                    "content": "You are a color therapy doctor. Based on the user input, please identify a color for him/her. And also a color therapy texts for a 30 to 60 seconds. The output format should be 'color. ....' For example: Blue. Blue is a calming color ....",
                },
                {"role": "user", "content": f"{user_prompt}"},
            ],
        )
        res = response.choices[0].message.content
    else:
        res = "Red. Red is a powerful color often associated with strong emotions, including anger and passion. While it can energize and inspire, too much red can exacerbate intense feelings. To balance this energy, it's beneficial to engage with calming colors, particularly shades of blue or green. Visualizing these calming hues can help diffuse your anger, promoting serenity and relaxation. Take deep breaths, imagine a peaceful blue sky or a tranquil green meadow, and let those feelings wash over you, helping to restore your inner peace."

    color = res.split(".")[0]
    return color, res
