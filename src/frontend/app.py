import os 
from flask import Flask, render_template, jsonify, request, send_file

os.environ['HTTP_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"
os.environ['HTTPS_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"


## Get the get_color and content
from utils.chatbot import * 

app = Flask(__name__)

from utils.logger import setup_logger
logger = setup_logger(__name__)

@app.route("/")
def main():
    logger.info("Started application. Logging works fine")
    return render_template("index.html")



@app.route("/talk", methods=['POST'])
def talk():
    ## This function chats with the chatgpt box as user input messages
    user_prompt = request.form['prompt']
    color, message = get_color_and_content(user_prompt)

    logger.info(f"Detected color {color}")
    return jsonify({"response": message})


@app.route('/generate_speech')
def gen_speech():
    text = request.args.get('text', '')

    logger.info(f"Gen Speech get text: {text[:100]}...")
    
    fake_audio_path = r"D:\Main\DKU\Senior\SOSC110\color_system\src\server\static\fileid_1.flac"

    

    return send_file(fake_audio_path, mimetype='audio/mpeg')

if __name__ == "__main__":
    app.run(debug=True)
    pass
