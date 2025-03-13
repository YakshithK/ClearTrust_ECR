from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Elderly Companion Robot! How can I assist you today?"

@app.route('/process-voice', methods=['POST'])
def process_voice():
    # Placeholder: later integrate Whisper transcription
    return jsonify({"status": "Audio received"})

@app.route('/scam-detection', methods=['POST'])
def scam_detection():
    # Placeholder: will integrate scam detection logic
    data = request.json
    return jsonify({"message": data.get('message', ''), "scam_alert": False})

if __name__ == '__main__':
    app.run(debug=True)
