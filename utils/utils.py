import streamlit as st
import agent


def render_messages(messages):
    for message in messages:
        if message["role"] == "user":
            avatar = "🧑‍💻"
        elif message["role"] == "assistant":
            avatar = "🤖"
        elif message["role"] == "system":
            avatar = "🔧"
        with st.chat_message(name=message["role"], avatar=avatar):
            st.markdown(message["content"])


def create_chatbot(model, temperature, system_message, functions=None, pl_tags=[]):
    if model == "GPT-3.5":
        st.session_state.chatbot = agent.OpenAI(
            functions=functions, temperature=temperature, pl_tags=pl_tags
        )
    elif model == "GPT-4":
        st.session_state.chatbot = agent.OpenAI(
            functions=functions, temperature=temperature, model="gpt-4", pl_tags=pl_tags
        )
    elif model == "Claude 2":
        st.session_state.chatbot = agent.Claude(
            temperature=temperature, pl_tags=pl_tags
        )
    if system_message:
        st.session_state.chatbot.add_message(
            "system",
            system_message,
        )
    for message in st.session_state.messages:
        st.session_state.chatbot.add_message(message["role"], message["content"])
