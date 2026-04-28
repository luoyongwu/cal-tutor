
import streamlit as st
import google.generativeai as genai

# 页面基础配置
st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

# 侧边栏输入 API Key
api_key = st.sidebar.text_input("请输入您的 Gemini API Key", type="password")

if not api_key:
    st.info("请在左侧侧边栏输入 API Key 以开始使用。")
    st.stop()

# 初始化 AI
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"API 初始化失败: {e}")
    st.stop()

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示对话历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("输入你的微积分问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 直接调用模型
            response = model.generate_content(f"你是一位专业的微积分导师，请详细解答: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI 回复出错: {e}")
