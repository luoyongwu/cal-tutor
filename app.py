
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

# 核心启动逻辑
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        st.sidebar.success("✅ 导师已就绪")

        # 渲染对话
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 引导式对话输入
        if prompt := st.chat_input("输入你的微积分问题..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                # 注入共识指令
                instruction = "你是一位专业的微积分导师。请使用启发诱导式教学，不要直接给答案，先通过提问引导学生思考。"
                response = model.generate_content(f"{instruction} 用户问题: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"❌ 系统运行错误: {e}")
else:
    st.error("系统底层未检测到 Key，请检查配置文件。")
