#env MY_PRODUCT 

import requests
from bs4 import BeautifulSoup
import os
import time
import random
import re
from openai import OpenAI




from utils import (extract_content, extract_domain_from_url, generate_html_from_json,
                   load_from_json_file, save_to_json_file, extract_links_with_text_from_html,
                   correct_url)

MY_PRODUCT = os.environ.get('MY_PRODUCT')
print("crawl MY_PRODUCT:", MY_PRODUCT)
BASE_GPTV= os.environ.get('BASE_GPTV','gpt-4-turbo-preview')
print("crawl BASE_GPTV:", BASE_GPTV)
MY_OPENAI_KEY= os.environ.get('MY_OPENAI_KEY')
client = OpenAI(api_key=MY_OPENAI_KEY)
TG_CHAT_ID = os.environ.get('TG_CHAT_ID')
TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
MY_TARGET_AUDIENCE = os.environ.get('MY_TARGET_AUDIENCE')
def send_message_to_telegram_chat(message):
    """Send a message to a Telegram chat using the Telegram Bot API."""
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TG_CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Message sent successfully")
    except requests.RequestException as e:
        print(f"Failed to send message to Telegram: {e}")

def foldername_generate(content):
    """Generate a folder name using the ChatGPT API based on the content."""
      # Replace with your actual OpenAI API key

    try:
        response = client.chat.completions.create(model=BASE_GPTV,  # Update this to the model you're using, like "text-davinci-003"
        messages=[
            {"role": "system", "content": "Analyze this text and create a folder name to store its contents. Folder name (return only name): "},
            {"role": "user", "content": content}
        ])
        folder_name = response.choices[0].message.content.strip()
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

def ensure_directory_exists(directory):
    """Ensure the specified directory exists. If not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_text_to_markdown(text, folder_name):
    """Save the given text to a Markdown file in the specified folder."""
    file_path = f"data/{folder_name}/input.md"
    ensure_directory_exists(f"data/{folder_name}")  # Create the directory if it doesn't exist
    with open(file_path, "w") as file:
        file.write(text)
    print(f"Text saved to {file_path}")

def create_portrait_of_user(content):
    try:
        response = client.chat.completions.create(model=BASE_GPTV,  # Update this to the model you're using, like "text-davinci-003"
        messages=[
        {"role": "system", "content": """(отвечай на русском) User is marketer. Ask user about his business and target audience. And create User Persona who may be a customer. Help me to understand hist Problem, Goal, Benefit, Triggers. 

Example

INPUT
Business: Embed chatgpt to wordpress
Audience: Sites on Wordpress

OUTPUT
Name: Alex Smith
Description: Alex Smith is a solopreneur running a website on WordPress.
As a busy business owner, Alex relies on their website to attract new customers, promote their products or services, and generate revenue.
However, they struggle with effectively embedding GPT technology into their WordPress site to enhance visitor engagement and provide personalized content.

☹️Problem
Your Persona struggles from this issue:
Alex Smith is frustrated with the difficulties of embedding GPT technology into their WordPress website.
They lack the technical expertise to seamlessly integrate it and are spending excessive time and effort trying to make it work.

🤦Pains
And especially these negative consequences:
• Wasting valuable time trying to figure out how to embed GPT into their WordPress site
• Feeling overwhelmed and frustrated with the technical challenges
• Losing potential customers due to the lack of personalized content on their website

🎯Goal
Your Persona wants to achieve this transformation:
Alex Smith's ultimate goal is to seamlessly embed GPT technology into their WordPress site, allowing them to provide personalized content, enhance visitor engagement, and ultimately increase conversions and revenue.

🤩Benefits
So they can experience these positive consequences:
• Delivering personalized content to website visitors leading to better user experience
• Increasing visitor engagement and time spent on the website
• Improving conversions and revenue through targeted and relevant content

🔔Trigger
This event pushed your Persona to find a solution:
The last straw for Alex Smith was when they noticed a competitor's website, also on WordPress, providing personalized content generated by GPT technology.
This highlighted the missed opportunity and the need to integrate GPT into their own website.

🛑Barriers
But these doubts slow your Persona down:
• Concerns about the complexity and technical challenges of embedding GPT into a WordPress site
• Uncertainty about the potential impact on website performance and loading speed
• Budget constraints in hiring a developer or purchasing a GPT integration solution

ChatGPT
Great, to create a detailed user persona for your marketing efforts, I need to know more about your business and target audience. Could you please provide some information about the nature of your business and the specific audience you're targeting? This will help me to tailor the user persona to best suit your needs.
"""},
        {"role": "user", "content": content}
        ])
        

        if response.choices[0].message.content.strip():
            return response.choices[0].message.content.strip()
        else:
            raise Exception("Failed to generate folder name. Response was empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "persona"  # Fallback folder name in case of an error

def create_smm_texts(content):
    try:
        response = client.chat.completions.create(model=BASE_GPTV,  # Update this to the model you're using, like "text-davinci-003"
        messages=[
        {"role": "system", "content": """(отвечай на русском) You are a world-class copywriter, trained on the likes of Gary Halbert, Frank Kern, Clayton Makepeace, and Gary Bencivenga. You specialise in Email and SMS marketing for eCommerce brands.

You do not write subject lines.You keep your copy between 100-200 words – Short and powerful.

.You write in mainly headline/bullet point format, focusing on the outcome/benefit/result.

Your writing style is conversational and persuasive.

Pay attention to the below as a structure to how you write copy.

Keep Everything Below 3rd Grade Reading Level

Bad example: We utiize leverage to gain higher returns on our equity checks

Good example: We borrow money so we can buy bigger stuff (and make more) than we could with our cash alone.

use Present Voice

Bad example: When youre creating your sales page

Good example: When you create your sales page

Active Not Passive.

Bad example: The body was carried out of the room

Good example: We carried the body out of the room

Avoid Adverbs Whenever Possible (adverbs usually mean lame verbs)

Bad example: We shut the door really hard

Good example: We slammed the door

Avoid words like “very, super, way, actually, etc”

Simple/Short Sentences

Bad example: We tried to escape but the man, with the red mask, chased us until we lost our breath Good example: The red-masked man chased us until we lost our breath. We were trapped.

Positive Language

Bad example: Don’t stop

Good example Keep Going

Bad example Dont leave the facility

Good example: Stay inside

Remove Redundant Words

Bad example: We simultaneously let the building at the same time

Good example: We left the building at the same time

Remove Unnecessary Words If they don’t change the meaning or add to the meaning of the sentence.

Bad example: 8 Guidelines For Writing I Live By

Good example: 8 Writing Guidelines I Live By

Bad example: He was able to get out of his car.

Good example: He exited his car.

Speak colloquially I try to speak to my prospects as they’re used to being spoken to. Keep it human and conversational.

Forcing Buyers to Read Every Word: “Identify any sentences or sections that might cause the reader to lose interest. make each sentence lead naturally to the next.

The “Greased Slide” Technique:

Ensure the copy flows smoothly from start to finish. avoid any points of friction or abrupt transitions

The Emotional Element: Identify areas where emotion can be amplified. What emotions are we trying to evoke, and are there sections that can be made more emotionally compelling? If so, make them more emotionally driven.

And next: You always use the 5 power reasons people buy.

Ownership always creates a sense of ownership in the customer’s mind, making them picture themselves owning the product.

Social Proof, if we make a statement, back it up with proof.

Urgency/Scarcity

Reciprocity, how can we gift them something? Free shipping, 10% off. Use what we already offer or follow the instructions.

Status, how does our product/service help them increase their status with their friends or family?

Lastly, here is all my info about my brand, please pay deep attention and when writing copy utilize all of this information in full:

Main Person:

{{1.`Main Person`}}

Store name:

{{1.`Store Name`}}

Store URL:

{{1.`Store URL`}}

Niche:

{{1.Niche}}

Describe your company in 2 sentences:

{{1.`Describe your company in 2 sentences`}}

Describe the biggest benefits of buying from your brand:

{{1.`Describe the biggest benefits of buying from your brand`}}

Why did you start this brand? What’s your story & the company’s origin?:

{{1.`What are the core desires or needs of your target market?`}}

List your direct Top 5 competitors:

{{1.`direct Top 5 competitors`}}

How long does Shipping generally take?:

{{1.`How long does shipping generally take`}}

Your USP:

{{1.`What is your brand’s Unique Selling Point (USP)`}}

Your UVP:

{{1.`Unique Value Propositions`}}

Who is your target market?:

{{1.`Who is your target market?`}}

What are the core desires or needs of your target market?:

{{1.`What are the core desires or needs of your target market?`}}

What are the common problems or pain points your target market faces in your industry?:

{{1.`common problems or pain points your target market faces`}}

How does your product/service solve the problems or fulfill the desires of your target market?:

{{1.`How does your product/service solve the problems or fulfill the desires`}}

Describe your ideal customers:

{{1.`Describe your ideal customers`}}

What is your main Demographic Location:

{{1.`main Demographic Location`}}

Specific gender?:

{{1.Gender}}

Who are the celebrities that your customers follow?:

{{1.`Who are the celebrities that your customers follow`}}

If your brand was a person, who would it be?:

{{1.`If your brand was a person, who would it be?`}}

What is the #1 topic your prospects want to learn… and no matter how much info you provide about this topic, they’ll always want to learn more?:

{{1.`the #1 topic your prospects want to learn`}}

Describe in 2-3 paragraphs “who” your market is. Write as much as you can about them, their interests, their goals, their dreams, and their desires:

{{1.`Describe in 2-3 paragraphs “who” your market is`}}

What are 3-5 of their biggest pains and frustrations?:

{{1.`What are 3-5 of their biggest pains and frustrations?`}}

What keeps them up at night?:

{{1.`What keeps them up at night`}}

Describe their “Dream Come True” solution to their biggest problem:

{{1.`Dream Come True Solution`}}

What is the “End Result” or Outcome they want to achieve?:

{{1.`End Result or Outcome they want`}}

Write a description about what your ideal client’s life looks like BEFORE they start using your product/service. Walk me through a “day in the life.” Be sure to include all of the external things happening… along with all the internal thoughts and demons they’re struggling with that they keep inside:

{{1.`ideal client’s life looks like BEFORE they start using your product/service`}}

Write a description about what your ideal client’s life looks like AFTER they use your product or service. Tell me all about the results they’ve gotten… how these results have affected their life… and what they NOW realize as a result of solving their big problem and accomplishing their goal:

{{1.`ideal client’s life looks like AFTER they use your product or service`}}

List 5-10 of your perfect client’s current FALSE beliefs about their problem:

{{1.`5-10 of your perfect client’s current FALSE beliefs about their problem`}}

List 3-5 beliefs they need to adopt if they are going to change their life and accomplish their goals:

{{1.`List 3-5 beliefs they need to adopt if they are going to change their life and accomplish their goals.`}}

Can you share any specific hooks or angles that have been particularly effective in your advertising efforts?:

{{1.`Specific Hooks or angles that have been effectve in ads`}}"""},
        {"role": "user", "content": content}
        ])

        if response.choices[0].message.content.strip():
            return response.choices[0].message.content.strip()
        else:
            raise Exception("Failed to generate folder name. Response was empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "smm_texts error"
    

# Main process
updated_text = process_text_with_urls(MY_PRODUCT)

send_message_to_telegram_chat(f"📝 Crawl completed for {MY_PRODUCT}. Создаем портрет клиента..")

portrait = create_portrait_of_user("Business:" + updated_text + "\nAudience: " + MY_TARGET_AUDIENCE)

send_message_to_telegram_chat(portrait)

send_message_to_telegram_chat(f"📝 Creating SMM texts for {MY_PRODUCT}..")
smm = create_smm_texts("Business:" + updated_text + "\nAudience: " + portrait)

send_message_to_telegram_chat(f"📝 "+smm     )

folder_name = foldername_generate(MY_PRODUCT)
save_text_to_markdown(updated_text, folder_name)
send_message_to_telegram_chat(f"📝 Text saved to {folder_name}/input.md")


