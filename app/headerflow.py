from cache.utilis import load_cache, save_cache
from .shift_finder import call_slicer
from .mind_valut import call_llm
import os 
from dotenv import load_dotenv
import json

load_dotenv()

HEADER = os.getenv("identity")


def add_headers(data):

    headers = []

    topic = ''
    
    for i, info in enumerate(data):
        
        prompt = f"""
            You are an expert at generating semantic headers for a Retrieval-Augmented Generation (RAG) system.

            Generate headers for the ENTIRE chunk.

            IMPORTANT:
            - Return exactly ONE JSON object.
            - Never return multiple JSON objects.
            - Never return a JSON array.
            - Never split the chunk into multiple outputs.
            - Return ONLY valid JSON.
            - No markdown.
            - No explanations.

            Format:

            {{
                "content": "...",
                "headers": [
                    "...",
                    "...",
                    "...",
                    "...",
                    "..."
                ]
            }}

            Chunk:
            {info["chunks"]}
            """
        
        topic = info['topic']
        get_headers = call_llm(prompt)
        headers.append({
            "id" : i+1,
            "topic" : info['topic'],
            'orginal_content' : info['chunks'],
            "headers" : json.loads(get_headers)
        })

    load_header = load_cache(HEADER)
       
    load_header[topic] = headers

    save_cache(HEADER, load_header)
    return headers



def call_shifter():
    slicer = call_slicer();
    result = []

    for i in slicer:
        headers = add_headers(i)
        break
        result.append(headers)
    # return result


    
print(call_shifter())
