import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Function to fetch transcript
def fetch_transcript(video_id):
    try:
        # Retrieve the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None


# Format transcript into readable form (without timestamps)
def format_transcript(transcript):
    return "\n".join([item['text'] for item in transcript])


