import pandas as pd
import streamlit as st
from openai import OpenAI
import logging

def analyze_data(df: pd.DataFrame, user_prompt: str) -> str:

    # Log user prompt
    logging.info(f"User Prompt: {user_prompt}")

    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

    if not user_prompt:
        prompt = """
        Provide a comprehensive industry benchmarking analysis using the data provided in not more than 10000 words. The ultimate goal of this analysis is to help companies understand their competitive position in the market and identify areas for improvement.
        Your analysis should consists the following sections:

        1. Financial Performance Analysis
        Profitability Trends: Compare profitability for each company and rank them.
        Industry Benchmarks: Identify the average revenue, expenses, and profitability across different industries.

        2. Product Portfolio Analysis
        Product Diversity vs. Revenue: See if companies with a wider product range generate higher revenue.
        Popular Product Trends: Identify common product lines among top-performing companies.
        Niche vs. Generalist Strategy: Compare revenue of companies with a broad product line vs. specialized product offerings.
        
        3. Social Media Engagement Analysis
        Follower-to-Revenue Correlation: Check if higher social media engagement translates to higher revenue.
        Platform Effectiveness: Identify which social media platforms drive the most engagement.
        Brand Awareness Ranking: Rank companies based on social media presence and growth.
        
        4. Competitor Benchmarking & Strategy Insights
        High-Growth Companies: Identify which companies are expanding rapidly and analyze their strategies.
        Marketing Effectiveness: Compare revenue between companies with high and low social media engagement.
        Industry Leaders vs. Challengers: Spot established industry leaders and fast-rising competitors.

        5. Recommendations & Conclusion
        Key Insights: Summarize the most important findings from your analysis.
        Strategic Recommendations: Provide actionable recommendations for companies to improve their performance.
        Conclusion: Draw conclusions and provide a summary of the analysis.

        Your output should be a publication-ready report in markdown format." \
        """
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
