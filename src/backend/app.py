import os 
import sys 
sys.path.append(os.path.dirname(os.getcwd()))
os.environ['HTTP_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"
os.environ['HTTPS_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"

from flask import Flask, request, send_file
from flask_cors import CORS

## Get the get_color and content
app = Flask(__name__)
from utils import setup_logger
logger = setup_logger(__name__)

###
### Note that this file serves as the testing purpose
###
logger.info("Backend server started normal")

wav_list = ['static/prompt_1.wav', 'static/example_red_color.wav']
idx = 1
CORS(app)

@app.route('/wav')
def gen_speech():
    global idx
    text = request.args.get('text', '')

    logger.info(f"backend get speech text: {text[:100]}...")
    
    fake_audio_path = wav_list[idx]
    idx+=1
    idx = idx % len(wav_list)
    print(idx)

    return send_file(fake_audio_path, mimetype='audio/wav')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    pass




