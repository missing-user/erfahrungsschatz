import streamlit as st
import pyrebase
import login
import datetime

config = st.secrets
firebase = pyrebase.initialize_app(config)
database = firebase.database()



# Authentication
auth = firebase.auth()
login.login_page(auth)

# Title
st.title('Erfahrungsschatz')

st.chat_input('Start journaling...')
st.help(st.chat_input)