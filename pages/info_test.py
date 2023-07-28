import streamlit as st

import agent
from utils import render_messages

st.title("天使湾创投 V3")  # 待确认

chatbot_system_message = """你是一个擅长沟通、情商很高，讲话既幽默妥当，又逻辑清晰、一针见血的职业投资人，就职于天使湾创投。
天使湾创投，成立2010年，是一家专注于互联网早期创业的天使投资基金。
投资企业包括“洋码头”、“大姨吗”等多个估值上亿美元的项目。倾向于投资泛互联网和科技相关的领域：包括产业+互联网、消费升级、AI大数据、区块链服务、医疗健康、社交文创、深科技、互联网金融等。
20-100万种子投资，100-500万天使投资，500-1000万Pre-A投资。
你的任务是向到访的创业团队介绍天使湾，解答他们关于天使湾的疑问。如果对方表现出融资意图，请调用info_collection函数开始仔细收集对方团队的信息。"""


if "infobot_v3" not in st.session_state:
    st.session_state.infobot_v3 = agent.ChatBot()
    st.session_state.infobot_v3.set_system_message(chatbot_system_message)
    st.session_state.infobot_v3_messages = []


render_messages(st.session_state.infobot_v3_messages)

if user_message := st.chat_input("你好！"):
    # 渲染并储存用户消息
    with st.chat_message(name="user", avatar="🧑‍💻"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # 发给ChatBot
    assistant_message = st.session_state.chatbot.chat(user_message)

    # 渲染并储存ChatBot消息
    with st.chat_message(name="assistant", avatar="🤖"):
        if assistant_message == 0:  # 识别出报名意图

            def button_click():
                st.session_state.chatbot.set_system_message("你已经报名成功！哈哈哈哈")

            st.button("报名", on_click=button_click)
            assistant_message = "那好！请点击以上按钮，进入报名模式。"
        st.markdown(assistant_message)
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_message}
        )
