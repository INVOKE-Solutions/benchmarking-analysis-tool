import os
import streamlit as st
from utils.auth import authenticate_user
from utils.file_handler import upload_file
from utils.data_analysis import analyze_data
from utils.word_generator import generate_word
# from utils.pdf_generator import convert_markdown_to_pdf
import logging

# Configure logging
logging.basicConfig(filename="user_prompts.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# --------------------Page configuration--------------------

st.set_page_config(
    page_title='Benchmarking Analysis App Demo',
    layout="centered",    
    initial_sidebar_state="auto"
)

hide_streamlit_style = """
            <style>
            header {visibility: hidden;}
            footer {visibility: hidden;}
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem; padding-bottom: 4rem;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --------------------Start main page--------------------

def main():
    st.title("Benchmarking Analysis App Demo")
    # Authenticate user
    authenticate_user()
    
    df = upload_file()
    if df is not None:
        st.write("### Preview of Uploaded Data")
        st.dataframe(df.head())

        st.write("### Prompt")
        user_prompt = st.text_area("Insert your prompt here", height=300)
        st.session_state.prompt = user_prompt
        
        if st.button("Analyze Data"):
            with st.spinner("Analyzing data..."):
                analysis_result = analyze_data(df, user_prompt)
                st.session_state.analysis_result = analysis_result
                st.success("Analysis complete!")
                st.text_area("Result", analysis_result, height=500)
        
        if "analysis_result" in st.session_state:
            word_path = generate_word(st.session_state.analysis_result)
            
            with open(word_path, "rb") as word_file:
                st.download_button(
                    label="Download output as Word Document",
                    data=word_file,
                    file_name="benchmarking_analysis_app_output.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            
            os.remove(word_path)

if __name__ == "__main__":
    main()