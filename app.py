
import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

# 定义放宽的安全设置
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_input = st.sidebar.text_input("请输入 Gemini API Key", type="password", value=st.session_state.api_key)

if st.sidebar.button("验证并保存"):
    clean_key = api_input.strip()
    try:
        genai.configure(api_key=clean_key)
        # 初始化模型时带上安全设置
        model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
        model.generate_content("Hi") 
        
        st.session_state.api_key = clean_key
        st.success("✅ 验证成功！")
        st.rerun()
    except Exception as e:
        st.error(f"❌ 验证失败: {e}")

if st.session_state.api_key:
    if "messages" not in st.session_state:
        st.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("输入你的微积分问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                # 每次生成时使用相同的配置
                model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
                response = model.generate_content(f"你是一位微积分导师，请详细解答: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"对话报错: {e}")
else:
    st.warning("请在侧边栏输入 API Key 并点击“验证并保存”以启动助教。")
