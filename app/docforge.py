from cache.utilis import load_cache, save_cache
from .mind_valut import call_llm
import os 
from dotenv import load_dotenv
import json
import re

load_dotenv()

HEADER = os.getenv('headers')
headers = load_cache(HEADER)
AUGMENTATION = os.getenv("aug")

def helper() :
    for i, chunk in enumerate(headers):
        chunk = headers[chunk]
        augmentation = doc_aug(chunk)
    return augmentation
        


def parse_llm_json(raw_text: str) -> dict:
    """Strip markdown fences (if any) and parse JSON safely."""
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_text.strip())
    return json.loads(cleaned) 


def doc_aug(chunk):

    aug = []

   
    for i, chunk in enumerate(chunk):
        prompt = f"""
            your an expert to provide doc augmentation for Retrivel augmented generation (RAG)

            generate (4-6 doc augmentation questions, keywords ) and single line summary related with provided chunk as JSON Format

            rule: 
            no extra content 
            no explanation 

            example_format : 

                {{
                    "summary" : "....",
                    "augmentation" : [
                    "...",
                    "...",
                    "...",
                    "...",
                    "...",
                    "..."],
                    "keywords" : [
                    "...",
                    "...",
                    "...",
                    "...",
                    "...",
                    "..."
                    ]

                }}

            chunk = {chunk['orginal_content']}

            topic = {chunk['topic']}
        """

        response = call_llm(prompt)

        if not response:
            print("Invalid Prompt")

        try:
            response = parse_llm_json(response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Raw response was: {response}")
            continue
        
        aug.append({
            "id" : i + 1,
            "topic" : chunk['topic'],
            "original_content" : chunk['orginal_content'],
            "summary" : response['summary'],
            "headers" : chunk['headers'],
            "augmentation" : response['augmentation'],
            "keywords" : response['keywords']
        })

    cache_file = load_cache(AUGMENTATION)

    cache_file[chunk['topic']] = aug 

    save_cache(AUGMENTATION, cache_file)

    print(f"Completed generationg {chunk['topic']}")

    return aug




print(helper())