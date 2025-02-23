from flask import Flask, Response, jsonify, render_template, request, send_file
import os 
import sys 
import tempfile
import time 
from flask_cors import CORS

sys.path.append(os.path.dirname(os.getcwd()))
from utils import setup_logger
logger = setup_logger(__name__)
import argparse

p = argparse.ArgumentParser()
p.add_argument("--port", type=int, required=True)
p.add_argument("--device", type=str, required=True)
args = p.parse_args()
os.environ['CUDA_VISIBLE_DEVICES'] = args.device

logger.info(f"[Port {args.port}] is intializing Funcodec Model")

from model.funcodec import Text2AudioWrapper
import json
with open("/DKUdata/tangbl/FunCodec/FunCodec/egs/LibriTTS/text2speech_laura/infer_default.json", "r") as file:
    kwargs = json.load(file)
text2audio = Text2AudioWrapper(**kwargs)

app = Flask("LauraGPT Compute Node")
CORS(app)

@app.route("/generate_prompt")
def generate_prompt():
    text = request.args.get("text")
    prompt_path = request.args.get("prompt")
    text2audio.change_prompt_audio_and_text(prompt_path, text)
    return jsonify({"status": "success"})


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
    logger.info(f"[NODE {args.port}]Get audio path {audio_path}")
    # return send_file(audio_path, mimetype='audio/wav')
    return jsonify({"audio_path": audio_path})
    # return Response(generate(text), mimetype="audio/wav")  # ✅ Correct MIME type for audio

if __name__ == "__main__":
    app.run(port=args.port)


