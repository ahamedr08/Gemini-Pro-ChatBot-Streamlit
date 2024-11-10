import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings with a custom theme
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",     # Page layout option
)

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

# Add custom CSS styling for chat messages
st.markdown("""
    <style>
        .user-message {
            background-color: #e8f5ff;
            color: #1e3a5f;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            font-weight: bold;
        }
        .assistant-message {
            background-color: #f5e8ff;
            color: #3a1e5f;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

# Display the chatbot's title with a vibrant header
st.title("🤖 **InterviewIQ** - Your AI Interview Coach")

st.markdown("---")  # Adds a line divider

# Display the chat history with color-coded message bubbles
for message in st.session_state.chat_session.history:
    message_class = "assistant-message" if translate_role_for_streamlit(message.role) == "assistant" else "user-message"
    st.markdown(f"<div class='{message_class}'>{message.parts[0].text}</div>", unsafe_allow_html=True)

# Input field for the user's message
user_prompt = st.text_input("💬 Ask me anything about interviews!", "")
if user_prompt:
    # Add the user's message to chat history and display it
    st.markdown(f"<div class='user-message'>{user_prompt}</div>", unsafe_allow_html=True)

    # Send the message to Gemini-Pro and retrieve the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    st.markdown(f"<div class='assistant-message'>{gemini_response.text}</div>", unsafe_allow_html=True)
