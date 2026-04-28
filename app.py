
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="微积分导师", layout="centered")
st.title("👨‍🏫 AI 微积分导师")

# 1. 确保 Session State 初始化
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 2. 自动配置 (核心：每次刷新都会执行)
if st.session_state.api_key:
    genai.configure(api_key=st.session_state.api_key)

# 3. 侧边栏输入与保存
api_input = st.sidebar.text_input("请输入 Gemini API Key", type="password", value=st.session_state.api_key)

if st.sidebar.button("验证并保存"):
    clean_key = api_input.strip()
    try:
        genai.configure(api_key=clean_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        model.generate_content("Hi") # 测试连接
        
        st.session_state.api_key = clean_key
        st.success("✅ 验证成功！")
        st.rerun() # 保存后立即刷新
    except Exception as e:
        st.error(f"❌ 验证失败: {e}")

# 4. 对话逻辑 (只有有了 Key 才会运行)
if st.session_state.api_key:
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
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"你是一位微积分导师，请详细解答: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"对话报错: {e}")
else:
    st.warning("请在侧边栏输入 API Key 并点击“验证并保存”以启动助教。")
