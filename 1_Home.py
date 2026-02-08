import streamlit as st
import pyrebase  # Added for Firebase
import json      # Added to parse Firebase errors

# --- Firebase Configuration ---
firebase_config = {
  "apiKey": "AIzaSyCUbcWK3ar365MZ5p-ykXXIVJTRywJOBEg",
  "authDomain": "cloud12-45b38.firebaseapp.com",
  "projectId": "cloud12-45b38",
  "storageBucket": "cloud12-45b38.firebasestorage.app",
  "messagingSenderId": "919325392963",
  "appId": "1:919325392963:web:8508d6fee2b5b43759d4f6",
  "measurementId": "G-B3CQDMEH69",
  "databaseURL": "https://cloud12-45b38-default-rtdb.firebaseio.com"
}


# --- Initialize Firebase ---
@st.cache_resource
def init_firebase():
    """Initializes and returns the Firebase Auth object."""
    try:
        if not all(firebase_config.get(key) for key in ["apiKey", "authDomain", "projectId", "databaseURL"]):
            st.error("Firebase configuration is incomplete. Please fill in `firebase_config` in 1_Home.py.")
            return None
            
        firebase = pyrebase.initialize_app(firebase_config)
        return firebase.auth()
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {e}")
        return None

auth = init_firebase()

# --- Page Configuration ---
st.set_page_config(
    page_title="CARAG Home", # --- MODIFIED: Renamed
    page_icon="🏠",
    layout="centered"
)

# --- Background Color and Styling ---
def set_styles():
    st.markdown(f"""
    <style>
    /* --- MODIFIED: Added Background Image --- */
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1550745165-9bc0b252726c?auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* --- MODIFIED: Added "Frosted Glass" Effect for Readability --- */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: rgba(10, 25, 47, 0.8); /* Dark semi-transparent blue */
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }}
    
    /* --- MODIFIED: Renamed title class --- */
    .carag-title {{
        font-size: 6rem; /* Slightly smaller for centered layout */
        font-weight: 900;
        text-align: center;
        color: #f0f0f0;
    }}
    
    .carag-subtitle {{
        font-size: 1.5rem;
        font-weight: 300;
        text-align: center;
        color: #ddd;
    }}
    
    /* Ensure all text is readable */
    body, p, h1, h2, h3, h4, .st-bh, .st-emotion-cache-16txtl3 {{
        color: #f0f0f0; 
    }}
    </style>
    """, unsafe_allow_html=True)

set_styles()

# --- Initialize Session State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "username" not in st.session_state:
    st.session_state.username = None

# --- Login Logic ---
def login_form():
    """Displays the Firebase Login/Sign Up form."""
    # --- MODIFIED: Renamed
    st.markdown("<h1 style='text-align: center; color: #f0f0f0;'>Welcome to CARAG</h1>", unsafe_allow_html=True)
    
    if auth is None:
        st.warning("Firebase is not initialized. Please check your `firebase_config`.")
        return

    action = st.radio("Choose action:", ("Login", "Sign Up"), horizontal=True, label_visibility="collapsed")

    with st.form("firebase_auth_form"):
        email = st.text_input("Email", placeholder="user@example.com")
        password = st.text_input("Password", type="password", placeholder="********")
        submitted = st.form_submit_button(action)

        if submitted:
            try:
                if action == "Login":
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.session_state.username = user['email']
                    st.rerun()
                
                elif action == "Sign Up":
                    user = auth.create_user_with_email_and_password(email, password)
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.session_state.username = user['email']
                    st.success("Account created successfully! You are now logged in.")
                    st.balloons()
                    st.rerun()

            except Exception as e:
                # ... (Error handling code is unchanged) ...
                try:
                    error_data = e.args[1]
                    error_json = json.loads(error_data)
                    error_message = error_json['error']['message']
                    if error_message == "EMAIL_NOT_FOUND" or error_message == "INVALID_PASSWORD" or error_message == "INVALID_LOGIN_CREDENTIALS":
                        st.error("Invalid email or password. Please try again.")
                    elif error_message == "EMAIL_EXISTS":
                        st.error("An account with this email already exists. Please log in.")
                    elif error_message == "WEAK_PASSWORD":
                        st.error("Password is too weak. It must be at least 6 characters.")
                    else:
                        st.error(f"Firebase error: {error_message}")
                except (IndexError, KeyError, json.JSONDecodeError):
                    st.error(f"An error occurred: {e}")

# --- Main Page Content ---
if not st.session_state.authenticated:
    login_form()
else:
    # --- Home Page Content (when logged in) ---
    
    # --- MODIFIED: Renamed title and class ---
    st.markdown("<p class='carag-title'>CARAG</p>", unsafe_allow_html=True)
    st.markdown("<p class='carag-subtitle'>Corrective Agentic Retrieval-Augmented Generation</p>", unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to your personal document analysis tool.
    
    This application allows you to 'chat' with your PDF documents *and* the web using a powerful agent-driven RAG system.
    
    ### How to Use:
    1.  **Go to the `CARAG_App` page** using the sidebar on the left.
    2.  **Upload your PDF** in the sidebar (optional).
    3.  **Start chatting!** * Ask questions about your document (e.g., "What is the conclusion of this paper?").
        * Ask general questions (e.g., "What is the capital of France?").
    4.  **Check the `History` page** to see all your questions and answers, saved to the cloud.
    """)
    
    # --- MODIFIED: Added an "About" section ---
    with st.expander("About CARAG"):
        st.markdown("""
        **CARAG** is a "Corrective Agentic Retrieval-Augmented Generation" system.
        
        Unlike standard RAG, which is limited to a single document, CARAG acts as an intelligent **agent**. It analyzes your query and *decides* the best source of information:
        
        * **For document-specific questions,** it reads your uploaded PDF.
        * **For general or real-time questions,** it "corrects" its path and uses a live web search.
        
        This hybrid, agent-driven approach solves the "closed-domain" problem of traditional RAG, providing flexible, accurate, and context-aware answers.
        """)
    
    if st.session_state.username:
         st.sidebar.success(f"Logged in as: {st.session_state.username}")

    if st.button("Logout", type="primary"):
        # Robust logout to clear all session data
        keys_to_clear = ["authenticated", "user", "username", "messages", "history", "faiss_index", "chunks", "pdf_name"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()