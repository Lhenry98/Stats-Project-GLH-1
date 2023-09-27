import streamlit as st

st.set_page_config(page_title="Welcome")

st.write("# Welcome! 👋")

st.markdown("##")

name=st.text_input('your name', 'enter')

if name=='Sina':
    st.session_state['state']=1
else:
    st.session_state['state']=2
 
if st.session_state['state']==1:
    st.write('Hello Sina')
else:
    st.write("I don't recognize you")
