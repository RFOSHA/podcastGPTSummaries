from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import re
import config

# Setup for using Chrome WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_driver_path = config.chrome_driver  # Update with your actual path to the ChromeDriver


# Function to fetch and parse the HTML content using Selenium
def fetch_html_with_selenium(url):
    # Set up the Chrome WebDriver
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the URL
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(5)  # Adjust this based on how long the page takes to load

    # Get the page source (the full HTML with dynamically loaded content)
    html = driver.page_source
    #print(html)

    # Close the driver
    driver.quit()

    return html


# Function to extract episode links from the main series page based on the specific structure provided
# Function to extract episode links and their titles from the main series page
def get_episode_links(base_url):
    html = fetch_html_with_selenium(base_url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')

    # Find the root div by id
    root_div = soup.find('div', id='root')
    if not root_div:
        print("No div with id='root' found.")
        return []

    episodes = []

    # Find all <a> elements within this root div
    for link in root_div.find_all('a', href=True):
        href = link['href']
        # Filter episode links based on the provided pattern '/episode/'
        if '/episode/' in href:
            full_url = f"https://app.podscribe.ai{href}"
            # Capture the text inside the <a> tag as the title
            title = link.get_text(strip=True)
            episodes.append({"url": full_url, "title": title})

    return episodes


# Function to extract the transcript from an episode page
def extract_transcript(episode_url):
    html = fetch_html_with_selenium(episode_url)
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # Find the div that contains the transcript content
    transcript_container = soup.find_all('div', attrs={'data-slate-node': 'element'})

    if not transcript_container:
        print(f"No transcript found for episode: {episode_url}")
        return None

    transcript_text = []

    # Loop through the divs to extract the text inside nested spans
    for div in transcript_container:
        for span in div.find_all('span', attrs={'data-slate-string': 'true'}):
            transcript_text.append(span.get_text(strip=True))

    # Join the transcript text list into a single string
    return ' '.join(transcript_text)


# Main function to iterate through the last 3 episodes and extract transcripts
def extract_last_three_transcripts(base_url):
    episode_links = get_episode_links(base_url)
    save_directory = "C:/Users/ryanm/Desktop/Podcasts Summaries/Transcripts/Motley Fool Money/"

    # Sort the episode links to get the most recent ones (assuming the site lists them in descending order)
    episode_links = sorted(episode_links, key=lambda x: x["url"], reverse=True)

    # Only keep the lastest episodes
    episodes = episode_links[:config.max_results]
    transcripts = {}

    for episode in episodes:
        episode_url = episode["url"]
        episode_title = re.sub(r'[^\w\s-]', '', episode["title"]).strip()

        # Create the file path
        file_path = os.path.join(save_directory, f"{episode_title}.txt")

        if os.path.exists(file_path):
            print(f"The video TRANSCRIPT for '{episode_title}' already exists in the directory.")

        else:
            print(f"Extracting transcript from: {episode_title} ({episode_url})")
            transcript = extract_transcript(episode_url)
            if transcript:
                transcripts[episode_title] = transcript
            # Pause between requests to avoid overwhelming the server
            time.sleep(2)

        return transcripts

# Function to save transcript to a .txt file
def save_transcript_to_file(episode_name, transcript):
    # Directory to save transcripts
    # print(f"MF EPISODE NAME: {episode_name}")
    save_directory = "C:/Users/ryanm/Desktop/Podcasts Summaries/Transcripts/Motley Fool Money/"
    # print(f"MF SAVE DIRECTORY: {save_directory}")

    # Create the file path
    file_path = os.path.join(save_directory, f"{episode_name}.txt")
    # print(f"MF FILE PATH: {file_path}")

    # Check if the file already exists in the directory
    if os.path.exists(file_path):
        print(f"The video TRANSCRIPT for '{episode_name}' already exists in the directory.")
    else:
        # Write the transcript to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(transcript)

    print(f"Transcript saved to {file_path}")





