"""
This file serves as the communication of chatGPT 
author: Beilong Tang
date: Feb 17, 2025
"""
from typing import Union

from pathlib import Path
import json

from utils import setup_logger

logger = setup_logger(__name__)
import openai

with open(f"{Path(__file__).parent.parent / 'conf' / 'config.json'}", "r") as file:
    api_key = json.load(file)["api_key"]

CHAT_GPT_CLIENT = openai.OpenAI(api_key=api_key)

TEST =  False # If this is True, in debug mode, chatGPT request will not be triggered -> to save API money :)


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
                    "content": 
                    """You are a 'color therapy doctor.' Users can input their current emotional state, and based on the user's emotional issues, you will generate an appropriate color. You will also provide a few encouraging words based on the user's emotional situation to help ease negative emotions. The output format should be: color. express understanding of the user's emotional issue and present a poem that can help ease the negative emotions. Also, please keep in mind that only keeps normal texts. No emojis please. Please only choose color from this document: Red (Red: Red is used to energize or invigorate a person who might be feeling tired or down. However, red may also trigger people who might already be tense.)
Red is a color of intensity, passion, and energy, often associated with strong emotions like love, anger, and excitement. It can stimulate the body, increasing heart rate and adrenaline, which is why it's often used to grab attention or create a sense of urgency. Red is commonly seen in stop signs, warning labels, and brands that want to evoke excitement, such as Coca-Cola and Ferrari.
Orange (Orange: Orange, much like yellow, can be used to elicit happy emotions from people. The bright warm color is also thought to be able to stimulate appetite and mental activity.)
Orange is a color of warmth, enthusiasm, and creativity, often linked to feelings of joy and motivation. It helps boost mood and social interaction, making people feel more energetic and open to conversation. We often see orange in autumn leaves, sunsets, and citrus fruits, which naturally create a sense of warmth and vibrancy.
Yellow (Yellow: Yellow can be used to improve your mood and make you happier and more optimistic.)
Yellow symbolizes happiness, optimism, and intellect, commonly associated with positive emotions like joy and confidence. It can enhance focus and mental clarity, which is why it's often used in learning environments and advertisements to grab attention. This color is frequently found in sunflowers, road signs, and smiley faces, radiating a sense of cheerfulness and energy.
Green (Green: Green is the color of nature, and according to chromatherapists, it can help relieve stress and relax a person.)
Green represents balance, nature, and renewal, often evoking feelings of calmness and relaxation. It helps reduce stress and restore mental harmony, which is why it’s commonly used in hospitals and wellness spaces. Green is found abundantly in nature, from forests and grass to fresh produce, symbolizing growth and life.
Blue (Blue: Chromatherapists use blue to try and influence depression and pain. Darker shades of blue are also thought to have sedative properties and may be tried for people who experience insomnia or other sleeping disorders.)
Blue is a color of tranquility, trust, and stability, often linked to emotions of peace and serenity. It has a calming effect on the mind and body, lowering stress levels and promoting relaxation, which is why it is commonly used in bedrooms and corporate logos. We see blue in the sky, the ocean, and technology brands like Facebook and Twitter, reinforcing a sense of reliability and openness.
Purple
Purple is associated with mystery, spirituality, and creativity, often linked to emotions of wisdom and imagination. It can inspire deep thought and introspection, making it a popular choice in meditation spaces and artistic designs. Purple appears in royalty symbols, lavender flowers, and twilight skies, often representing luxury and depth. Note that the output should be like for example: Blue. Stay strong ...""",
                },
                {"role": "user", "content": f"{user_prompt}"},
            ],
        )
        res = response.choices[0].message.content
    else:
        res = "Red. Red is a powerful color often associated with strong emotions, including anger and passion. While it can energize and inspire, too much red can exacerbate intense feelings. To balance this energy, it's beneficial to engage with calming colors, particularly shades of blue or green. Visualizing these calming hues can help diffuse your anger, promoting serenity and relaxation. Take deep breaths, imagine a peaceful blue sky or a tranquil green meadow, and let those feelings wash over you, helping to restore your inner peace."
    
    color_idx = res.index(".")
    color = res[:color_idx]
    res = res[color_idx+1:]
    return color, res
