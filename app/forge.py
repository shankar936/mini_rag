from .mind_valut import call_llm
from .Retrive import retrive


def generation(query):

    # retrieve relevant chunks
    call_retrivel = retrive(query)

    # build context from ALL chunks
    context = "\n\n".join([
        f"Topic: {r['topic']}\n{r['chunks']}"
        for r in call_retrivel
    ])

    prompt = f"""You are a helpful assistant.
Use only the context below to answer the question.
If the answer is not in the context say I don't know.

Rules:
- No hallucination
- Use only provided context

Question: {query}

Context:
{context}

Answer:"""

    try:
        response = call_llm(prompt)
    except Exception as e:
        print(f"Error occurred: {e}")
        response = "Error generating response."

    return response, call_retrivel   # ← return both