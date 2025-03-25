import pandas as pd
import streamlit as st
from openai import OpenAI
import logging

def analyze_data(df: pd.DataFrame, user_prompt: str) -> str:

    # Log user prompt
    logging.info(f"User Prompt: {user_prompt}")

    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

    if not user_prompt:
        st.error("User prompt cannot be empty.")
        raise ValueError("User prompt cannot be empty.")
    else:
        prompt = user_prompt

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data analysis expert."},
            {"role": "user", "content": f"{prompt}\\n\\n{df}"},
        ]
    )

    analysis_result = response.choices[0].message.content

    return analysis_result
