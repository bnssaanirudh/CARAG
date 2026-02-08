import os
import faiss
import streamlit as st  # <-- ADDED
import pdfplumber
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from tavily import TavilyClient
from google.cloud import firestore  # <-- ADDED
from google.oauth2 import service_account  # <-- ADDED

# Load environment variables
load_dotenv()

# --- Model and Client Caching ---
# ... (get_groq_client, get_tavily_client, get_sentence_transformer... no changes here)
@st.cache_resource
def get_groq_client():
    """Returns a cached Groq client."""
    try:
        client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
        return client
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        return None

@st.cache_resource
def get_tavily_client():
    """Returns a cached Tavily client."""
    try:
        client = TavilyClient(api_key=os.environ.get('TAVILY_API_KEY'))
        return client
    except Exception as e:
        print(f"Failed to initialize Tavily client: {e}")
        return None

@st.cache_resource
def get_sentence_transformer():
    """Returns a cached sentence transformer model."""
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


# --- PDF Processing and RAG Logic ---
# ... (extract_text_from_pdf, chunk_text, index_chunks... no changes here)
def extract_text_from_pdf(uploaded_file):
    """Extracts text from an in-memory uploaded PDF file."""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def chunk_text(text, chunk_size=700, overlap=100):
    """Chunks text into overlapping segments."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def index_chunks(chunks, model):
    """Creates a FAISS index for text chunks."""
    try:
        embeddings = model.encode(chunks, show_progress_bar=True)
        embeddings = embeddings.astype('float32')
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index, chunks
    except Exception as e:
        print(f"Error creating FAISS index: {e}")
        return None, []


# --- Agentic RAG Tools ---
# ... (retrieve_pdf_chunks, tavily_web_search, decide_tool_to_use, generate_answer_stream... no changes here)
def retrieve_pdf_chunks(question, chunks, index, model, top_k=3):
    """Retrieves the most relevant chunks from the PDF."""
    try:
        question_embedding = model.encode([question]).astype('float32')
        distances, indices = index.search(question_embedding, top_k)
        return [chunks[i] for i in indices[0]]
    except Exception as e:
        print(f"Error retrieving PDF chunks: {e}")
        return []

def tavily_web_search(question, top_k=3):
    """Performs a web search using Tavily."""
    try:
        client = get_tavily_client()
        response = client.search(
            query=question, 
            search_depth="basic", 
            max_results=top_k
        )
        return [result['content'] for result in response['results']]
    except Exception as e:
        print(f"Error during Tavily search: {e}")
        return [f"Error searching web: {e}"]

def decide_tool_to_use(question, client):
    """Uses a fast LLM to decide which tool to use."""
    prompt = f"""
    You are a routing agent. Your job is to decide whether to answer a user's question using a private PDF document or a public web search.
    If the question is about "the document", "the paper", "this document", or seems to refer to a specific uploaded text, reply with the single word: PDF
    If the question is a general knowledge question, asks for real-time information, or is about a public topic, reply with the single word: WEB
    User Question: "{question}"
    Your decision (reply with only PDF or WEB):
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            top_p=0.1,
            max_tokens=10
        )
        decision = completion.choices[0].message.content.strip()
        if "PDF" in decision:
            return "PDF"
        else:
            return "WEB"
    except Exception as e:
        print(f"Error in routing: {e}")
        return "PDF"

def generate_answer_stream(question, context_chunks, chat_history, source_type):
    """Generates an answer stream using Groq based on context."""
    client = get_groq_client()
    if client is None:
        yield "Error: Groq client not initialized."
        return

    context = "\n\n---\n\n".join(context_chunks)
    system_prompt = {
        "role": "system",
        "content": f"You are an expert Q&A assistant. Use the given context from a {source_type} to answer the user's question accurately..."
    }
    user_prompt = {
        "role": "user",
        "content": f"Context: {context}\n\nQuestion: {question}"
    }
    messages_for_api = [system_prompt] + chat_history + [user_prompt]
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_for_api,
            temperature=0.2,
            top_p=0.1,
            max_tokens=1000,
            stream=True
        )
        
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        yield f"\n\nError calling Groq API: {e}"


# --- NEW: Firebase Firestore Functions ---

@st.cache_resource
@st.cache_resource
@st.cache_resource
def get_firestore_client():
    """Initializes and returns a Firestore client using a JSON key file."""
    try:
        # --- THIS IS THE FIX ---
        # Define the path to your key file
        key_file_path = ".streamlit/firestore-key.json"

        # Check if the file exists
        if not os.path.exists(key_file_path):
            st.error(f"Firestore key file not found at: {key_file_path}")
            st.error("Please make sure your JSON key file is in the .streamlit folder.")
            return None

        # Load credentials directly from the file
        creds = service_account.Credentials.from_service_account_file(key_file_path)
        db = firestore.Client(credentials=creds, project=creds.project_id)
        return db

    except Exception as e:
        st.error(f"Failed to connect to Firestore using key file: {e}")
        return None

def write_history_to_firestore(username, question, answer):
    """Writes a new Q&A pair to the user's history in Firestore."""
    try:
        db = get_firestore_client()
        if db:
            doc_data = {
                "username": username,
                "question": question,
                "answer": answer,
                "timestamp": firestore.SERVER_TIMESTAMP  # Automatically set server time
            }
            # Add a new document with a random ID to the 'chat_history' collection
            db.collection("chat_history").add(doc_data)
            return True
    except Exception as e:
        st.error(f"Error writing to Firestore: {e}")
        return False

@st.cache_data(ttl=300) # Cache for 5 minutes
def load_history_from_firestore(username):
    """Loads a user's entire chat history from Firestore."""
    try:
        db = get_firestore_client()
        if db:
            # Query the collection for docs matching the username, order by timestamp
            docs = db.collection("chat_history") \
                     .where("username", "==", username) \
                     .order_by("timestamp", direction=firestore.Query.ASCENDING) \
                     .stream()
            
            history_list = []
            for doc in docs:
                data = doc.to_dict()
                history_list.append({
                    "Question": data.get("question"),
                    "Answer": data.get("answer")
                })
            return history_list
    except Exception as e:
        st.error(f"Error loading history from Firestore: {e}")
        return []