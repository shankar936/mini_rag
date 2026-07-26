import nltk
import os 
from nltk.tokenize import sent_tokenize
from dotenv import load_dotenv
from cache.utilis import get_cache_path, load_cache, save_cache


load_dotenv()

BASE = os.getenv("brain")

nltk.download("punkt")
nltk.download("punkt_tab")


def split_text():
    
    # loading all the content from cache/wiki_valut file and storing it in articles 
    articles = load_cache(BASE)

    chunks = []

    # iterating on load data and passing to sent_tokenize to split into chunks
    for topic, article in articles.items():
        chunk = sent_tokenize(article['content'])

        chunks.append({
            "id" : topic,
            "length" : len(chunk),
            "text" : chunk
        })
    return chunks




