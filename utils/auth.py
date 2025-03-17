import streamlit as st

def authenticate_user():
    """Simple authentication using Streamlit secrets"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        password = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            if password == st.secrets["PASSWORD"]:
                st.session_state.authenticated = True
                st.success("Login successful!")
                return True
            else:
                st.error("Incorrect password")
        st.stop()