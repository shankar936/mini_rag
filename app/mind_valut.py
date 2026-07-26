import chromadb
client = chromadb.PersistentClient(path="./mini_valut")
client.heartbeat()
from ollama import chat
from cache.utilis import load_cache
import os 
from dotenv import load_dotenv

load_dotenv()

collection = client.get_or_create_collection("brain", metadata={"hnsw:space": "cosine"})


AUGMENTATION = os.getenv('aug')


def call_llm(prompt : str) -> str:

    reposnse = chat(
        model = 'gemma3:4b',
        messages = [
            {
            'role' : 'user',
            'content' : prompt
            }
        ]
    )

    return reposnse.message.content





# def get_flatten():
#     data = load_cache(AUGMENTATION)

#     result = []
#     id = 1
#     for i in data:
#         for j in data[i]:
#             j['id'] = id 
#             result.append(j)
#             id += 1
#     return result 


# print(get_flatten())
        