import streamlit as st
def login_page(auth):

  email, pw = st.text_input('Email'), st.text_input('Password', type='password')
  if st.button('Log In'):
      try:
          auth.sign_in_with_email_and_password(email, pw)
      except:
          st.write('Invalid email or password')
          
  if st.button('Sign Up'):
      try:
          auth.create_user_with_email_and_password(email, pw)
      except:
          st.write('Something went wrong...')
  st.write('User:', auth.current_user)


