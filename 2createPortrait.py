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
BASE_GPTV= os.environ.get('BASE_GPTV','gpt-3.5-turbo-0125')
print("crawl BASE_GPTV:", BASE_GPTV)
MY_OPENAI_KEY= os.environ.get('MY_OPENAI_KEY')
client = OpenAI(api_key=MY_OPENAI_KEY)
