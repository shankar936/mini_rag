# Mini Rag (Retrivel Augmented Generation)

## overview 
A simple 'Mini Rag' project that give relavant responses using your documents or information through LLM (large Langunage Model). This rag project trained on 95,456 words with semantic chunking strategy for better meaningful accurate responses.

## projet layout
```
app/
    ragnify.py 
    harvest.py 
    slicer.py
    shift_finder.py
    headerflow.py
    docforge.py
    vector_engine.py
    retrive.py
    forge.py
    mind_valut.py
```

## features 

- 📄 Fetches articles from Wikipedia for knowledge indexing.
- ✂️ Performs semantic chunking to create meaningful document chunks.
- 🏷️ Generates descriptive headings for each chunk using an LLM.
- 📝 Enhances chunks with document augmentation and summaries.
- 🧠 Stores vector embeddings and metadata in ChromaDB.
- 🔎 Creates query rewrites and subqueries to improve retrieval.
- ⚡ Retrieves the most relevant context using semantic search.
- 💬 Generates accurate, context-aware responses using an LLM.

## Architecture Design
```
Indexing -> 

                                      INDEXING
+-----------+      +------+         +------------------+            +-------------+
| Wikipedia | -->  | NLTK | -->     | Semantic Chunker |    -->     | LLM Enhance |
+-----------+      +------+         +------------------+            +-------------+
                                                             |
                                                             v
                  +------------------+      +-------------+         +----------+
                  | Augment + Summary|  --> | Embeddings  |  -->    | ChromaDB |
                  +------------------+      +-------------+         +----------+
                                                                   ^
                                                                   |
===================================================================|========================
                                                                   |
                                                              RETRIEVAL
+------------+          +------------------+         +------+
| User Query |   -->    | Query Generation |  -->    | LLM  |
+------------+          +------------------+         +------+
                                                |
                     +--------------------------+-------------------------+
                     |                                                    |
                     v                                                    v
             +----------------+                                  +----------------+
             | Rewritten Query|                                  |   Subqueries   |
             +----------------+                                  +----------------+
                     |                                                    |
                     +--------------------------+-------------------------+
                                                |
                                                v
                                          +----------+
                                          | ChromaDB |
                                          +----------+
                                                |
                                                v
                                     +-------------+        +------+        +----------+
                                     | Merge/Clean |   -->  | LLM  |  -->   | Response |
                                     +-------------+        +------+        +----------+
```

## Indexing Pipeline
- harvest -> Fetches each topic from wikipedia and store in cache file for future use.
- silcer -> Load and iterate on wiki_valut data and using NLTK model divides paragraph into sentences.
- shift_finder -> Calling slicer file to retrive senteces and iterate on each sentence to combine related content using
semantic chunking.
- headerflow -> Iterating on combined chunks on each topic and passing to LLM (large language model) to generate headers for each
chunk
- docforge -> Fetch all chunks with headers and pass one by one to llm (large language model) to generate summary of original context and augmentation to enhance chunks.
- vector_engine -> This file is responsible to manage the emebedding and stores in chromadb. 

## Retrieval Pipeline
- Retrive -> It will manages query rewriting, sub queries and retrive related content from chromadb.
- forge -> This will pass retrived content to llm and generate accurate response throung this content.

## Installation
- python version -> 3.14.6 
- pip install -r requirements.txt  
<!-- if installation was failed due version issue or windows security --> 
- python -m pip install -r requirements.txt

## Example Query & Output

## Tech Stack

- Python
- chromadb  <!-- chromadb is a storage tool for rag beginner projects -->
- Sentence-Transformers 
- NLTK
- wikipedia-api
- ollama <!-- it will run locally on your system without api-->
- streamlit
## Future Improvements

- consumize to upload images, files, pdf's, etc... with api's 
- Includes evalution metrics and Deepeval metric for model performance

## Conclusion
- This project implements a Retrivel Augmented Generation (RAG) systems that retrives relavant content or information
from the knowledge base before generating responses with the large language model.