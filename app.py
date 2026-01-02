import streamlit as st
import json
from llm import load_hf_llm, MODEL_NAME
from rag import load_or_create_vectordb, retrieve_context

st.set_page_config(page_title="IELTS Writing Evaluator (RAG)", page_icon="📝")
st.title("📝 IELTS Writing Evaluator with RAG")
st.caption("Uses official IELTS band descriptors for context via RAG")

# Load LLM and vector DB
client = load_hf_llm()
vectordb = load_or_create_vectordb()

# Essay input
essay = st.text_area("Paste your IELTS Writing Response:", height=350)
use_rag = st.checkbox("Use official IELTS rubric context (RAG)", value=True)

if st.button("Evaluate Writing"):
    if not essay.strip():
        st.warning("Please enter your writing.")
    else:
        # Retrieve context if RAG is enabled
        context = retrieve_context(vectordb, essay) if use_rag else ""
        
        prompt = f"""
You are an IELTS Writing Examiner. Use the following official band descriptors to evaluate the essay.

Context:
{context}

Essay:
{essay}

Provide JSON output with:
- Task Achievement / Task Response
- Coherence & Cohesion
- Lexical Resource
- Grammar
- Final Band Score
- Strengths
- Weaknesses
- Improvement Tips
"""

        with st.spinner("Evaluating..."):
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )
            text_result = response.choices[0].message.content.strip()

        st.success("Evaluation Complete")
        
        # Try parsing JSON
        try:
            json_result = json.loads(text_result)
            st.json(json_result)
        except Exception:
            st.text_area("Evaluation Result (Raw)", value=text_result, height=400)
