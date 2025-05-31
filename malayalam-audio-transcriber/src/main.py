# src/main.py

from audio_capture import record_audio
from transcriber import transcribe_malayalam
from editor import edit_transcript
import os
from datetime import datetime

def main():
    print("\nMalayalam Audio Transcriber")
    print("==========================")
    
    while True:
        permission = input("\nReady to start recording? (yes/no): ").lower().strip()
        if permission in ['yes', 'y']:
            break
        elif permission in ['no', 'n']:
            print("Exiting program.")
            return
        else:
            print("Please enter 'yes' or 'no'")
    
    try:
        duration = input("Enter recording duration in seconds (default is 10): ").strip()
        duration = int(duration) if duration.isdigit() else 10
    except ValueError:
        duration = 10
    
    print(f"\nStarting audio capture for {duration} seconds...")
    print("Recording... (Press Ctrl+C to stop early)")
    
    try:
        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        audio_path = os.path.join(os.getcwd(), filename)

        record_audio(duration, audio_path)
        print(f"\nRecording complete. Saved to: {audio_path}")

        print("\nTranscribing audio...")
        transcript = transcribe_malayalam(audio_path)
        print("\nTranscript:", transcript)

        print("\nWould you like to edit the transcript?")
        if input("Enter 'yes' to edit, any other key to skip: ").lower().strip() in ['yes', 'y']:
            print("\nEditing transcript...")
            edited_transcript = edit_transcript(transcript)
        else:
            edited_transcript = transcript

        with open("transcript.txt", "w", encoding="utf-8") as f:
            f.write(edited_transcript)
        print("\nTranscript saved to transcript.txt")

    except KeyboardInterrupt:
        print("\n\nRecording interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    
    print("\nProgram finished.")

if __name__ == "__main__":
    main()
