import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings with custom theme
st.set_page_config(
    page_title="🤖 InterviewIQ",
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Custom CSS for background and styling
st.markdown("""
    <style>
        /* Full page background image */
        body {
            background-image: url('https://example.com/background-image.jpg'); /* Replace with your image URL */
            background-size: cover;
            background-position: center;
        }
        
        /* Custom styling for chat messages */
        .user-message {
            background-color: rgba(232, 245, 255, 0.9);
            color: #1e3a5f;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            font-weight: bold;
        }
        
        .assistant-message {
            background-color: rgba(245, 232, 255, 0.9);
            color: #3a1e5f;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            font-style: italic;
        }
        
        /* Center title with shadow for effect */
        .main-title {
            text-align: center;
            font-size: 36px;
            color: #ffffff;
            text-shadow: 2px 2px 8px #000000;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Display the chatbot's title with vibrant design
st.markdown("<h1 class='main-title'>InterviewIQ</h1>", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_session.history:
    message_class = "assistant-message" if translate_role_for_streamlit(message.role) == "assistant" else "user-message"
    st.markdown(f"<div class='{message_class}'>{message.parts[0].text}</div>", unsafe_allow_html=True)

# Input field for user's message
user_prompt = st.text_input("💬 Ask anything about interviews!", "")
if user_prompt:
    st.markdown(f"<div class='user-message'>{user_prompt}</div>", unsafe_allow_html=True)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    st.markdown(f"<div class='assistant-message'>{gemini_response.text}</div>", unsafe_allow_html=True)
