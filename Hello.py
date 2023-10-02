import streamlit as st

st.set_page_config(page_title="Welcome")

st.write("# Welcome! 👋")

st.markdown("##")

name = st.text_input('Password')

if 'key' not in st.session_state:
    st.session_state.key = 0

if name == st.secrets["soldout"]["soldout"]:
    st.session_state.key = 1
elif name == st.secrets["moody"]["moody"]:
    st.session_state.key = 2
else:
    st.session_state.key = 3
#-------------------------------------
if st.session_state.key == 1:
    st.write('Success, you are free to browse!')
elif st.session_state.key == 2:
    st.write('Success, you are free to browse!')
else:
    st.write("Enter Password")
