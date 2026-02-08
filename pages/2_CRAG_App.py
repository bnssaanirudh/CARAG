import streamlit as st
import rag_backend as rb  # Import your backend functions

st.set_page_config(layout="wide")
st.title("📄🚀 Agentic RAG Chatbot (PDF + Web)")

# --- Initialize models and clients ---
try:
    client = rb.get_groq_client()
    model = rb.get_sentence_transformer()
    rb.get_tavily_client() 
    
    if client is None or model is None:
        st.error("Error initializing models or clients. Check API keys and backend.")
        st.stop()
        
except Exception as e:
    st.error(f"Failed to initialize models or clients: {e}")
    st.stop()


# --- Sidebar for PDF Upload and Settings ---
with st.sidebar:
    st.header("1. Upload Your PDF")
    uploaded_file = st.file_uploader("Upload a PDF document:", type="pdf")
    
    show_debug = st.checkbox("Show retrieved context (Debug)")

    if uploaded_file:
        if "faiss_index" not in st.session_state or st.session_state.get("pdf_name") != uploaded_file.name:
            with st.spinner("Processing PDF... (Extracting, Chunking, Embedding)"):
                pdf_text = rb.extract_text_from_pdf(uploaded_file)
                if pdf_text:
                    all_chunks = rb.chunk_text(pdf_text)
                    st.session_state.faiss_index, st.session_state.chunks = rb.index_chunks(all_chunks, model)
                    st.session_state.pdf_name = uploaded_file.name 
                    st.success(f"PDF '{uploaded_file.name}' processed! Indexed {len(all_chunks)} chunks.")
                else:
                    st.error("Failed to extract text from PDF.")
    
    st.header("2. Chat with your Doc")
    st.markdown("Your bot can now answer questions about your PDF *and* the general web.")

# --- Main Chat Interface ---

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# NEW: Initialize the history page list
if "history" not in st.session_state:
    st.session_state.history = []


# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new chat input
if prompt := st.chat_input("Ask about your doc or the web..."):
    # Check if user is logged in (assuming username is set at login)
    if "username" not in st.session_state:
        st.error("Error: You must be logged in to chat.")
        st.stop()
    
    username = st.session_state.username

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- AGENTIC LOGIC ---
    with st.chat_message("assistant"):
        
        # STEP 1: Decide which tool
        if "faiss_index" in st.session_state:
            tool_choice = rb.decide_tool_to_use(prompt, client)
        else:
            tool_choice = "WEB"
            st.info("No PDF loaded. Using web search.")

        # STEP 2: Run the chosen tool
        if tool_choice == "PDF":
            st.write("*(Searching PDF...)*")
            retrieved_chunks = rb.retrieve_pdf_chunks(
                prompt, 
                st.session_state.chunks, 
                st.session_state.faiss_index, 
                model
            )
            source_type = "private PDF document"
        
        else: # tool_choice == "WEB"
            st.write("*(Searching the web...)*")
            retrieved_chunks = rb.tavily_web_search(prompt)
            source_type = "web search"

        if show_debug:
            with st.info(f"Retrieved Context from {source_type} (Debug View)"):
                st.write(retrieved_chunks)

        # STEP 3: Generate and stream the response
        response_placeholder = st.empty()
        full_response = ""
        history_for_api = st.session_state.messages[:-1] 
        
        stream = rb.generate_answer_stream(
            prompt, 
            retrieved_chunks, 
            history_for_api, 
            source_type
        )
        
        for chunk in stream:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌") 
        response_placeholder.markdown(full_response)
    
    # --- NEW: Save to History ---
    
    # 1. Add assistant's full response to chat UI
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # 2. Add Q&A pair to the local session history
    st.session_state.history.append({"Question": prompt, "Answer": full_response})
    
    # 3. Write Q&A pair to Firebase
    rb.write_history_to_firestore(username, prompt, full_response)


    # Display Source Citations
    with st.expander(f"View Sources (from {source_type})"):
        for i, chunk in enumerate(retrieved_chunks):
            st.markdown(f"**Source {i+1}:**\n> {chunk}\n\n---")