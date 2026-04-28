
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

api_input = st.sidebar.text_input("请输入您的 Gemini API Key", type="password")

if st.sidebar.button("验证并保存 API Key"):
    clean_key = api_input.strip()
    try:
        genai.configure(api_key=clean_key)
        # 强制进行一次连接测试
        model = genai.GenerativeModel('gemini-pro')
        model.generate_content("Hello")
        st.session_state.api_key = clean_key
        st.success("✅ 验证成功！可以开始提问了。")
    except Exception as e:
        st.error(f"❌ Key 无效: {e}")
        st.session_state.api_key = None

if "api_key" in st.session_state and st.session_state.api_key:
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
                response = chat.send_message(f"你是一位微积分导师，请详细解答: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"对话出错: {e}")
