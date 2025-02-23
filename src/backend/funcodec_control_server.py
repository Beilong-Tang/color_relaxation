from flask import Flask, Response, jsonify, render_template, request, send_file
import os
import sys
import tempfile
import time
from flask_cors import CORS
import nltk
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import tempfile
import soundfile as sf 
import requests

sys.path.append(os.path.dirname(os.getcwd()))
from utils import setup_logger

logger = setup_logger(__name__)

app = Flask("LauraGPT Control Mode")
CORS(app)

import argparse

p = argparse.ArgumentParser()
p.add_argument("--port", type=int, required=True)
p.add_argument("--compute_ports", nargs="+", required=True)
args = p.parse_args()

logger.info(f"Backend ports: {args.compute_ports}")

@app.route('/prompt_upload', methods=['POST'])
def upload_prompt():

    def _send_request(params):
        """
        This function informs other nodes to update the prompt audio 
        """
        file_path, text, node = params
        
        url = f"http://127.0.0.1:{node}/generate_prompt"
        _params = {"text": text, "prompt": file_path}
        res = requests.get(url, params = _params)
        res = res.json()
        if "status" in res:
            return {"status": "success"}
        return {"failure": "failure"}

    if 'file' not in request.files:
        return jsonify({'message': 'No file part', 'success': False}), 400
    file = request.files['file']
    text = request.form.get("text")
    if text is None:
        return jsonify({'message': 'No text found', 'success': False}), 400
    if file.filename == '':
        return jsonify({'message': 'No selected file', 'success': False}), 400
    if file and file.filename.endswith('.wav'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            path = temp_file.name
        file.save(path)
        compute_ports = args.compute_ports
        ## Notify the compute nodes to update speaker prompt
        with ThreadPoolExecutor(max_workers=len(compute_ports)) as executor:
            results = list(
                executor.map(
                    _send_request,
                    [(path, text, node) for node in compute_ports],
                )
            )
        for _r in results:
            if "failure" in _r:
                return jsonify({'message': 'Compute nodes failed', 'success': False}), 400
        return jsonify({'message': 'success', 'success': True}), 200
    return jsonify({'message': 'Invalid file type', 'success': False}), 400


# Simulating audio generation
@app.route("/wav")
def generate_sim():
    text = request.args.get("text", "")  # ✅ Capture text before the generator starts
    if text == "":
        return Response(jsonify({"status": "error"}))

    def generate(text):
        def _split_text_chunk(sentences, length):
            chunks = np.array_split(sentences, length)
            chunks = [
                list(chunk) for chunk in chunks if list(chunk) != []
            ]  # [[str1, str2], [str3, str4], [str4]]
            res = [" ".join(_c) for _c in chunks]
            return res

        def _send_request(params):
            sentence, node, id = params

            url = f"http://127.0.0.1:{node}/wav"
            params = {"text": sentence}
            response = requests.get(url, params=params)  # Do the computation
            json_data = response.json()
            audio_path = json_data["audio_path"]
            return {"audio_path": audio_path, "id": id}

        compute_ports = args.compute_ports
        logger.info(f"[Control Node] Get Text {text}")
        start_time = time.time()
        audio_path = None
        sentences = nltk.tokenize.sent_tokenize(text)
        sentence_list = _split_text_chunk(
            sentences, len(compute_ports)
        )  # [sent1, sent2, ...]
        logger.info(f"sentence list: {sentence_list}")

        with ThreadPoolExecutor(max_workers=len(compute_ports)) as executor:
            results = list(
                executor.map(
                    _send_request,
                    [(sentence_list[i], node, i) for i, node in enumerate(compute_ports)],
                )
            )
        results = sorted(results, key=lambda x: x['id']) ## Sort them according to id
        
        audio_path_list = [ r['audio_path'] for r in results ]

        ## Concatenate them in a audio path
        res = []
        for _audio_path in audio_path_list:
            audio, _ = sf.read(_audio_path)
            res.append(audio)
        res = np.concatenate(res, axis = 0)

        audio_path = None
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            audio_path = temp_file.name
            sf.write(audio_path, res, samplerate=16000)
        
        logger.info(f"[Control Node] laura gpt infer time {time.time() - start_time}")
        start_time = time.time()
        return audio_path

    audio_path = generate(text)
    logger.info(f"Get audio path {audio_path}")
    return send_file(audio_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=args.port)
