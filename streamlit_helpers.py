import openai
import streamlit as st
from htbuilder import (
    HtmlElement,
    div,
    ul,
    li,
    br,
    hr,
    a,
    p,
    img,
    styles,
    classes,
    fonts,
)
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def generate_response(prompt, temperature=0):
    """Send prompt to OpenAI and return the response. Add the prompt and response to
    the session state."""
    st.session_state["messages"].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"],
        temperature=temperature,
    )
    response = completion.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": response})
    return response


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def footer(*args: list):
    """Add footer at the bottom of your Streamlit app.
    Adapted from https://discuss.streamlit.io/t/st-footer/6447

    Parameters
    ----------
    *args : list
        List of strings, links, or br elements to display in the footer. They will all be combined
        together.

    Example Input Parameters
    ------------------------
    >>> footer_elements = myargs = [
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
    >>> footer(*footer_elements)
    """

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1,
    )

    style_hr = styles(
        display="block",
        margin=px(0, 0, "auto", "auto"),
        border_style="inset",
        border_width=px(0),
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, (str, HtmlElement)):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)
