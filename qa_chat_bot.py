import os
import re
import streamlit as st
import streamlit_sal as sal
from datarobot import Client
from datarobot.client import set_client
from streamlit_sal import sal_stylesheet
from dotenv import load_dotenv 
from components import render_prompt_message, render_response_message, render_empty_chat, render_app_header
from constants import *
from utils import add_new_prompt_message, initiate_session_state, get_deployment

st.set_page_config(page_title=I18N_APP_NAME, page_icon=APP_FAVICON, layout=APP_LAYOUT,
                   initial_sidebar_state=SIDEBAR_DEFAULT_STATE)

load_dotenv() 

# List of US states (only full names)
US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", 
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", 
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", 
]

def detect_state(user_input):
    """Detects a US state from the user input without considering abbreviations."""
    if not user_input:  
        return None

    user_input_lower = user_input.lower()

    for state in US_STATES:
        # Use regex word boundary (\b) to avoid partial matches
        if re.search(rf'\b{re.escape(state.lower())}\b', user_input_lower):
            return state  # Return full state name
    
    return None

def start_streamlit():
    st.session_state.token = os.getenv("TOKEN")
    st.session_state.endpoint = os.getenv("ENDPOINT")
    st.session_state.deployment_id = os.getenv("DEPLOYMENT_ID")
    initiate_session_state()
    
    if "selected_state" not in st.session_state:
        st.session_state.selected_state = None

    # Setup DR client
    set_client(Client(token=st.session_state.token, endpoint=st.session_state.endpoint))
    has_valid_deployment = st.session_state.deployment_id and get_deployment()

    with sal_stylesheet():
        render_app_header()

        if SHOW_SIDEBAR:
            with st.sidebar:
                st.subheader('Sidebar Title')
                st.write('Add your sidebar content here ....')

        # If chatbot is ready
        if has_valid_deployment:
            user_input = st.chat_input(I18N_INPUT_PLACEHOLDER)

            if user_input:
                # Detect state if mentioned
                detected_state = detect_state(user_input)
                if detected_state:
                    st.session_state.selected_state = detected_state

                # Ensure the chatbot retains the selected state
                selected_state = st.session_state.selected_state

                # If the state is known, append it to user input before sending to chatbot
                if selected_state:
                    if re.fullmatch(r"\s*no[\s.!?]*", user_input, re.IGNORECASE):
                        st.session_state.selected_state = None  # Reset the state
                        add_new_prompt_message("Thank you! Call us again for further queries.")
                        return  
                    else:
                        user_input = f"User is from {selected_state}. {user_input}"

    
                # Send updated user input for processing
                add_new_prompt_message(user_input)

        # Render chat history
        if len(st.session_state.messages) > 0:
            for message in st.session_state.messages:
                render_prompt_message(message)
                render_response_message(message)
        else:
            with sal.container('empty-chat'):
                render_empty_chat()

if __name__ == "__main__":
    start_streamlit()
