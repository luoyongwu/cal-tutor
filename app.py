
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

# 1. 从 Secrets 自动读取 Key (无感启动)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.sidebar.success("✅ 系统已激活 (Secrets Mode)")

        # 显示对话
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 引导式教学逻辑
        if prompt := st.chat_input("输入你的微积分问题..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                # 注入诱导式教学 Prompt
                instruction = "你是一位微积分导师。请使用启发诱导式教学。不要给直接答案，先问一个直观问题引导学生思考。"
                response = model.generate_content(f"{instruction} 用户问题: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"❌ API 连接失败: {e}")
else:
    st.error("未在 Secrets 中检测到 Key。请在 Streamlit 侧边栏 Settings -> Secrets 中添加：GEMINI_API_KEY = '你的KEY'")
