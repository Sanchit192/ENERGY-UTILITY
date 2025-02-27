import os
import re
import streamlit as st
import streamlit_sal as sal
from dotenv import load_dotenv  # Import dotenv
from datarobot import Client
from datarobot.client import set_client
from streamlit_sal import sal_stylesheet

from components import render_prompt_message, render_response_message, render_empty_chat, render_app_header
from constants import *
from utils import add_new_prompt_message, initiate_session_state, get_deployment

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title=I18N_APP_NAME, page_icon=APP_FAVICON, layout=APP_LAYOUT,
                   initial_sidebar_state=SIDEBAR_DEFAULT_STATE)

def start_streamlit():
    initiate_session_state()
    
    # Fetch credentials from environment variables
    st.session_state.token = os.getenv("TOKEN")
    st.session_state.endpoint = os.getenv("ENDPOINT")
    st.session_state.deployment_id = os.getenv("DEPLOYMENT_ID")

    if not st.session_state.token or not st.session_state.endpoint:
        st.error("Missing API credentials. Check your .env file.")
        return

    try:
        # Set up DataRobot client
        set_client(Client(token=st.session_state.token, endpoint=st.session_state.endpoint))
        has_valid_deployment = st.session_state.deployment_id and get_deployment()
    except ValueError as e:
        st.error(f"Error initializing DataRobot client: {e}")
        return

    with sal_stylesheet():
        render_app_header()

        if SHOW_SIDEBAR:
            with st.sidebar:
                st.subheader('Sidebar Title')
                st.write('Add your sidebar content here')

        if has_valid_deployment:
            user_input = st.chat_input(I18N_INPUT_PLACEHOLDER)

            if user_input:
                add_new_prompt_message(user_input)

        if len(st.session_state.messages) > 0:
            for message in st.session_state.messages:
                render_prompt_message(message)
                render_response_message(message)
        else:
            with sal.container('empty-chat'):
                render_empty_chat()

if __name__ == "__main__":
    start_streamlit()
