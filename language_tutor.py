import os
import json

import openai
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from redlines import Redlines
from streamlit_chat import message
from streamlit_helpers import generate_response

# Set org ID and API key
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

# Setting page title and header
title = "Langy - The Interactive Language Tutor"
st.set_page_config(page_title=title, page_icon=":mortar_board:")
st.title(':mortar_board: ' + title)

intro = """Hi! I'm Langy, an AI bot to help you improve your foreign language writing skills. 

Select the language you want to practice and the level you want to practice at in the sidebar. 
Then enter some text and I'll give you corrections and suggestions to improve your writing.

Don't know what to write? Click one of the example sentences below to get some ideas."""
st.markdown(intro)

attribution = f"""Made with ❤️ by [Adam Murphy](https://github.com/codeananda) - \
[Source Code](https://github.com/codeananda/ChatGPT_Projects/blob/main/language_tutor/language_tutor.py)

Need a chatbot built? Reach out via my [Upwork profile](https://www.upwork.com/freelancers/~01153ca9fd0099730e) \
to schedule a call and see how I can help."""
st.markdown(attribution)
st.markdown("---")


def get_system_prompt():
    """Define system prompt for the chatbot."""
    system_prompt = """
    You are a friendly German language language tutor here to help students improve
    their writing skills.
    
    All your responses must be in JSON format.
    """
    system_prompt = system_prompt.replace("\n", " ")
    return system_prompt


def get_prompt(german_text):
    """Define prompt for the chatbot."""
    prompt = f"""
    Please perform the following analysis on the student's input text, delimited by 
    ####
    Input text: ####{german_text}####
    
    Steps
    1. Classify the level of the input text as A1, A2, B1, B2, C1, or C2.
    2. Give a reason for the classification.
    3. Correct the grammar and spelling of the input text. Find all mistakes and provide
    all possible corrections so that it is in perfect German.
    
    Output Format
    Output the results as a JSON object with the following fields:
    1. level,
    2. level_reason,
    3. corrected_text,
    
    Do not output anything else other than the JSON object.
    """
    prompt = prompt.replace("\n", " ")
    return prompt

def write_response_to_screen(user_input, response):
    """Parse the response from the chatbot and format nicely for viewing."""
    st.markdown(f"## Input Text")
    st.markdown(user_input)
    response = json.loads(response)
    comparison = Redlines(user_input, response["corrected_text"])
    corrected_text = comparison.output_markdown
    st.markdown(f'## Level: {response["level"]}')
    st.markdown(f'{response["level_reason"]}')
    st.markdown(f"## Corrected Text")
    st.markdown(corrected_text, unsafe_allow_html=True)
    st.markdown("## Correction Reasons")
    reasoning_prompt = f"""
    Please provide a reason for each correction in the corrected text delimited by
    ####. 
    
    Corrected text: ####{corrected_text}####
    
    Provide output as a JSON with a numeric key for each correction and each value being
    a string with the reason for the correction.
    """
    reason_response = generate_response(reasoning_prompt)
    reason_response = json.loads(reason_response)
    for i, reason in reason_response.items():
        st.markdown(f"{i}. {reason}")
    return response


initial_state = [
    {"role": "system", "content": get_system_prompt()},
]

if "messages" not in st.session_state:
    st.session_state["messages"] = initial_state

# Let user clear the current conversation
clear_button = st.sidebar.button("Clear Conversation", key="clear")
if clear_button:
    st.session_state["messages"] = initial_state

# Chat history container
response_container = st.container()
# Text input container
input_container = st.container()

with input_container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("You:", height=100)
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        # Clear input area after submit
        st.session_state["messages"] = initial_state
        response = generate_response(get_prompt(user_input))
        write_response_to_screen(user_input, response)


example_sentence = """
Hallo, ich heisse Adam. Ich habe 25 Jahre alt. Ich wohne in England seit 15 Jahren
aber ich wuerde gerne irgendwo anders wohnen. Ich liebe es zu reisen. Meiner Meinung 
nach, ist man wirklich am leben, wenn man reist. 
"""
