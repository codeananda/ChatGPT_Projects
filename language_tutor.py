import os
import json
from json.decoder import JSONDecodeError

import openai
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from redlines import Redlines
from streamlit_chat import message
from streamlit_helpers import generate_response, footer, link
from htbuilder import br

# Set org ID and API key
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

# Setting page title and header
title = "Langy - The Interactive AI Language Tutor"
st.set_page_config(page_title=title, page_icon=":mortar_board:")
st.title(":mortar_board: " + title)

# Intro
intro = """👋 Hi! I'm Langy, an AI bot to help you improve your foreign language writing skills. ✍️

Enter some text, then I'll correct it, and explain my reasoning. 

I'm not perfect. Sometimes you'll get odd responses. Running it again usually helps. 🔄"""
st.markdown(intro)

# Footer
footer_elements = myargs = [
    "Made with ❤️ by ",
    link("https://github.com/codeananda", "Adam Murphy"),
    " - ",
    link(
        "https://github.com/codeananda/ChatGPT_Projects/blob/main/language_tutor/language_tutor.py",
        "Source Code",
    ),
    br(),
    "Like what you see? Let's ",
    link(
        "https://www.upwork.com/freelancers/~01153ca9fd0099730e",
        "work together",
    ),
    "! 🤝",
]
footer(*footer_elements)


def get_system_prompt():
    """Define system prompt for the chatbot. It is a language tutor there to correct
    mistakes in a foreign language."""
    system_prompt = """
    You are a friendly German language language tutor here to help students improve
    their writing skills.
    
    All your output must be in JSON format.
    Under no circumstances should you output anything extra. Only JSON object, at all times.
    """
    system_prompt = system_prompt.replace("\n", " ")
    return system_prompt


def convert_input_to_prompt(german_text):
    """Convert users input text in a foregin language, into a prompt that classifies
    the text level, gives a reason, and provides corrections."""

    prompt = f"""
    Please perform the following analysis on the student's input text, delimited by 
    ####
    Input text: ####{german_text}####
    
    Steps
    1. Classify the level of the input text as A1 (Lower Beginner), A2 (Upper Beginner), 
    B1 (Lower Intermediate), B2 (Upper Intermediate), C1 (Lower Advanced), or C2 (Upper Advanced).
    2. Give a reason for the classification.
    3. Correct the grammar and spelling of the input text. Find all mistakes and provide
    all possible corrections so that it is in perfect German. Keep paragraph breaks in tact.
    Paragraph breaks are not mistakes.
    
    Output Format
    Output the results as a JSON object with the following fields:
    1. level,
    2. level_reason,
    3. corrected_text,
    
    Do not output anything else other than the JSON object.
    """
    prompt = prompt.replace("\n", " ")
    return prompt


def write_response_to_screen(user_input: str, response: str, placeholder: st.delta_generator.DeltaGenerator):
    """Parse the response from the chatbot and format nicely for viewing.

    Parameters
    ----------
    user_input : str
        The user's input text.
    response : str
        The response from the chatbot.
    placeholder : st.delta_generator.DeltaGenerator
        The placeholder to write the response to. Likely created with st.empty().
    """
    with placeholder.container():
        st.markdown(f"## Input Text")
        st.markdown(user_input)
        try:
            response = json.loads(response)
        except JSONDecodeError:
            st.markdown('JSONDecodeError: trying again...')
            first_brace = response.find("{")
            last_brace = response.rfind("}")
            response = response[first_brace : last_brace + 1]
            response = json.loads(response)
            st.markdown('Successfully parsed JSON response.')
        comparison = Redlines(user_input, response["corrected_text"])
        corrected_text = comparison.output_markdown
        st.markdown(f'## Level: {response["level"]}')
        st.markdown(f'{response["level_reason"]}')
        st.markdown(
            'See [Common European Framework of Reference for Languages]'
            '(https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages)'
            ' for more information on language levels.'
        )
        st.markdown(f"## Corrected Text")
        st.markdown(corrected_text, unsafe_allow_html=True)
        st.markdown("## Correction Reasons")
        reasoning_prompt = f"""
        Please provide a reason for each correction in the corrected text delimited by
        ####. 
        
        Corrected text: ####{corrected_text}####
        
        Provide output as a JSON with a numeric key for each correction and each value being
        a string with the reason for the correction.
        
        Do not output anything else other than the JSON object.
        """
        reason_response = generate_response(reasoning_prompt)
        reason_response = json.loads(reason_response)
        for i, reason in reason_response.items():
            if 'no correction' in reason.lower():
                continue
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

# Create placeholder space above for output
output_space = st.empty()

with st.form(key="my_form", clear_on_submit=True):
    user_input = st.text_area("You:", height=100)
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    # st.markdown(f'This is the current user input: {user_input}')
    # Clear input area after submit
    st.session_state["messages"] = initial_state
    response = generate_response(convert_input_to_prompt(user_input))
    # response
    write_response_to_screen(user_input, response, output_space)

# st.session_state["messages"]


example_sentence = """
Hallo, ich heisse Adam. Ich habe 25 Jahre alt. Ich wohne in England seit 15 Jahren
aber ich wuerde gerne irgendwo anders wohnen. Ich liebe es zu reisen. Meiner Meinung 
nach, ist man wirklich am leben, wenn man reist. 
"""

two = """
Hey Alter, wie geht es dir denn so? Hast du Kohle? Ich bin Deutscher aber 
habe tuerkische Wurzeln, deshalb habe ich Akzent.
"""
