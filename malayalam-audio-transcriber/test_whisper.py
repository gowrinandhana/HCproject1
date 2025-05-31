import whisper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_whisper():
    try:
        logger.info("Testing Whisper model initialization...")
        model = whisper.load_model("medium")
        logger.info("✓ Whisper model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error loading Whisper model: {str(e)}")
        return False

if __name__ == "__main__":
    if test_whisper():
        print("\nWhisper model test passed! The model is working correctly.")
    else:
        print("\nWhisper model test failed. Please check the error messages above.") 