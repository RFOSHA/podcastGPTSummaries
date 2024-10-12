import re
import googleapiclient.discovery
import isodate
import config

api_key = config.youtube_api_key

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
# Parse the ISO 8601 duration (e.g., 'PT2M30S') and return duration in seconds.
def parse_duration(duration):
    try:
        parsed_duration = isodate.parse_duration(duration)
        return int(parsed_duration.total_seconds())
    except Exception as e:
        print(f"Error parsing duration: {e}")
        return 0

def process_videos(video_item, details_item):
    # Extract the video duration (ISO 8601 duration format)
    if 'duration' not in details_item['contentDetails']:
        duration_seconds = 300  # Default duration for missing duration info
    else:
        duration = details_item["contentDetails"]["duration"]
        duration_seconds = parse_duration(duration)

    # Filter out shorts (e.g., less than 90 seconds)
    if duration_seconds >= 90:
        video_title = video_item["snippet"]["title"]
        video_title = re.sub(r'[^a-zA-Z0-9\s]', '', video_title.split('|')[0]).strip()
        video_id = video_item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Return the video object
        return {
            "title": video_title,
            "url": video_url,
            "id": video_id,
            "duration_seconds": duration_seconds
        }

    return None  # Return None if the video is too short


print("IN LIVE SECTION")
videos = []

# Fetch live videos from the channel
live_request = youtube.search().list(
    part="snippet",
    channelId="UCNjyEXSvYUUCzagFAKmaJ1Q",
    order="date",
    #eventType="live",  # Filter for live events
    type="video",  # Only return videos
    maxResults=3
)
live_response = live_request.execute()
print(live_response)

if "items" in live_response:
    live_video_ids = [item["id"]["videoId"] for item in live_response["items"]]

    # Get video details for live videos
    live_video_details_request = youtube.videos().list(
        part="contentDetails",
        id=','.join(live_video_ids)
    )
    live_video_details_response = live_video_details_request.execute()

    # Process each live video and append to the videos list
    for video_item, details_item in zip(live_response["items"], live_video_details_response["items"]):
        video = process_videos(video_item, details_item)
        if video:
            videos.append(video)

print(videos)