import streamlit as st

from utils import render_messages, create_chatbot


# ------------------------------网页------------------------------
page_title = "ChatBot"
st.set_page_config(
    page_title=page_title,
    page_icon="random",
    menu_items={
        "About": "Hi! **Jamie** developed me! Contact him [here](https://github.com/dwjamie/chatbot) if you have any problems."
    },
)

# ------------------------------侧边栏------------------------------
with st.sidebar:
    st.header("机器人配置")
    system_message = st.text_area(label="角色设定", placeholder="机器人需要扮演什么角色？")
    model = st.selectbox("模型", options=["GPT-3.5", "GPT-4", "Claude 2"])
    temperature = st.slider("随机性", min_value=0.0, max_value=1.0, step=0.01, value=0.0)
    change_config = st.button(label="更改配置")
    clean_history = st.button(label="清空对话历史")

if "current_page" not in st.session_state:
    st.session_state.current_page = page_title

if st.session_state.current_page != page_title or "chatbot" not in st.session_state:
    st.session_state.messages = []
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.session_state.current_page = page_title

if clean_history:
    st.session_state.messages = []
    st.info("对话历史已清空！", icon="✅")

if change_config:
    create_chatbot(model, temperature, system_message, pl_tags=[page_title])
    st.info("机器人配置已更改！", icon="✅")

# ------------------------------对话框------------------------------
st.title(page_title)  # 渲染标题
render_messages(st.session_state.messages)  # 渲染对话历史
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
