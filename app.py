
import streamlit as st
import google.generativeai as genai

# 页面基础配置
st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

# 在侧边栏使用 Session State 保存 API Key
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 侧边栏输入
api_input = st.sidebar.text_input("请输入您的 Gemini API Key", type="password", value=st.session_state.api_key)

# 加入明确的保存按钮
if st.sidebar.button("保存 API Key"):
    st.session_state.api_key = api_input
    st.rerun()  # 强制刷新页面以加载 API

# 初始化 AI
if st.session_state.api_key:
    try:
        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.sidebar.error(f"API Key 配置错误: {e}")
else:
    st.sidebar.warning("请在左侧输入 API Key 并点击“保存”")
    st.stop() 

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理输入
if prompt := st.chat_input("输入你的微积分问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(f"你是一位专业的微积分导师，请详细解答这个问题: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"发生错误: {e}")
