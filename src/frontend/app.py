import os 
import sys 
sys.path.append(os.path.dirname(os.getcwd()))
os.environ['HTTP_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"
os.environ['HTTPS_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"

from flask import Flask, render_template, jsonify, request, send_file


### Global Config for now ###
BACKEND_PATH= "http://127.0.0.1:8000"
# BACKEND_PATH= "http://10.200.14.51:5000" ## RedTTS
# BACKEND_PATH= "http://10.200.14.51:5009" ## Funcodec LauraGPT
TEST_AUDIO = True


## Get the get_color and content
from chatbot.chatbot import * 

app = Flask(__name__)
from utils import setup_logger
logger = setup_logger(__name__)


@app.route("/")
def main():
    logger.info("Started application. Logging works fine")
    return render_template("index.html", backend_path = BACKEND_PATH)


@app.route("/talk", methods=['POST'])
def talk():
    ## This function chats with the chatgpt box as user input messages
    user_prompt = request.form['prompt']
    color, message = get_color_and_content(user_prompt)

    logger.info(f"Detected color {color}")
    return jsonify({"response": message, "color": color})

@app.route("/wav")
def generate_audio():
    if TEST_AUDIO is True:
        return send_file('static/example_red_color.wav', mimetype='audio/wav')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
    pass
