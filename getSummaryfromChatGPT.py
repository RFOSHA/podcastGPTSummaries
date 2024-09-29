import os
from openai import OpenAI
import config

def generate_summary(file_content, prompt):
    client = OpenAI(
        # This is the default and can be omitted
        # api_key=os.environ.get("OPENAI_API_KEY"),
        api_key = config.openai_api_key
    )

    # Send the file content to the API for summarization
    completion = client.chat.completions.create(
      model="gpt-4o-mini",  # Specify the model you'd like to use
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}:\n\n{file_content}"}
      ]
    )

    # Extract and print the summary from the response
    summary = completion.choices[0].message.content
    return summary

