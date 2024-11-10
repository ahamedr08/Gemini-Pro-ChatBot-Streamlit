import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    # Start the chat session with an initial welcome message
    st.session_state.chat_session = model.start_chat(history=[
        {"role": "model", "content": "Hello, and welcome to InterviewIQ. I’ll be your interviewer today, guiding you through technical and interpersonal questions aligned with the job description you provided. Please begin by introducing yourself."}
    ])

# Display the chatbot's title on the page
st.title("🤖 InterviewIQ")

# Add custom CSS for chat alignment
st.markdown("""
    <style>
    .chat-message.assistant {
        text-align: left;
        background-color: #f1f0f0;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 30% 10px 0;
    }
    .chat-message.user {
        text-align: right;
        background-color: #dcf8c6;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0 10px 30%;
    }
    </style>
""", unsafe_allow_html=True)

# Display the chat history
for message in st.session_state.chat_session.history:
    role_class = translate_role_for_streamlit(message["role"])
    st.markdown(f'<div class="chat-message {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Input field for user's message
user_prompt = st.chat_input("Ask AI...")
if user_prompt:
    # Add user's message to chat and display it
    st.session_state.chat_session.history.append({"role": "user", "content": user_prompt})
    st.markdown(f'<div class="chat-message user">{user_prompt}</div>', unsafe_allow_html=True)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    st.session_state.chat_session.history.append({"role": "model", "content": gemini_response.text})

    # Display Gemini-Pro's response
    st.markdown(f'<div class="chat-message assistant">{gemini_response.text}</div>', unsafe_allow_html=True)
