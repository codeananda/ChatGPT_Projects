import os

import openai
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from streamlit_chat import message

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
attribution = f"Created by [Adam Murphy](https://github.com/codeananda)"
attribution += f" - [Source Code](https://github.com/codeananda/ChatGPT_Projects/blob/main/prompt_engineering/WaffleHouse.py)"
st.markdown(attribution)
st.markdown("---")
