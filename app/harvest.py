import uuid

import wikipediaapi
from cache.utilis import load_cache, save_cache, is_cache
import re
import os
from dotenv import load_dotenv

load_dotenv()

wiki = wikipediaapi.Wikipedia(user_agent="Rag Project", language='en')

FILENAME = os.getenv("brain")

def extract_text(topic: str, main_heading: str):

    if is_cache(FILENAME, topic):
        print(f"{topic} found in folder, reading from cache.")
        cache = load_cache(FILENAME)
        return cache
    
    else:
        print(f"{topic} not found in cache. Fetching from Wikipedia.")
        page = wiki.page(topic)
        content = page.text

        clean_text = clean_wikipedia(content)

        cache = load_cache(FILENAME)
        cache[topic] = {
            "id": str(uuid.uuid4()),
            'topic' : topic,
            "status": "Success",
            "length": len(clean_text),
            "Source" : f"{main_heading}_wikipedia",
            "content": clean_text
        }
        save_cache(FILENAME, cache)
        print(f"Successfully saved '{topic}' in {FILENAME}")


    return content



def clean_wikipedia(text):
    # Remove LaTeX display math
    text = re.sub(r"\{\\displaystyle.*?\}", "", text, flags=re.DOTALL)

    # Remove LaTeX commands
    text = re.sub(r"\\[a-zA-Z]+", "", text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove repeated whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()



