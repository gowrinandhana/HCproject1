from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from src.transcriber import transcribe_malayalam
from src.web_editor import format_transcript
from werkzeug.utils import secure_filename
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
    static_folder='static',
    template_folder='templates'
)

# Enable CORS
CORS(app)

# App configuration
app.config.update(
    UPLOAD_FOLDER='uploads',
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
    ALLOWED_EXTENSIONS={'wav', 'mp3', 'ogg', 'm4a', 'webm'}
)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.url}")
    if request.method == 'OPTIONS':
        return '', 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route('/')
def index():
    """Render the main page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        return jsonify({'error': 'Failed to load application'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle audio file upload and transcription."""
    start_time = time.time()
    temp_file_path = None

    try:
        logger.info("Received upload request")
        logger.info(f"Request content type: {request.content_type}")
        logger.info(f"Request headers: {dict(request.headers)}")
        
        # Check if file was uploaded
        if 'audio' not in request.files:
            logger.error("No 'audio' field in request.files")
            logger.info(f"Available fields: {list(request.files.keys())}")
            return jsonify({'error': 'No audio file provided'}), 400

        file = request.files['audio']
        if file.filename == '':
            logger.error("Empty filename provided")
            return jsonify({'error': 'No selected file'}), 400

        logger.info(f"Received file: {file.filename}")
        
        # Create a unique filename with timestamp
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        original_filename = secure_filename(file.filename)
        filename = f"recording_{timestamp}_{original_filename}"
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        try:
            logger.info(f"Saving file to: {temp_file_path}")
            file.save(temp_file_path)
            
            # Verify the file was saved
            if not os.path.exists(temp_file_path):
                raise FileNotFoundError("File was not saved successfully")
                
            file_size = os.path.getsize(temp_file_path)
            logger.info(f"File saved successfully. Size: {file_size} bytes")
            
            if file_size == 0:
                raise ValueError("Saved file is empty")
                
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}")
            return jsonify({'error': f'Failed to save audio file: {str(e)}'}), 500

        # Transcribe the audio
        try:
            logger.info("Starting transcription process...")
            transcript = transcribe_malayalam(temp_file_path)
            
            if not transcript:
                logger.warning("No speech detected in the audio")
                return jsonify({'error': 'No speech detected in the audio'}), 400

            # Format transcript for web display
            formatted_transcript = format_transcript(transcript)
            
            processing_time = time.time() - start_time
            logger.info(f"Transcription completed in {processing_time:.2f} seconds")
            logger.info(f"Transcript length: {len(formatted_transcript)} characters")

            return jsonify({
                'transcript': formatted_transcript,
                'processing_time': f"{processing_time:.2f} seconds"
            })

        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            return jsonify({'error': 'Audio file not found'}), 404
        except RuntimeError as e:
            logger.error(f"Whisper model error: {str(e)}")
            return jsonify({'error': 'Error loading transcription model'}), 500
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return jsonify({'error': f'Failed to transcribe audio: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.error(f"Failed to clean up temporary file: {str(e)}")

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large (max 16MB)'}), 413

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    try:
        # Create uploads directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            logger.info(f"Created uploads directory: {app.config['UPLOAD_FOLDER']}")
            
        logger.info("Starting Malayalam Audio Transcriber web application...")
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}") 