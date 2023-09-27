import streamlit as st

st.set_page_config(page_title="Welcome")

st.write("# Welcome! 👋")

st.markdown("##")

name = st.text_input('Password')

if name == st.secrets["password"]:
    st.session_state['state'] = 1
else:
    st.session_state['state'] = 2
 
if st.session_state['state'] == 1:
    st.write('Success')
else:
    st.write("Enter Password")
