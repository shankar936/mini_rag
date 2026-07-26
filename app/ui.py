import streamlit as st
from app.forge import generation

st.set_page_config(
    page_title="Mini RAG",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Mini RAG System")
st.markdown("Ask anything from the knowledge base")

query = st.text_input("Your question:", placeholder="What is deep learning?")

if st.button("Ask") and query:

    with st.spinner("Thinking..."):
        answer, results = generation(query)   # ← unpack both

    st.markdown("### Answer")
    st.write(answer)

    st.markdown("### Sources")
    for i, r in enumerate(results):
        with st.expander(f"Source {i+1} — {r['topic']} (score: {r['similarity']})"):
            st.write(r['chunks'])