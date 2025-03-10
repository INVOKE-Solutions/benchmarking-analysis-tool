import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_data(df):
    prompt = ""  # User-defined prompt
    data_summary = df.head().to_csv(index=False)

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data analyst."},
            {"role": "user", "content": f"{prompt}\\n\\n{data_summary}"},
        ]
    )

    return response["choices"][0]["message"]["content"].strip()
