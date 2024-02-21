#env MY_PRODUCT 

import requests
from bs4 import BeautifulSoup
import os
import time
import random
import re
import openai

MY_PRODUCT = os.environ.get('MY_PRODUCT')
print("crawl MY_PRODUCT:", MY_PRODUCT)
BASE_GPTV= os.environ.get('BASE_GPTV','gpt-3.5-turbo-0125')
print("crawl BASE_GPTV:", BASE_GPTV)




def foldername_generate(content):
    """Generate a folder name using the ChatGPT API based on the content."""
    openai.api_key = 'your-api-key-here'  # Replace with your actual OpenAI API key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Update this to the model you're using, like "text-davinci-003"
            messages=[
                {"role": "system", "content": "Analyze this text and create a folder name to store its contents."},
                {"role": "user", "content": content}
            ]
        )
        folder_name = response.choices[0].message['content'].strip()
        if folder_name:
            return folder_name
        else:
            raise Exception("Failed to generate folder name. Response was empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "default_folder_name"  # Fallback folder name in case of an error


def find_urls(string):
    """Find all URLs in a given string."""
    url_regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    urls = re.findall(url_regex, string)
    return urls

def append_crawled_content(original_text, urls):
    appended_text = original_text
    for url in urls:
        content = extract_content(url)  # Assuming this is a function you have that returns {'error': None, 'text_content': '...'}
        if content['error'] is None:
            text_content = content['text_content']
            appended_text += "\n\n" + text_content
        else:
            print(f"Error occurred while crawling {url}: {content['error']}")
    return appended_text

def process_text_with_urls(text):
    urls = find_urls(text)
    if urls:
        updated_text = append_crawled_content(text, urls)
    else:
        updated_text = text  # No URLs found, use the original text
    return updated_text

def save_text_to_markdown(text, folder_name):
    """Save the given text to a Markdown file in the specified folder."""
    file_path = f"/data/{folder_name}/input.md"
    ensure_directory_exists(f"/data/{folder_name}")  # Create the directory if it doesn't exist
    with open(file_path, "w") as file:
        file.write(text)
    print(f"Text saved to {file_path}")

# Main process
updated_text = process_text_with_urls(MY_PRODUCT)
folder_name = foldername_generate(updated_text)
save_text_to_markdown(updated_text, folder_name)