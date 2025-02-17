import os 
from flask import Flask, render_template, jsonify, request

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

if __name__ == "__main__":
    app.run(debug=True)
    pass
