import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load authentication configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def authenticate():
    """Streamlit-Authenticator based authentication"""
    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status:
        st.session_state.authenticated = True
        st.success(f"Welcome {name}!")
    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")
        st.stop()