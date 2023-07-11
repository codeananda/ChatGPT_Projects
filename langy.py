from typing import Any

import openai
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import LLMResult
from pydantic import BaseModel, Field

openai.api_key = st.secrets["OPENAI_API_KEY"]
openai.organization = st.secrets["OPENAI_ORG_ID"]

# Setting page title and header
title = "Langy - The Interactive AI Language Tutor"
st.set_page_config(page_title=title, page_icon=":mortar_board:")
st.title(":mortar_board: " + title)


class StreamingStreamlitCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming. Only works with LLMs that support streaming."""

    def __init__(self, message_placeholder: st.delta_generator.DeltaGenerator):
        """Initialize the callback handler.

        Parameters
        ----------
        message_placeholder: st.delta_generator.DeltaGenerator
            The placeholder where the messages will be streamed to. Typically an st.empty() object.
        """
        self.message_placeholder = message_placeholder
        self.full_response = ""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.full_response += token
        self.message_placeholder.markdown(self.full_response + "▌")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.message_placeholder.markdown(self.full_response)
        st.session_state.messages.append({"role": "assistant", "content": self.full_response})


def classify_text_level(prompt, message_placeholder):
    """Classify the prompt based on the Common European Framework of Reference. Prompt
    is assumed to be text in a foreign language that the user wants help with."""
    llm = ChatOpenAI(
        temperature=0,
        streaming=True,
        callbacks=[StreamingStreamlitCallbackHandler(message_placeholder)],
    )

    template_reason_level = """Classify the text based on the Common European Framework of Reference
    for Languages (CEFR), provide detailed reasons for your answer.

    Text: {text}

    {format_instructions}
     """

    class ReasonLevel(BaseModel):
        reason: str = Field(description="Detailed reasons for the classification")
        level: str = Field(description="The CEFR level of the text, e.g. A1, B2, etc.")

    parser_reason_level = PydanticOutputParser(pydantic_object=ReasonLevel)

    prompt_template_reason_level = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_reason_level)],
        input_variables=["text"],
        partial_variables={
            "format_instructions": parser_reason_level.get_format_instructions()
        },
    )

    shorter_template = """Classify the text based on the Common European Framework of Reference
    for Languages (CEFR), provide detailed reasons for your answer.

    Text: {text}

    Format the output as markdown like this
    
    ```markdown
    ## CEFR Level: <level>
    <reason>
    ```
     """
    prompt_template_reason_level = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(shorter_template)],
        input_variables=["text"],
    )

    chain_reason_level = LLMChain(
        llm=llm, prompt=prompt_template_reason_level, output_key="reason_level"
    )

    response = chain_reason_level({"text": prompt})
    return response


# Intro
intro = """👋 Hi! I'm Langy, an AI bot to help you improve your foreign language writing skills. ✍️

Enter some text, then I'll correct it, and explain my reasoning. 
"""
st.markdown(intro)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Let user clear the current conversation
clear_button = st.button("Clear Conversation", key="clear")
if clear_button:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter some text to get corrections"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # full_response = ""
        response = classify_text_level(prompt, message_placeholder)
        cefr_text = (
            "\n\nSee [Common European Framework of Reference for Languages]"
            "(https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages)"
            " for more information on language levels."
        )
        for letter in cefr_text:
            response['reason_level'] += letter
            message_placeholder.markdown(response['reason_level'] + "▌")
        message_placeholder.markdown(response['reason_level'])


def main():
    pass


main()
