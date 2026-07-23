from cache.utilis import load_cache
from .mind_valut import collection
import os 
from dotenv import load_dotenv
from .shift_finder import model

load_dotenv()



AUGMENTATION = os.getenv("aug")
aug = load_cache(AUGMENTATION)



def call_embed():

    start_id = 0

    for chunk in aug:
        count = embed(chunk, start_id)
        start_id += count



def build_embed_text(chunk):


    original_content = "".join(chunk['original_content'])
    headers = " | ".join(chunk['headers'])
    augmentation = " | ".join(chunk['augmentation'])
    summary = "".join(chunk['summary'])

    return f"""{original_content}{headers}{augmentation}{summary}""".strip()



def vector_store(documents, embedding, metadata, ids):
    existing = set(collection.get(ids=ids)['ids'])
    new_idx = [i for i in range(len(ids)) if ids[i] not in existing]

    if not new_idx:
        print(f"Already stored — {len(ids)} chunks")
        return

    collection.add(
        ids=[ids[i] for i in new_idx],
        documents=[documents[i] for i in new_idx],
        metadatas=[metadata[i] for i in new_idx],
        embeddings=[embedding[i] for i in new_idx],
    )



def embed(header, start_id):

    documents = []
    embedding = []
    metadata = []
    ids = []

    for i, chunk in enumerate(aug[header]):
        
        vector_text = build_embed_text(chunk)

        vector_embed = model.encode(vector_text).tolist()

        documents.append(chunk['original_content'])
        embedding.append(vector_embed)
        metadata.append({
            "topic" : chunk['topic'],
            "headers" : " | ".join(chunk['headers']),
            "augmentation" : " | ".join(chunk['augmentation'])
        })
        ids.append(str(start_id+i))

    store = vector_store(documents, embedding, metadata, ids)
    return len(documents)
    

call_embed()

data = collection.get(include=["embeddings", "documents", "metadatas"])
print(data['embeddings'][:2])   # print first 2 embedding vectors