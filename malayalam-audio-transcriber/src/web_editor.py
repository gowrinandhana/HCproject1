def format_transcript(transcript):
    """Format the transcript for web display."""
    if not transcript:
        return ""
    
    # Clean up the transcript
    transcript = transcript.strip()
    
    # Add proper line breaks for web display
    transcript = transcript.replace('\n', '<br>')
    
    return transcript 