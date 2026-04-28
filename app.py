
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

# 侧边栏输入
api_input = st.sidebar.text_input("请输入您的 Gemini API Key", type="password")

if st.sidebar.button("验证并保存"):
    clean_key = api_input.strip()
    try:
        genai.configure(api_key=clean_key)
        # 使用更稳健的 gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hi")
        
        st.session_state.api_key = clean_key
        st.success("✅ 验证成功！")
        st.rerun()
    except Exception as e:
        st.error(f"❌ 验证失败: {e}")
        st.session_state.api_key = None

# 如果已有 Key，运行对话
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
                # 再次强调使用 gemini-1.5-flash
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"你是一位微积分导师，请详细解答: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"对话报错: {e}")
