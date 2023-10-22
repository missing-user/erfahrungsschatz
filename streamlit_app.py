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

database.remove()

# Create data
for i in range(3):
  data = {'userId': auth.current_user, 'entry': "abc", 'date': str(datetime.datetime.utcnow())}
  database.push(data)



for entries in database.get().each():
  with st.chat_message("user"):
    st.write(entries.val()["entry"])


# Title
st.title('Erfahrungsschatz')

st.chat_input('Start journaling...')
st.help(st.chat_input)