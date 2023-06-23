import os

import openai
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from streamlit_chat import message
from streamlit_helpers import generate_response

# Set org ID and API key
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

# Setting page title and header
title = "Langy - The Interactive Language Tutor"
st.set_page_config(page_title=title, page_icon=":mortar_board:")
st.title(title + " :mortar_board:")

intro = """Hi! I'm Langy, an AI bot to help you improve your foreign language writing skills. 

Select the language you want to practice and the level you want to practice at in the sidebar. 
Then enter some text and I'll give you corrections and suggestions to improve your writing.

Don't know what to write? Click one of the example sentences below to get some ideas."""
st.markdown(intro)

attribution = f"""Created by [Adam Murphy](https://github.com/codeananda) - \
[Source Code](https://github.com/codeananda/ChatGPT_Projects/blob/main/language_tutor/language_tutor.py)

Need a chatbot built? Reach out via my [Upwork profile](https://www.upwork.com/freelancers/~01153ca9fd0099730e) \
to schedule a call and see how I can help."""
st.markdown(attribution)
st.markdown("---")


def get_system_prompt():
    """Define system prompt for the chatbot."""
    system_prompt = """
    You are a language tutor. 
    """
    system_prompt = system_prompt.replace("\n", " ")
    return system_prompt