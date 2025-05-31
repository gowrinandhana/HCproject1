# src/editor.py

def edit_transcript(transcript):
    print("\n--- Transcript (You can now edit it) ---")
    print(transcript)
    print("\nEnter your corrected transcript below. Press ENTER when done:")
    print("(Tip: If you don't want to edit, just press ENTER)")

    user_input = input(">> ")
    return user_input.strip() if user_input.strip() else transcript
