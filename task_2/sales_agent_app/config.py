import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Check if API key is set
if not api_key:
    st.error("❌ API Key is missing! Please set it in the .env file.")
    st.stop()

# Configure the Gemini API
genai.configure(api_key=api_key)
