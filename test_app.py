import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from PIL import Image
from io import BytesIO
import requests

# Fungsi dan kelas yang ingin kita uji
from tia_chatbot import (
    load_openai_client_and_assistant,
    wait_on_run,
    get_assistant_response,
    initialize_session_state,
    submit,
    render_ui,
    render_response
)

class TestStreamlitApp(unittest.TestCase):
    
    @patch('tia_chatbot.OpenAI')
    @patch('tia_chatbot.st.secrets')
    def test_load_openai_client_and_assistant(self, mock_secrets, mock_openai):
        # Mocking the secrets
        mock_secrets.return_value = {'API_KEY': 'fake_api_key', 'ASSISTANT_ID': 'fake_assistant_id'}
        
        # Mocking the OpenAI client and its methods
        mock_client = MagicMock()
        mock_assistant = MagicMock()
        mock_thread = MagicMock()
        
        mock_openai.return_value = mock_client
        mock_client.beta.assistants.retrieve.return_value = mock_assistant
        mock_client.beta.threads.create.return_value = mock_thread
        
        client, assistant, thread = load_openai_client_and_assistant()
        
        self.assertEqual(client, mock_client)
        self.assertEqual(assistant, mock_assistant)
        self.assertEqual(thread, mock_thread)
    
    @patch('tia_chatbot.time.sleep', return_value=None)
    def test_wait_on_run(self, _):
        mock_client = MagicMock()
        mock_run = MagicMock(status="queued")
        mock_thread = MagicMock(id="thread_id")
        
        # Simulate a status change from "queued" to "completed"
        mock_client.beta.threads.runs.retrieve.side_effect = [
            MagicMock(status="queued"),
            MagicMock(status="in_progress"),
            MagicMock(status="completed")
        ]
        
        result = wait_on_run(mock_client, mock_run, mock_thread)
        self.assertEqual(result.status, "completed")
    
    @patch('tia_chatbot.st.session_state', {'user_input': '', 'query': ''})
    def test_initialize_session_state(self):
        initialize_session_state()
        self.assertIn('user_input', st.session_state)
        self.assertIn('query', st.session_state)
    
    @patch('tia_chatbot.requests.get')
    @patch('tia_chatbot.Image.open')
    @patch('tia_chatbot.st.image')
    @patch('tia_chatbot.st.subheader')
    @patch('tia_chatbot.st.text_input')
    @patch('tia_chatbot.st.write')
    @patch('tia_chatbot.st.columns')
    @patch('tia_chatbot.initialize_session_state')
    def test_render_ui(self, mock_initialize_session_state, mock_columns, mock_write, mock_text_input, mock_subheader, mock_image_open, mock_requests_get, mock_image):
        mock_initialize_session_state.return_value = None
        
        # Setup the mock for requests.get to return a bytes-like content
        mock_response = MagicMock()
        mock_response.content = b'fake_image_bytes'
        mock_requests_get.return_value = mock_response

        mock_image = MagicMock()
        mock_image_open.return_value = mock_image
        mock_columns.return_value = (MagicMock(), MagicMock())
        
        col1, col2 = mock_columns.return_value
        render_ui()
        
        col1.image.assert_called_once_with(mock_image, width=80)
        col2.subheader.assert_called_once_with("Tanya TIA - Pemrograman Berbasis Objek 👋")
        mock_write.assert_any_call("TIA - Tel-U Interactive AI")

    @patch('tia_chatbot.st.markdown')
    def test_render_response(self, mock_markdown):
        render_response("Ini adalah respons TIA.")
        mock_markdown.assert_called()

if __name__ == "__main__":
    unittest.main()
