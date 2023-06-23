import openai
import streamlit as st

def generate_response(prompt):
    """Send prompt to OpenAI and return the response. Add the prompt and response to the session state."""
    st.session_state["messages"].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=st.session_state["messages"]
    )
    response = completion.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": response})
    return response