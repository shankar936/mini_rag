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
Answer the question using ONLY the information in the context below.

Context:
{context}

Question: {query}

Instructions:
- Synthesize a clear answer IN YOUR OWN WORDS by combining relevant information from the context above.
- Do not copy sentences directly from the context — rephrase and summarize instead.
- If multiple context chunks are relevant, combine them into one coherent answer.
- Every claim in your answer must be traceable back to something stated in the context.
- If the answer is not present in the context, say "I don't know based on the provided information."

Answer:"""

    try:
        response = call_llm(prompt)
    except Exception as e:
        print(f"Error occurred: {e}")
        response = "Error generating response."

    return response, call_retrivel   # ← return both


query = input('Enter your Query: ')
response, retrive = generation(query)
print(response)
print(retrive)
      