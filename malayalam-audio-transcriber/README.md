# Malayalam Audio Transcriber

This project provides a real-time audio transcription solution for Malayalam language audio. It captures audio from the microphone, transcribes it using the Whisper model, and allows users to edit the transcribed text.

## Project Structure

```
malayalam-audio-transcriber
├── src
│   ├── main.py          # Entry point of the application
│   ├── audio_capture.py  # Handles real-time audio input
│   ├── transcriber.py    # Transcribes audio to text
│   ├── editor.py         # Edits the transcribed text
│   └── utils
│       └── __init__.py   # Utility functions
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd malayalam-audio-transcriber
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage Guidelines

1. **Run the application:**
   ```
   python src/main.py
   ```

2. **Audio Capture:**
   - The application will start capturing audio from the microphone.
   - Press the designated key to stop recording.

3. **Transcription:**
   - The captured audio will be transcribed into Malayalam text.
   - The transcribed text will be displayed for editing.

4. **Editing:**
   - Use the editor functionality to modify the transcribed text as needed.
   - Save the edited transcript to a file.

## Dependencies

- Whisper: For audio transcription.
- Additional audio processing libraries as specified in `requirements.txt`.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Your contributions are welcome!