import streamlit as st


def render_messages(messages):
    for message in messages:
        match message["role"]:
            case "user":
                avatar = "🧑‍💻"
            case "assistant":
                avatar = "🤖"
            case "system":
                avatar = "🔧"
        with st.chat_message(name=message["role"], avatar=avatar):
            st.markdown(message["content"])
