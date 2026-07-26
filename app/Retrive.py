from .mind_valut import call_llm, collection
import json
import re
from .shift_finder import model

def query_rebuild(query):
    prompt = f"""
        generate a rewriten query for the rag project

        your are an expert to rewrite the query in meaningful and 
        descriptive way according to user query in one line

        rules:
        - no  extra content
        - no examples 
        - no symbols 
        - no answer or responses


        query : {query}

    """
    generate_query = call_llm(prompt)

    return generate_query



def parse_llm_json_response(raw_response: str) -> dict:
    # Strip markdown code fences if present (```json ... ``` or ``` ... ```)
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_response.strip())
    return json.loads(cleaned)

def subqueires(query):

    prompt = f"""
        Break this complex query into 3 - subquestions for this rag project 

        format :
        {{
            "subquestions" : [
            "...",
            "...",
            "...",
            ]
        }}

        query = {query}

    """

    generated_subqueries = call_llm(prompt)

    return generated_subqueries



def searching(question):

    result = collection.query(
        query_embeddings= [question],
        n_results=2
    )

    if not result:
        print("Hallucination started")

    return result


def extract_result(raw):

    documents = raw['documents'][0]
    metadata = raw['metadatas'][0]
    distances = raw['distances'][0]
    ids = raw['ids'][0]


    return [
        {
            'id' : id,
            'chunks' : chunk,
            'topic' : meta['topic'],
            'similarity'  : round(1 - dis,4)
        }

        for chunk, meta, dis, id in zip(documents, metadata, distances, ids)
    ]



def retrive(userquery):

    if userquery == None:
        return 'User Query Required'


    thersold = 0.5

    result = []
    seen_ids = set()
    build_query = query_rebuild(userquery)

    query_embedding = model.encode(build_query).tolist()
    raw_result = searching(query_embedding)

    for r in extract_result(raw_result):
        if r['id'] not in seen_ids:
            seen_ids.add(r['id'])
            result.append(r)

    sub_response = subqueires(userquery)
    subquery = parse_llm_json_response(sub_response)
    for question in subquery['subquestions']:
        subquery_embedding = model.encode(question).tolist()
        raw_search = searching(subquery_embedding)

        for r in extract_result(raw_search):
            if r['id'] not in seen_ids:
                seen_ids.add(r['id'])
                result.append(r)
        result = [r for r in result if r['similarity'] > thersold]

    return result
