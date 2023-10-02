import streamlit as st

st.set_page_config(page_title="Welcome")

st.write("# Welcome! 👋")

st.markdown("##")

name = st.text_input('Password')
session_state = 0

#add for each login
if name == st.secrets["password"]:
    session_state = 1
else:
    session_state = 2
#-------------------------------------
if session_state == 1:
    st.write('Success, you are free to browse!')
else:
    st.write("Enter Password")
