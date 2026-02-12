import sys
from pathlib import Path
import streamlit as st

# ---- Ajouter racine au PYTHONPATH ----
sys.path.append(str(Path(__file__).resolve().parent.parent))

# ---- Import Backend LLM ----
from Backend.main import generate_response

# ---- Page config ----
st.set_page_config(page_title="JARVIS", layout="centered")
st.title("🤖 JARVIS")
st.subheader("Hi ! How can I help ?")

# ---- Input utilisateur ----
user_input = st.text_input("Enter your message here...", placeholder="Écris ici...")

if user_input:
    with st.spinner("Generating response..."):
        response = generate_response(user_input)
        st.markdown("### Response")
        st.write(response)
