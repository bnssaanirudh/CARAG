import streamlit as st
import pandas as pd
import rag_backend as rb  # Import your backend functions

# --- Page Configuration ---
st.set_page_config(
    page_title="Query History",
    page_icon="🗂️",
    layout="wide"
)

# --- Background Image and Styling (Same as Home) ---
def set_styles():
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: black;
        /* ... other styles ... */
    }}
    .stDataFrame th {{
        background-color: #f0f2f6;
        color: #333;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

set_styles()

# --- Page Protection ---
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in from the `1_Home` page to view history.")
    st.stop()

# --- History Page Content ---
st.title("🗂️ Session Query History")

# Get username
username = st.session_state.get("username", None)
if not username:
    st.error("Error: Could not find username. Please log in again.")
    st.stop()

# --- NEW: Load from Firestore ---
# We check if history has already been loaded this session.
if "history" not in st.session_state:
    with st.spinner("Loading persistent history from cloud..."):
        # Load from Firebase and store it in the session
        st.session_state.history = rb.load_history_from_firestore(username)
else:
    # If "history" is in session_state, it means we've already loaded it
    # OR we've been adding to it from the CRAG_App page.
    # The rb.load_history_from_firestore() is cached, but this
    # check prevents re-loading if we just navigate away and come back.
    pass 


if "history" in st.session_state and st.session_state.history:
    st.markdown("Here is your complete query history, loaded from the cloud.")
    
    # Convert history list of dicts to a DataFrame
    # Note: This will be in reverse chronological order from Firestore
    df = pd.DataFrame(st.session_state.history)
    
    # Optional: Display in reverse order (newest on top)
    st.dataframe(df.iloc[::-1], use_container_width=True)
    
    # --- Download Button ---
    @st.cache_data
    def convert_df_to_csv(df_to_convert):
        return df_to_convert.to_csv(index=False).encode('utf-8')

    csv_data = convert_df_to_csv(df)
    
    st.download_button(
        label="Download History as CSV",
        data=csv_data,
        file_name=f"{username}_chat_history.csv",
        mime="text/csv",
        type="primary"
    )
    
else:
    st.info("No queries have been made in this session. Go to the `2_CRAG_App` page to start.")