from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import whisper
import uuid
from src.transcriber import transcribe_malayalam
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder="../static", template_folder="../templates")
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load Whisper model once (medium recommended, switch to large if resources allow)
model = whisper.load_model("medium")

UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload folder exists

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio_data' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio_data']
    if audio_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save the uploaded audio file with a unique filename to avoid overwrite issues
    ext = os.path.splitext(audio_file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, unique_filename)
    audio_file.save(save_path)

    # ✅ ADD DEBUGGING HERE
    print(f"Saved audio file path: {save_path}")
    print(f"File exists: {os.path.exists(save_path)}")

        # Malayalam transcription
        result_ml = model.transcribe(save_path, language="malayalam", task="transcribe", fp16=False)
        transcript_ml = result_ml["text"]

        # English translation
        result_en = model.transcribe(save_path, language="malayalam", task="translate", fp16=False)
        translation_en = result_en["text"]
        translation_en = result_en["text"]

        # Save transcript (optional)
        with open("../transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript_ml)

        return jsonify({
            "transcript": transcript_ml,
            "translation": translation_en
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/uploads/<filename>')
def serve_audio(filename):
    return send_from_directory(UPLOAD_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
