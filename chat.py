import streamlit as st

import agent
from utils import render_messages

st.title("ChatBot")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = agent.OpenAI()
    st.session_state.messages = []

render_messages(st.session_state.messages)

if user_message := st.chat_input("你好！"):
    # 渲染并储存用户消息
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # 发给ChatBot
    assistant_message = st.session_state.chatbot.chat(user_message)

    # 渲染并储存ChatBot消息
    with st.chat_message(name="assistant", avatar="🤖"):
        st.markdown(assistant_message)
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message}
    )
