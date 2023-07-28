import streamlit as st

import agent
from utils import render_messages

st.title("信息收集机器人")  # Single prompt + GPT-4

st.session_state.infobot_messages = []

with st.sidebar:
    role = st.text_area(
        label="角色设定", placeholder="机器人本次扮演什么人物角色？\n例：你是一位擅长沟通、逻辑清晰的职业投资人，就职于天使湾创投。"
    )
    context = st.text_area(
        label="背景知识", placeholder="机器人需要知道哪些背景知识？\n例：天使湾是一家成立于2010年、专注于创业领域的天使投资基金。"
    )
    info = st.text_area(label="信息收集", placeholder="机器人需要收集哪些信息？\n例：创业团队的个人信息、项目情况、融资意向")
    system_message = f"""===
你需要扮演的角色与任务:
{role}
===
你需要知道的背景知识:
{context}
===
你可能需要向对话者收集的信息:
{info}"""
    start_dialogue = st.button(label="开始对话")

if start_dialogue:
    st.session_state.infobot = agent.OpenAI(model="gpt-4", pl_tags=["info"])
    st.session_state.infobot.messages = [
        {"role": "system", "content": system_message},
        {
            "role": "assistant",
            "content": "明白了，我将会真实生动地扮演你描述的角色。我将永不出戏，永不脱离我的角色与职责。",
        },
    ]
    st.info("机器人创建成功！", icon="✅")

render_messages(st.session_state.infobot_messages)

if user_message := st.chat_input("你好！"):
    # 如用户尚未创建机器人，则提示用户先创建机器人
    if "infobot" not in st.session_state:
        st.info("请先填写机器人配置", icon="🚨")
        st.stop()

    # 渲染并储存用户消息
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(user_message)
    st.session_state.infobot_messages.append({"role": "user", "content": user_message})

    # 发给ChatBot
    assistant_message = st.session_state.infobot.chat(user_message)

    # 渲染并储存ChatBot消息
    with st.chat_message(name="assistant", avatar="🤖"):
        st.markdown(assistant_message)
    st.session_state.infobot_messages.append(
        {"role": "assistant", "content": assistant_message}
    )
