from .mind_valut import collection


results = collection.query(
    query_texts=["What are the primary applications of generative AI image models?"],
    n_results=2
)
print(results['documents'])
