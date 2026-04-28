
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

# 侧边栏 API 设置
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "configured" not in st.session_state:
    st.session_state.configured = False

api_input = st.sidebar.text_input("请输入您的 Gemini API Key", type="password", value=st.session_state.api_key)

if st.sidebar.button("保存 API Key"):
    # 自动去空格，防止输入错误
    clean_key = api_input.strip()
    if clean_key:
        try:
            genai.configure(api_key=clean_key)
            # 简单测试一下 Key 是否有效
            model = genai.GenerativeModel('gemini-pro')
            model.generate_content("Hello")
            
            st.session_state.api_key = clean_key
            st.session_state.configured = True
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"API Key 无效，请检查！错误: {e}")
            st.session_state.configured = False
    else:
        st.sidebar.error("请输入有效的 Key")

# 如果配置成功
if st.session_state.configured:
    st.sidebar.success("✅ API Key 已保存，开始对话吧！")
    
    # 对话逻辑
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("输入你的微积分问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                chat = genai.GenerativeModel('gemini-pro').start_chat(history=[])
                response = chat.send_message(f"你是一位专业的微积分导师，请详细解答这个问题: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"发生错误: {e}")
else:
    st.warning("请在左侧输入 API Key 并点击“保存”以启动助教。")
