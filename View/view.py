from io import BytesIO
import streamlit as st
from PIL import Image
import requests

def initialize_session_state():
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.query
    st.session_state.query = ''

def render_ui():
    logo_url = "https://github.com/GabrielDFA/Tia-Chatbot/blob/e0f2ec150495c0298da9b9e9ec1f50a71e41333b/Asset/logo.png?raw=true"
    response = requests.get(logo_url)
    logo = Image.open(BytesIO(response.content))
    col1, col2 = st.columns([1, 7])
    with col1:
        st.image(logo, width=80)
    with col2:
        st.subheader("Tanya TIA - Pemrograman Berbasis Objek 👋")

    st.write("TIA - Tel-U Interactive AI")

    st.text_input("Tanya TIA seputar Pemrograman Berbasis Objek... ", key='query', on_change=submit)

    user_input = st.session_state.user_input

    st.write("Kamu Memasukkan...", user_input)

    return user_input

def render_response(result):
    container_style = """
    <style>
    .response-container {
        max-width: 700px;
        margin: auto;
    }
    </style>
    """
    st.markdown(container_style, unsafe_allow_html=True)
    st.markdown(f'<div class="response-container"><h2>TIA <span style="color: blue;">Menjawab...</span> 🗣️</h2><p>{result}</p></div>', unsafe_allow_html=True)
