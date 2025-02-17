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


def get_color_and_content(user_prompt: str) -> Union[str, str]:
    """
    This function is called to identify the color of user prompt
    """
    logger.info(f"processing the request")
    response= CHAT_GPT_CLIENT.chat.completions.create(
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

    color = res.split('.')[0]
    return color, res
