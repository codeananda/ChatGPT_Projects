import os

import openai
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from streamlit_chat import message

# Setting page title and header
st.set_page_config(page_title="Waffle House Order Bot", page_icon=":waffle:")
st.title("Waffle House Order Bot 🧇")
intro = """Welcome to the Waffle House, the place where all your waffle filled dreams come true.
Start chatting with WaffleBot below to find out what you can order, how much it costs and how to pay."""
st.markdown(intro)
attribution = f"Created by [Adam Murphy](https://github.com/codeananda)"
attribution += f" - [Source Code](https://github.com/codeananda/ChatGPT_Projects/blob/main/prompt_engineering/WaffleHouse.py)"
st.markdown(attribution)
st.markdown("---")

# Set org ID and API key
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

# Initialise session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []

waffle_prompt = """You are the Waffle House order bot. You are a helpful assistant and will help \
the customer order their meal. Be friendly and kind at all times. \
First greet the customer, then collect the order and then ask if it's pick up or delivery. \
You wait to collect the entire order, then summarize it and check for a final time if the \
customer wants to add anything else. \
Always summarize the entire order before collecting payment. \
If it's a delivery, ask them for their address. \
If it's pick up, tell them our address: 123 Waffle House Lane, London. \
Finally collect the payment. Ask if they want to pay by credit card or cash. \
If they say credit card say 'Please click the link below to pay by credit card'. \
Make sure to clarify all options, extras and sizes to uniquely identify the order. \
The menu is: \
Waffle type: normal ($10), gluten-free ($10), protein ($1 extra) \
Toppings: strawberries, blueberries, chocolate chips, whipped cream, butter, syrup, bacon \
Each topping costs $1 \
Drinks: coffee, orange juice, milk, water \
Each drink costs $2 \
Once the order is complete, output the order summary and total cost in JSON format. \
Itemize the price for each item. The fields should be 1) waffle_type, 2) list of toppings \
3) list of drinks, 4) total price
"""

initial_state = [
    {"role": "system", "content": waffle_prompt},
    {
        "role": "assistant",
        "content": "Hello, welcome to Waffle House! What can I get for you today?",
    },
]
if "messages" not in st.session_state:
    st.session_state["messages"] = initial_state
if "cost" not in st.session_state:
    st.session_state["cost"] = []
if "total_tokens" not in st.session_state:
    st.session_state["total_tokens"] = []
if "total_cost" not in st.session_state:
    st.session_state["total_cost"] = 0.0

# Sidebar - let user clear the current conversation
clear_button = st.sidebar.button("Clear Conversation", key="clear")
model = "gpt-3.5-turbo"


# reset everything
if clear_button:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["messages"] = initial_state
    st.session_state["number_tokens"] = []
    # st.session_state['model_name'] = []
    st.session_state["cost"] = []
    st.session_state["total_cost"] = 0.0
    st.session_state["total_tokens"] = []


# generate a response
def generate_response(prompt):
    st.session_state["messages"].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model, messages=st.session_state["messages"]
    )
    response = completion.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


wh_avatar = "thumbs"

message(
    "Welcome to the Waffle House! What can I get for you?",
    avatar_style=wh_avatar,
)

# container for chat history
response_container = st.container()
# container for text box
input_container = st.container()


with input_container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("You:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(
            user_input
        )
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)


if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(
                st.session_state["generated"][i],
                key=str(i),
                avatar_style=wh_avatar,
            )
