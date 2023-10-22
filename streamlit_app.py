import streamlit as st
import pyrebase
import login
import datetime

config = st.secrets
st.title('Erfahrungsschatz')

firebase = pyrebase.initialize_app(config)
db = firebase.database()

if "auth_user" not in st.session_state or not st.session_state["auth_user"]:
  auth = firebase.auth()
  login.login(auth)

def entry(data, key):
  message = data["entry"]
  date = data["date"]
  with st.chat_message("human"):
    col1, col2 = st.columns([8,1])
    with col1:
      if "editing" in st.session_state and st.session_state["editing"] == key:
        edit_inp = st.text_area("Editing entry", value=message, key=key+"_edit")
        if edit_inp != message:
          db.child("journals").child(uid).child(key).update({"entry": edit_inp, "date": date})
          st.write("Updated entry", key)
          del st.session_state["editing"]
          st.rerun()
      else:
        st.markdown(message)
    with col2:
      if st.button("Edit", key=key):
        st.session_state["editing"] = key
        st.rerun()

if st.session_state["auth_user"]:
  uid = st.session_state["auth_user"]["localId"]
  st.write(st.session_state["auth_user"])

  #.order_by_child("date").limit_to_last(15)
  entries = db.child("journals").child(uid).get().each()
  print("fetching all data from db")
  if entries:
    for e in entries:
      entry(e.val(), e.key())


  journal_input = st.chat_input('Start journaling...')
  if journal_input:
    data = {'entry': journal_input, 'date': str(datetime.datetime.utcnow())}
    key = db.child("journals").child(uid).push(data)
    entry(data, key)
else:
  st.write("You need to login first")