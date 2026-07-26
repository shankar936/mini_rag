import math
from .slicer import split_text
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")



def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))

    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
    


def embedding(data):
    embed = []

    for i in range(len(data)):
        chunk_embed = model.encode(data[i]).tolist()

        embed.append({
            "id" : i,
            "content" : data[i],
            "length" : len(chunk_embed),
            "embedding": chunk_embed,    
        })

    return embed



def semantic_chunking(id, data, thersold):
    embed = embedding(data['text'])
    chunks = []

    current_chunk = embed[0]['content']
    last_score = 0

    for i in range(1, len(embed)):
        prev = embed[i-1]['embedding']
        curr = embed[i]['embedding'] 
       

        score = cosine_similarity(prev, curr)  
        last_score = score

        if score > thersold:
            current_chunk += "".join(embed[i]['content'])
            
        else :
            chunks.append({
                "id" : id +1,
                "topic" : data['id'],
                "chunks" : current_chunk,
                "Score" : score
                
            })
            current_chunk = embed[i]['content']

    chunks.append({
        "id": id + 1,
        "topic": data['id'],
        "chunks": current_chunk,
        "Score": last_score
    })
            

    return chunks



def call_slicer():

    sentences = split_text()
    shift_finder = []


    for i, data in enumerate(sentences):
        shifter = semantic_chunking(i, data, 0.5)
        shift_finder.append(shifter)

    return shift_finder;


