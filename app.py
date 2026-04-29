
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Calculus Tutor", layout="centered")
st.title("👨‍🏫 AI Calculus Tutor")

if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Use latest model to solve 404 error
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        st.sidebar.success("Tutor Ready")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Enter your question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                try:
                    # Logic: Guided teaching, response in Chinese
                    sys_prompt = "You are a calculus tutor. Use Socratic prompting. Do not give direct answers. Respond in Chinese."
                    response = model.generate_content(f"{sys_prompt} Question: {prompt}")
                    st.markdown(final_txt := response.text)
                    st.session_state.messages.append({"role": "assistant", "content": final_txt})
                except Exception as api_err:
                    st.error(f"API Error: {api_err}")
    except Exception as e:
        st.error(f"Init Error: {e}")
else:
    st.error("Key not found in system secrets.")
