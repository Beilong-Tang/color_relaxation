from flask import Flask, Response, jsonify, render_template, request, send_file
import os 
import sys 
import tempfile
import torchaudio
import time 
from flask_cors import CORS

sys.path.append(os.path.dirname(os.getcwd()))
from utils import setup_logger
logger = setup_logger(__name__)

DEVICE="cuda"
os.environ['CUDA_VISIBLE_DEVICES'] = '5'

logger.info("Inializeing Funcodec Model")

from model.funcodec import Text2AudioWrapper
import json
with open("/DKUdata/tangbl/FunCodec/FunCodec/egs/LibriTTS/text2speech_laura/infer_default.json", "r") as file:
    kwargs = json.load(file)
text2audio = Text2AudioWrapper(**kwargs)

app = Flask("LauraGPT Model")
CORS(app)

# Simulating audio generation
@app.route('/wav')
def generate_sim():
    text = request.args.get("text", "") # ✅ Capture text before the generator starts
    if text == "":
        return Response(jsonify({"status": "error"}))

    def generate(text):
        logger.info(f"Get Text {text}")
        logger.info("Synthesizeing audio")
        start_time = time.time()
        audio_path = None
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_path = temp_file.name
            text2audio(text, audio_path)
        logger.info(f"laura gpt infer time {time.time() - start_time}")
        start_time = time.time()
        return audio_path
    audio_path = generate(text)
    logger.info(f"Get audio path {audio_path}")
    return send_file(audio_path, mimetype='audio/wav')
    # return Response(generate(text), mimetype="audio/wav")  # ✅ Correct MIME type for audio

@app.route("/")
def index():
    """Audio streaming homepage."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


