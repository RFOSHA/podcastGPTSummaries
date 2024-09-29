import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from getLatestVideoFromYTSub import get_latest_video
from getTranscriptFromYT import *
from getSummaryfromChatGPT import *
import config

# Function to send an email with the summary attached
def send_email(subject, body, to_email):
    from_email = config.recipient_email  # Replace with your email
    from_password = config.from_password  # Replace with your email password or app-specific password

    # Create the email headers
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Log in to your email account
    server.login(from_email, from_password)

    # Send the email
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)

    # Close the connection to the server
    server.quit()