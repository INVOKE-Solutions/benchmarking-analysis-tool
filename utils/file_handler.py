import pandas as pd
import streamlit as st

def upload_file():
    """Handle file upload"""
    uploaded_file = st.file_uploader("Upload data in CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                return pd.read_csv(uploaded_file)
            else:
                return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")
    return None
