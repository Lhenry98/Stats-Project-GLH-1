import streamlit as st

st.set_page_config(page_title="Welcome")

st.write("# Welcome! 👋")

st.markdown("##")

admin = st.text_input('admin')
moody= st.text_input('moody')
zilker = st.text_input('zilker')

#add for each login
if name == st.secrets["admin"]:
    st.session_state['state'] = 1
else:
    st.session_state['state'] = 0
#------------------------------
if name == st.secrets["moody"]:
    st.session_state['state'] = 2
else:
    st.session_state['state'] = 0
#------------------------------
if name == st.secrets["zilker"]:
    st.session_state['state'] = 3
else:
    st.session_state['state'] = 0
#------------------------------
if st.session_state['state'] =! 0:
    st.write('Success, you are free to browse!')
else:
    st.write("Enter Password")
