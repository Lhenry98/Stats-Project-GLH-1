import streamlit as st

st.set_page_config(page_title="Welcome")

st.write("# Welcome! 👋")

st.markdown("##")

name = st.text_input('Password')

#st.session_state['state'] = 0

#add for each login
if name == st.secrets["password"]:
    st.session_state['state'] = 1
else:
    st.session_state['state'] = 0
#-------------------------------------
if st.session_state['state'] == 1:
    st.write('Success, you are free to browse!')
else:
    st.write("Enter Password")
