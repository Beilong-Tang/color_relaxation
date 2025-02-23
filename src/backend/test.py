from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('test.html')

@app.route('/prompt_upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part', 'success': False}), 400
    text = request.form.get("text")
    if text is None:
        return jsonify({'message': 'No text found', 'success': False}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file', 'success': False}), 400
    if file and file.filename.endswith('.wav'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return jsonify({'message': f'File saved as {file.filename}', 'success': True}), 200
    return jsonify({'message': 'Invalid file type', 'success': False}), 400

if __name__ == '__main__':
    app.run(debug=True)

