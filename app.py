import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Force load .env (fix for VS Code)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Debug
st.write("API KEY:", GOOGLE_API_KEY)

# 🚨 Stop if key missing
if not GOOGLE_API_KEY:
    st.error("❌ API Key not found. Check your .env file.")
    st.stop()

# Page Title
st.title("Movie Recommender System using Gemini 🍿")

# User Input
user_input = st.text_input(
    "Enter a movie title, genre or keywords (e.g. sci-fi movie)"
)

# Prompt Template
template = PromptTemplate(
    input_variables=["user_input"],
    template="Suggest 5 movies similar to {user_input}"
)

# Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # safer model
    google_api_key=GOOGLE_API_KEY
)

# Generate recommendation
if user_input and user_input.strip():
    try:
        chain = template | llm
        response = chain.invoke({"user_input": user_input})

        st.write("### Recommendations for you")
        st.write(response.content)

    except Exception as e:
        st.error(e)
