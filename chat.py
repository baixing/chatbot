import streamlit as st

import agent
from utils import render_messages

st.title("ChatBot")

if "chatbot" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("机器人配置")
    role = st.text_area(label="角色设定")
    model = st.selectbox("模型", options=["GPT-3.5", "GPT-4", "Claude 2"])
    temperature = st.slider("随机性", min_value=0.0, max_value=1.0, step=0.01, value=0.0)
    start_dialogue = st.button(label="开始对话")

if start_dialogue:
    if model == "GPT-3.5":
        st.session_state.chatbot = agent.OpenAI(
            temperature=temperature, pl_tags=["chatbot"]
        )
    elif model == "GPT-4":
        st.session_state.chatbot = agent.OpenAI(
            temperature=temperature, model="gpt-4", pl_tags=["chatbot"]
        )
    elif model == "Claude 2":
        st.session_state.chatbot = agent.Claude(
            temperature=temperature, pl_tags=["chatbot"]
        )
    if role:
        st.session_state.chatbot.add_message(
            "system",
            role,
        )
    for message in st.session_state.messages:
        st.session_state.chatbot.add_message(message["role"], message["content"])
    st.info("机器人创建成功！", icon="✅")

render_messages(st.session_state.messages)

if user_message := st.chat_input("你好！"):
    # 如用户尚未创建机器人，则提示用户先创建机器人
    if "chatbot" not in st.session_state:
        st.info("请先填写机器人配置", icon="🚨")
        st.stop()

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
