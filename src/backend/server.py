from flask import Flask, Response, jsonify, render_template, request
import os 
import sys 
import tempfile
import torchaudio
import soundfile as sf
import time 
sys.path.append(os.path.dirname(os.getcwd()))
from utils import setup_logger
logger = setup_logger(__name__)

DEVICE="cuda"
os.environ['CUDA_VISIBLE_DEVICES'] = '4'

logger.info("Inializeing Model, this can take 30mins")

from fireredtts.fireredtts import FireRedTTS

tts = FireRedTTS(
    config_path="/DKUdata/tangbl/tts/FireRedTTS/configs/config_24k.json",
    pretrained_path="/DKUdata/tangbl/tts/FireRedTTS/pretrained_models",
    device=DEVICE
)
rec_wav = tts.synthesize(
    prompt_wav="static/prompt_1.wav",
        text="Hello World",
        lang="en",
)
logger.info("Model intialized perfectly")

app = Flask("Backend Server")

# Simulating audio generation
@app.route('/wav')
def generate_sim():
    text = request.args.get("text", "") # ✅ Capture text before the generator starts
    if text == "":
        return Response(jsonify({"status": "error"}))

    def generate(text):
        logger.info(f"Get Text {text}")
        print("Synthesizeing audio")
        audio_sim = tts.synthesize_split(
            prompt_wav = "static/prompt_1.wav",
            text=text,
            lang="en" ## Support english for now
        )
        
        start_time = time.time()
        for audio in audio_sim:
            # audio_path = "speech.wav"
            audio_path = None
            logger.info(f"audio shape {audio.shape}")
            logger.info(f"infer time {time.time() - start_time}")
            start_time = time.time()
            # sf.write(audio_path, audio, samplerate= 24000)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                torchaudio.save(temp_file.name, audio, samplerate= 24000)
                audio_path = temp_file.name
            with open(audio_path, "rb") as fwav:
                # chunk_size = 10 * 24000 * 2 * 2  # 5 sec * 24kHz * 2 channels * 16-bit (2 bytes per sample)
                data = fwav.read()
                if not data:
                    break  # End of file
                yield data
    return Response(generate(text), mimetype="audio/wav")  # ✅ Correct MIME type for audio

@app.route("/")
def index():
    """Audio streaming homepage."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

