import os
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DB_PATH = "./ielts_vectordb"

def pdf_to_text(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def load_or_create_vectordb(pdf_path="data/ielts_writing_band_descriptors.pdf"):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(VECTOR_DB_PATH):
        vectordb = FAISS.load_local(
            VECTOR_DB_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )
    else:
        text = pdf_to_text(pdf_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50
        )
        chunks = splitter.split_text(text)

        vectordb = FAISS.from_texts(chunks, embedding_model)
        vectordb.save_local(VECTOR_DB_PATH)

    return vectordb

def retrieve_context(vectordb, essay, k=5):
    docs = vectordb.similarity_search(essay, k=k)
    return "\n".join(doc.page_content for doc in docs)
