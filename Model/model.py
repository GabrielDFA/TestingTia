import time
from openai import OpenAI
import streamlit as st

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
    
    # Check if messages are present and structured as expected
    if messages.data and messages.data[0].content and messages.data[0].content[0].text:
        return messages.data[0].content[0].text.value
    else:
        return "Maaf, sepertinya materi yang kamu tanyakan tidak ada pada mata kuliah ini."