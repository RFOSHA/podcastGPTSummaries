import re
import googleapiclient.discovery
import isodate

# Parse the ISO 8601 duration (e.g., 'PT2M30S') and return duration in seconds.
def parse_duration(duration):
    try:
        parsed_duration = isodate.parse_duration(duration)
        return int(parsed_duration.total_seconds())
    except Exception as e:
        print(f"Error parsing duration: {e}")
        return 0

# Function to process video items and return the video object
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

# Function to get the latest videos, including live streams if desired
def get_latest_video(api_key, channel_id, maxResults=1, include_live=True):
    # Build the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    videos = []

    # Fetch the latest regular videos from the channel
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=maxResults,  # Retrieve the specified number of latest videos
        type="video"  # Only return videos
    )
    response = request.execute()

    if "items" in response:
        video_ids = [item["id"]["videoId"] for item in response["items"]]

        # Get video details (including duration) for each video
        video_details_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(video_ids)
        )
        video_details_response = video_details_request.execute()

        # Process each video and append to the videos list
        for video_item, details_item in zip(response["items"], video_details_response["items"]):
            video = process_videos(video_item, details_item)
            if video:
                videos.append(video)

    if videos:
        return videos
    else:
        print("No videos found for the specified channel.")
        return None
