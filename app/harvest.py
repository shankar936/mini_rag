import wikipediaapi
from cache.utilis import load_cache, save_cache, is_cache
import re
import os
from dotenv import load_dotenv

load_dotenv()

wiki = wikipediaapi.Wikipedia(user_agent="Rag Project", language='en')

FILENAME = os.getenv("brain")

def extract_text(topic: str):

    if is_cache(FILENAME, topic):
        print(f"{topic} found in folder, reading from cache.")
        cache = load_cache(FILENAME)
        content = cache[topic]['content']
    else:
        print(f"{topic} not found in cache. Fetching from Wikipedia.")
        page = wiki.page(topic)
        content = page.summary

        clean_text = clean_wikipedia(content)

        cache = load_cache(FILENAME)
        cache[topic] = {
            "id": topic,
            "status": "Success",
            "length": len(clean_text),
            "Source" : "Wikipedia",
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





topics = {
    "Machine Learning",
    "Artificial Intelligence",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Data Science",
    "Neural Networks",
    "Generative AI",
    "Reinforcement Learning",
    "Large Language Models"
}



if __name__ == '__main__':
    for i in topics:
        extract_text(i)