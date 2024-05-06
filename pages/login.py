import streamlit as st
import pyrebase
import extra_streamlit_components as stx


@st.cache_resource()
def get_manager():
    return stx.CookieManager()


def login(auth: pyrebase.pyrebase.Auth):
    if "auth_user" not in st.session_state:
        st.session_state["auth_user"] = None

    uid_cookie = get_manager().get("utoken")
    # st.write('uid_cookie', get_manager().get_all())
    if uid_cookie:
        try:
            auth.sign_in_with_custom_token(uid_cookie)
            st.write("Logged in as", auth.current_user)
        except:
            login_page(auth)
    else:
        login_page(auth)


def login_page(auth: pyrebase.pyrebase.Auth):
    email, pw = st.text_input("Email", key="email"), st.text_input(
        "Password", type="password", key="password"
    )
    if st.button("Log In"):
        try:
            auth.sign_in_with_email_and_password(email, pw)
            # st.write(auth.create_custom_token(auth.current_user["localId"]))
            # get_manager().set('utoken', auth.create_custom_token(auth.current_user["idToken"]))
        except:
            st.write("Invalid email or password")

    if st.button("Sign Up"):
        auth_result = None
        try:
            auth_result = auth.create_user_with_email_and_password(email, pw)
            # auth.send_email_verification(auth.current_user["idToken"])
        except:
            st.write("Something went wrong...", auth_result)
    st.write("User:", auth.current_user)
    st.session_state["auth_user"] = auth.current_user


config = st.secrets
firebase = pyrebase.initialize_app(config)
db = firebase.database()

if "auth_user" not in st.session_state or not st.session_state["auth_user"]:
    auth = firebase.auth()
    login_page(auth)
