%%writefile app.py
import streamlit as st

st.title("Cal 助教系统测试")
st.write("如果看到这段话，说明程序运行成功！")

if st.button("测试按钮"):
    st.write("点击成功，系统运行正常。")
