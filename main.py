import os
import json
from getLatestVideoFromYTSub import get_latest_video
from getTranscriptFromYT import *
from getSummaryfromChatGPT import *
from getMFTranscripts import *
from sendEmail import *
import config

# Main script
if __name__ == "__main__":
    # Replace with your YouTube Data API key
    api_key = config.youtube_api_key
    recipient_email = config.recipient_email

    with open('channels2.json', 'r') as f:
        channels = json.load(f)

    for podcast in channels['podcasts']:
        channel = podcast.get('channel')
        channel_id = podcast.get('youtube_id')
        active = podcast.get('active')
        prompt = podcast.get('prompt')
        include_live = podcast.get('include_live')


        if active == False:
            continue

        if channel_id != "":
            print(f"Channel: {channel}")

            # Directory where the check will be performed (replace with your actual directory)
            transcript_directory = f'{config.transcript_path_prefix}{channel}'
            summary_directory = f'{config.summary_path_prefix}{channel}'

            latest_videos = get_latest_video(api_key, channel_id, config.max_results, include_live)
            if latest_videos:
                for latest_video in latest_videos:
                    if latest_video:
                        print(latest_video)
                        print(f"Latest Video Title: {latest_video['title']}")
                        print(f"Video URL: {latest_video['url']}")

                    # Create the file path by appending ".txt" extension to the cleaned title
                    transcript_file_path = os.path.join(transcript_directory, f"{latest_video['title']}.txt")

                    # Check if the file already exists in the directory
                    if os.path.exists(transcript_file_path):
                        print(f"The video TRANSCRIPT for '{latest_video['title']}' already exists in the directory.")
                    else:
                        try:
                            # If the file doesn't exist, create a new empty file
                            video_transcript = fetch_transcript(latest_video['id'])
                            formatted_transcript = format_transcript(video_transcript)
                        except Exception as e:
                            # Handle the exception and print the error
                            print(
                                f"Error occurred while fetching or formatting the transcript for video '{latest_video['title']}': {e}")
                            continue  # Skip the rest of this iteration and move to the next video

                        with open(transcript_file_path, 'w') as f:
                            f.write(f"Video title: {latest_video['title']}\n")
                            f.write(formatted_transcript)
                        print(f"New file created for the video TRANSCRIPT for '{latest_video['title']}' in the transcripts directory.")

                        summary = generate_summary(formatted_transcript, prompt)

                        # Create the file path by appending ".txt" extension to the cleaned title
                        summary_file_path = os.path.join(summary_directory, f"{latest_video['title']}.txt")

                        # Check if the file already exists in the directory
                        if os.path.exists(summary_file_path):
                            print(f"The video SUMMARY for'{latest_video['title']}' already exists in the directory.")
                        else:
                            with open(summary_file_path, 'w') as f:
                                f.write(f"Video title: {latest_video['title']}\n")
                                f.write(summary)
                            print(f"New file created for the video SUMMARY for '{latest_video['title']}' in the summaries directory.")

                        # Send email with summary as an attachment
                        subject = f"{channel} - Summary of: {latest_video['title']}"
                        body = summary
                        send_email(subject, body, recipient_email)
                        print(f"Email sent with the summary of '{latest_video['title']}' to {recipient_email}.")
            else:
                print(f"No videos retrieved for: {channel}")
        else:
            #Now handle the Motley fool podcasts

            # URL of the podcast series on Podscribe
            base_url = "https://app.podscribe.ai/series/1085"

            mf_summary_directory = f'{config.summary_path_prefix}Motley Fool Money/'

            # Extract and print transcripts of the last three episodes
            transcripts = extract_last_three_transcripts(base_url)

            for episode_title, transcript in transcripts.items():
                save_transcript_to_file(episode_title, transcript)

                # Create the file path for Motley Fool Money
                mf_summary_file_path = os.path.join(mf_summary_directory, f"{episode_title}.txt")

                # Check if the file already exists in the directory
                if os.path.exists(mf_summary_file_path):
                    print(f"The video SUMMARY for '{episode_title}' already exists in the directory.")
                else:
                    mf_summary = generate_summary(transcript, prompt)
                    with open(mf_summary_file_path, 'w') as f:
                        f.write(f"Video title: {episode_title}\n")
                        f.write(mf_summary)
                    print(f"New file created for the video SUMMARY for '{episode_title}' in the summaries directory.")

                    # Send email with summary as an attachment
                    subject = f"Motley Fool - Summary of: {episode_title}"
                    body_mf = mf_summary
                    send_email(subject, body_mf, recipient_email)
                    print(f"Email sent with the summary of '{episode_title}' to {recipient_email}.")
