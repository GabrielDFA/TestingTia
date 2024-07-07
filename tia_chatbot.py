import streamlit as st
from io import BytesIO
from PIL import Image
import requests
import time
from openai import OpenAI

# API and assistant configurations
api_key = st.secrets["API_KEY"]
assistant_id = st.secrets["ASSISTANT_ID"]

def load_openai_client_and_assistant():
    client = OpenAI(api_key=api_key)
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create()
    return client, my_assistant, thread

def wait_on_run(client, run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_assistant_response(client, assistant_thread, user_input=""):
    message = client.beta.threads.messages.create(
        thread_id=assistant_thread.id,
        role="user",
        content=user_input,
    )
    run = client.beta.threads.runs.create(
        thread_id=assistant_thread.id,
        assistant_id=assistant_id,
    )
    run = wait_on_run(client, run, assistant_thread)
    messages = client.beta.threads.messages.list(
        thread_id=assistant_thread.id, order="asc", after=message.id
    )
    
    if messages.data and messages.data[0].content and messages.data[0].content[0].text:
        return messages.data[0].content[0].text.value
    else:
        return "Maaf, sepertinya materi yang kamu tanyakan tidak ada pada mata kuliah ini."

def initialize_session_state():
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
    if 'query' not in st.session_state:
        st.session_state.query = ''

def submit():
    st.session_state.user_input = st.session_state.query
    st.session_state.query = ''

def render_ui():
    initialize_session_state()
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

if __name__ == "__main__":
    st.set_page_config(page_title="TIA - Tel-U Interactive AI", page_icon=":books:")

    client, my_assistant, assistant_thread = load_openai_client_and_assistant()

    initialize_session_state()

    user_input = render_ui()

    if user_input:
        result = get_assistant_response(client, assistant_thread, user_input)
        render_response(result)
