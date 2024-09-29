import re
import googleapiclient.discovery
from urllib.parse import urlparse, parse_qs
import config


# Function to extract channel ID from the URL
def extract_channel_id(url, api_key):
    parsed_url = urlparse(url)

    # Check if it's a standard /channel/ URL
    if 'channel' in parsed_url.path:
        # Extract channel ID directly
        channel_id = parsed_url.path.split('/')[-1]
        return channel_id

    # If it's a custom or user URL, use the YouTube Data API to resolve the ID
    elif 'user' in parsed_url.path or 'c' in parsed_url.path:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

        # Extract username or custom channel name
        channel_name = parsed_url.path.split('/')[-1]

        # Make API request to search for the channel by name
        request = youtube.channels().list(
            part="id",
            forUsername=channel_name
        )
        response = request.execute()

        # If no results under username, try custom URL name as part of search
        if not response.get("items"):
            request = youtube.search().list(
                part="snippet",
                q=channel_name,
                type="channel",
                maxResults=1
            )
            response = request.execute()

        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]["id"]
        else:
            print("Channel not found.")
            return None

    else:
        print("Invalid YouTube URL format.")
        return None


# Main script
if __name__ == "__main__":
    # Example YouTube channel URLs (replace with your own)
    youtube_channel_url = "https://www.youtube.com/c/GoogleDevelopers"  # Example of a custom URL

    # Replace with your YouTube Data API key
    youtube_api_key = config.youtube_api_key  # Replace with your actual YouTube Data API key

    # Extract and print channel ID
    channel_id = extract_channel_id(youtube_channel_url, youtube_api_key)
    if channel_id:
        print(f"Channel ID: {channel_id}")
