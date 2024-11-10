import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="centered",
)

# Custom CSS for chat alignment
st.markdown("""
    <style>
    .user-chat {
        text-align: right;
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 15px;
        max-width: 80%;
        margin-left: auto;
        margin-right: 0;
    }
    .assistant-chat {
        text-align: left;
        background-color: #E0E0E0;
        padding: 10px;
        border-radius: 15px;
        max-width: 80%;
        margin-left: 0;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.welcome_shown = False  # Flag to control welcome message display

# Display the chatbot's title on the page
st.title("🤖 InterviewIQ")

# Display the welcome message if it's the start of the session
if not st.session_state.welcome_shown:
    with st.chat_message("assistant"):
        st.markdown("<div class='assistant-chat'>Hello, and welcome to InterviewIQ. I’ll be your interviewer today, guiding you through technical and interpersonal questions aligned with the job description you provided. Please begin by introducing yourself.</div>", unsafe_allow_html=True)
    st.session_state.welcome_shown = True  # Ensure welcome message shows only once

# Display the chat history
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    class_name = "assistant-chat" if role == "assistant" else "user-chat"
    with st.chat_message(role):
        st.markdown(f"<div class='{class_name}'>{message.parts[0].text}</div>", unsafe_allow_html=True)

# Input field for user's message
user_prompt = st.chat_input("Ask AI...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(f"<div class='user-chat'>{user_prompt}</div>", unsafe_allow_html=True)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(f"<div class='assistant-chat'>{gemini_response.text}</div>", unsafe_allow_html=True)
