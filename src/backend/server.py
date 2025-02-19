from flask import Flask, Response, render_template
import wave
import time

app = Flask(__name__)

@app.route("/wav")

# def generate_sim():
#     ## Read an audio 
#
#     audio_sim = "static/example_red_color.wav"
#     
#     ## yield an audio
#     while True:
#         yield audio_sim[:int(5 * 24000)]
#         time.sleep(5)
#
# def streamwav():
#     def generate():
#         data = generate_sim()
#         while data is not None:
#             with open(data, "rb") as fwav:
#                 data = fwav.read(1024)
#                 while data:
#                     yield data
#                     data = fwav.read(1024)
#     return Response(generate(), mimetype="audio/x-wav")

# Simulating audio generation
def generate_sim():
    audio_sim = "/DKUdata/tangbl/tts/FireRedTTS/example_red_color.wav"
    
    # Open the audio file once to stream data
    with open(audio_sim, "rb") as fwav:
        # Read in chunks and simulate the periodic generation
        while True:
            # Yield a 5-second chunk of audio (assuming 24000 sample rate, 2 channels, 16-bit audio)
            # Here we simulate reading 5 seconds of audio data
            data = fwav.read(int(5 * 24000 * 2 ))  # Assuming stereo 16-bit audio (2 channels)
            if not data:
                break  # If no more data, stop the loop
            yield data
            time.sleep(5)  # Simulate periodic generation of audio

@app.route("/audio")
def streamwav():
    def generate():
        audio_gen = generate_sim()  # Get the audio chunks from the generator
        for chunk in audio_gen:
            yield chunk  # Stream each chunk of audio
        
    return Response(generate(), mimetype="audio/x-wav")


@app.route("/")
def index():
    """Audio streaming homepage."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True, port=5000)

