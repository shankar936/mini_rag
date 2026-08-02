from cache.utilis import load_cache, save_cache, is_cache
from .shift_finder import call_slicer
from .mind_valut import call_llm
import os 
from dotenv import load_dotenv
import json
import uuid

load_dotenv()

HEADER = os.getenv("headers")


def add_headers(data):

    cache = load_cache(HEADER) 
    headers = []

    topic = data[0]['topic']

    if is_cache(HEADER, data[0]['topic']):
        print(f"{data[0]['topic']} Found in headerFlow file")
        return cache[topic]
        
    
    for i, chunk in enumerate(data):
        print(f"Processing chunk {i+1}/{len(data)} for topic: {chunk['topic']}")

        
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
                "headers": [
                    "...",
                    "...",
                    "...",
                    "...",
                    "..."
                ]
            }}

            Chunk:
            {chunk["chunks"]}
            """
        
        topic = chunk['topic']
        get_headers = call_llm(prompt)
        get_headers = get_headers.replace("```json", "").replace("```", "").strip()

        response = json.loads(get_headers)
        headers.append({
            "id" : str(uuid.uuid4()),
            "topic" : topic,
            "source": chunk['source'],
            "original_content" : chunk['chunks'],
            "headers" : response['headers']
        })

    load_header = load_cache(HEADER)
       
    load_header[topic] = headers

    save_cache(HEADER, load_header)
    return headers



def call_shifter():
    slicer = call_slicer();

    for i in slicer:
        headers = add_headers(i)
    return headers
       

call_shifter()
