import streamlit as st
import pandas as pd
import os
from utils.auth import authenticate
from utils.file_handler import upload_file
from utils.openai_api import analyze_data
from utils.pdf_generator import generate_pdf

def main():
    st.title("Data Analysis App with OpenAI")
    authenticate()
    
    df = upload_file()
    if df is not None:
        st.write("### Preview of Uploaded Data")
        st.dataframe(df.head())
        
        if st.button("Analyze Data"):
            with st.spinner("Analyzing data..."):
                analysis_result = analyze_data(df)
                st.session_state.analysis_result = analysis_result
                st.success("Analysis complete!")
                st.text_area("Analysis Result", analysis_result, height=200)
        
        if "analysis_result" in st.session_state:
            pdf_path = generate_pdf(st.session_state.analysis_result)
            
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_file,
                    file_name="analysis_report.pdf",
                    mime="application/pdf"
                )
            
            os.remove(pdf_path)

if __name__ == "__main__":
    main()