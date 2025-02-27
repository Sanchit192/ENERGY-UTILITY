import re
import streamlit as st
import streamlit_sal as sal
from datarobot import Client
from datarobot.client import set_client
from streamlit_sal import sal_stylesheet

from components import render_prompt_message, render_response_message, render_empty_chat, render_app_header
from constants import *
from utils import add_new_prompt_message, initiate_session_state, get_deployment

st.set_page_config(page_title=I18N_APP_NAME, page_icon=APP_FAVICON, layout=APP_LAYOUT,
                   initial_sidebar_state=SIDEBAR_DEFAULT_STATE)

# List of US states (full names and abbreviations)
US_STATES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", 
    "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", 
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", 
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", 
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", 
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", 
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", 
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", 
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

def detect_state(user_input):
    """Detects a US state from the user input while avoiding substring mismatches."""
    if not user_input:  
        return None

    user_input_lower = user_input.lower()

    for state, abbr in US_STATES.items():
        # Use regex word boundary (\b) to avoid partial matches
        if re.search(rf'\b{re.escape(state.lower())}\b', user_input_lower) or \
           re.search(rf'\b{re.escape(abbr.lower())}\b', user_input_lower):
            return state  # Return full state name
    
    return None

def start_streamlit():
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
                st.write('Add your sidebar content here')

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
