import os 
import sys 
sys.path.append(os.path.dirname(os.getcwd()))
os.environ['HTTP_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"
os.environ['HTTPS_PROXY'] = "http://proxy-dku.oit.duke.edu:3128"

from flask import Flask, request, send_file

## Get the get_color and content
app = Flask(__name__)
from utils import setup_logger
logger = setup_logger(__name__)

@app.route('/tts')
def gen_speech():
    text = request.args.get('text', '')

    logger.info(f"backend get speech text: {text[:100]}...")
    
    fake_audio_path = r"static\fileid_1.flac"

    return send_file(fake_audio_path, mimetype='audio/mpeg')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
    pass




