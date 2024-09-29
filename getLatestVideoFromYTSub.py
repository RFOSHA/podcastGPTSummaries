import re
import googleapiclient.discovery
import isodate

def parse_duration(duration):
    #Parse the ISO 8601 duration (e.g., 'PT2M30S') and return duration in seconds.
    try:
        parsed_duration = isodate.parse_duration(duration)
        return int(parsed_duration.total_seconds())
    except Exception as e:
        print(f"Error parsing duration: {e}")
        return 0

def get_latest_video(api_key, channel_id, maxResults=1):
    # Build the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Fetch the latest videos from the channel
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=maxResults,  # Retrieve the specified number of latest videos
        type="video"  # Only return videos, no playlists, or channels
    )
    response = request.execute()

    videos = []

    # Check if the response contains items
    if "items" in response:
        video_ids = [item["id"]["videoId"] for item in response["items"]]

        # Now get video details (including duration) for each video
        video_details_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(video_ids)
        )
        video_details_response = video_details_request.execute()

        for video_item, details_item in zip(response["items"], video_details_response["items"]):
            print(details_item)
            # Extract the video duration (ISO 8601 duration format)
            if 'duration' not in details_item['contentDetails']:
                # If 'duration' is not present, set it to the default value of 300 seconds
                duration_seconds = 300
            else:
                duration = details_item["contentDetails"]["duration"]
                # Parse the ISO 8601 duration format
                duration_seconds = parse_duration(duration)

            # Filter out shorts (e.g., less than 90 seconds)
            if duration_seconds >= 90:  # Adjust as needed
                video_title = video_item["snippet"]["title"]
                video_title = re.sub(r'[^a-zA-Z0-9\s]', '', video_title.split('|')[0]).strip()
                video_id = video_item["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                videos.append({
                    "title": video_title,
                    "url": video_url,
                    "id": video_id,
                    "duration_seconds": duration_seconds
                })

        return videos
    else:
        print("No videos found for the specified channel.")
        return None



