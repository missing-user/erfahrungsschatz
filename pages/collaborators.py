import streamlit as st
import pyrebase
import hashlib

from streamlit_extras.switch_page_button import switch_page
if "auth_user" not in st.session_state or not st.session_state["auth_user"]:
  switch_page("login")

config = st.secrets

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

st.title("Invite collaborators")

def shash(email):
  return hashlib.md5(email.encode("utf-8")).hexdigest()

# Input to send a collaboration request
with st.form(key="collab_input"):
  col1, col2 = st.columns([4,1])
  partner_email = col1.text_input("Share your insights with a collaborator", placeholder="Enter email address", label_visibility="collapsed")
  if col2.form_submit_button("Send", type="primary") and partner_email:
    try:
      db.child("collabrequests").child(shash(partner_email)).push(st.session_state["auth_user"]["idToken"])
      st.success(f'Collaboration request sent to {partner_email}')
    except:
      st.error(f'Error sending collaboration request to {partner_email}')

st.divider()
uid = st.session_state["auth_user"]["localId"]
myhash = shash(st.session_state["auth_user"]["email"])

# Get the list of collaborators
collaborators = db.child("collaborators").child(uid).get().each()
if collaborators:
  st.title("Your collaborators")

  colab_ids = []
  for col in collaborators:
    colab_ids.append(col.key())
    partner_email = col.val()
    with st.chat_message(partner_email):
      st.write(partner_email)
  st.session_state["collaborators"] = collaborators
  st.divider()


# Check if there are any pending collaboration requests
collab_requests = db.child("collabrequests").child(myhash).get().each()
if collab_requests:
  st.warning("You have pending collaboration requests:")

  for collab_req in collab_requests:
    partner = auth.get_account_info(collab_req.val())
    partner_email = partner["users"][0]["email"]
    partner_uid = partner["users"][0]["localId"]

    with st.chat_message(partner_email):
      col1, col2, col3 = st.columns([4,1,1])
      with col1:
        placeholder = st.empty()
        placeholder.write(f"{partner_email} wants to collaborate with you")
      with col2:
        if st.button("Accept", key=collab_req.key()+"accept"):
          # Add the collaborator to the current user's collaborators list and vice versa
          db.child("collaborators").child(uid).child(partner_uid).set(partner_email)
          db.child("collaborators").child(partner_uid).child(uid).set(partner_email)
          # Remove the collaboration request
          db.child("collabrequests").child(myhash).remove(collab_req.key())
          with col1:
            placeholder.success(f"You are now collaborating with {partner_email}")
      with col3:
        if st.button("Decline", key=collab_req.key()+"decline"):
          # Remove the collaboration request
          db.child("collabrequests").child(myhash).remove(collab_req.key())
          with col1:
            placeholder.error(f'Collaboration request from {partner_email} declined')
