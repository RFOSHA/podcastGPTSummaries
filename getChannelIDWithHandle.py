import googleapiclient.discovery
from urllib.parse import urlparse
import config

# Function to extract channel ID from the YouTube handle
def extract_channel_id(handle, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Make API request to search for the channel using the handle
    request = youtube.search().list(
        part="snippet",
        q=handle,
        type="channel",
        maxResults=1
    )
    response = request.execute()

    if "items" in response and len(response["items"]) > 0:
        return response["items"][0]["snippet"]["channelId"]
    else:
        print("Channel not found.")
        return None

# Main script
if __name__ == "__main__":
    # Example YouTube handle (replace with the actual handle)
    youtube_handle = "timferriss"  # Handle without '@'

    # Replace with your YouTube Data API key
    youtube_api_key = config.youtube_api_key  # Replace with your actual YouTube Data API key

    # Extract and print channel ID
    channel_id = extract_channel_id(youtube_handle, youtube_api_key)
    if channel_id:
        print(f"Channel ID: {channel_id}")
