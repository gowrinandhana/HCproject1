# src/transcriber.py

import whisper
import logging
import os
import torch
import numpy as np
import wave
import subprocess
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhisperTranscriber:
    def __init__(self):
        self.model = None
        logger.info("Initializing WhisperTranscriber")
        # Check if CUDA is available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
    
    def ensure_model_loaded(self):
        if self.model is None:
            try:
                logger.info("Loading Whisper model (medium)...")
                self.model = whisper.load_model("medium", device=self.device)
                logger.info("✓ Whisper model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading Whisper model: {str(e)}")
                raise RuntimeError(f"Failed to load Whisper model: {str(e)}")

    def transcribe(self, audio_path):
        try:
            if not os.path.exists(audio_path):
                logger.error(f"Audio file not found at path: {audio_path}")
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            logger.info(f"Audio file exists at: {audio_path}")
            file_size = os.path.getsize(audio_path)
            logger.info(f"Audio file size: {file_size} bytes")
            
            # Ensure model is loaded
            self.ensure_model_loaded()
            logger.info(f"Starting transcription of {audio_path}")
            
            # Transcribe the audio
            try:
                result = self.model.transcribe(
                    audio_path,
                    language="ml",
                    task="transcribe",
                    verbose=True
                )
                
                if not result:
                    logger.warning("Transcription returned no result")
                    return ""
                    
                if "text" not in result:
                    logger.warning("No 'text' field in transcription result")
                    return ""
                
                text = result["text"].strip()
                logger.info(f"Transcription successful. Text length: {len(text)} characters")
                return text
                
            except Exception as e:
                logger.error(f"Error during transcription process: {str(e)}")
                raise
            
        except Exception as e:
            logger.error(f"Error in transcribe method: {str(e)}")
            raise

# Create a single instance of the transcriber
transcriber = WhisperTranscriber()

def transcribe_malayalam(audio_path):
    """
    Transcribe Malayalam audio to text.
    
    Args:
        audio_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
        
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        RuntimeError: If there's an error with the Whisper model
        Exception: For other transcription errors
    """
    try:
        logger.info(f"Starting transcription request for: {audio_path}")
        text = transcriber.transcribe(audio_path)
        logger.info("Transcription completed successfully")
        return text
    except Exception as e:
        logger.error(f"Error in transcribe_malayalam: {str(e)}")
        raise
