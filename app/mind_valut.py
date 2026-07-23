import chromadb
client = chromadb.PersistentClient(path="./mini_valut")
client.heartbeat()
from ollama import chat

collection = client.get_or_create_collection("brain", metadata={"hnsw:space": "cosine"})


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
