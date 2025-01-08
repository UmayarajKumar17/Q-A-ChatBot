import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
import time

# Streamlit Page Configuration
st.set_page_config(
    page_title="Conversational Q&A Chatbot",
    page_icon="💬",
    layout="wide"
)

# Chat Header
st.markdown(
    """
    <style>
        .chat-header {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            color: #4CAF50;
        }
        .message-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
            margin-bottom: 10px;
        }
        .message-box {
            margin: 10px 0;
            padding: 10px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background-color: #DCF8C6;
            align-self: flex-end;
            text-align: right;
        }
        .ai-message {
            background-color: #F1F0F0;
            align-self: flex-start;
            text-align: left;
        }
        .dark-theme {
            background-color: #333;
            color: #eee;
        }
        .dark-theme .message-container {
            background-color: #444;
            border-color: #555;
        }
        .dark-theme .message-box {
            background-color: #555;
        }
        .dark-theme .user-message {
            background-color: #4CAF50;
        }
        .dark-theme .ai-message {
            background-color: #666;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="chat-header">💬 Conversational Q&A Chatbot</div>', unsafe_allow_html=True)

# Initialize LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key="/",  # Replace with your actual API key
    model_name="llama-3.1-70b-versatile"
)

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state["history"] = [SystemMessage(content="You are a helpful AI assistant.")]
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# Function to get response from the chat model
def get_chatmodel_response(question):
    st.session_state["history"].append(HumanMessage(content=question))
    # Simulate AI typing delay
    with st.spinner("AI is thinking..."):
        time.sleep(1.5)
    answer = llm.invoke(st.session_state["history"])
    st.session_state["history"].append(AIMessage(content=answer.content))
    return answer.content

# Theme Toggle
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🌙 Dark Mode" if st.session_state["theme"] == "light" else "☀️ Light Mode"):
        st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

# Apply Theme
theme_class = "dark-theme" if st.session_state["theme"] == "dark" else ""

# Chat Interface
st.markdown(f'<div class="message-container {theme_class}" id="chat-container">', unsafe_allow_html=True)
for msg in st.session_state["history"]:
    if isinstance(msg, HumanMessage):
        st.markdown(
            f'<div class="message-box user-message {theme_class}">{msg.content}</div>',
            unsafe_allow_html=True
        )
    elif isinstance(msg, AIMessage):
        st.markdown(
            f'<div class="message-box ai-message {theme_class}">{msg.content}</div>',
            unsafe_allow_html=True
        )
st.markdown("</div>", unsafe_allow_html=True)

# User Input and Submit Button
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input(
        "Type your question here:",
        key="input",
        placeholder="Ask me anything...",
    )
with col2:
    submit = st.button("Send", type="primary")

if submit and user_input.strip():
    # Get the LLM response
    ai_response = get_chatmodel_response(user_input)

    # Scroll to bottom of chat history
    st.markdown(
        """
        <script>
        var container = document.getElementById("chat-container");
        container.scrollTop = container.scrollHeight;
        </script>
        """,
        unsafe_allow_html=True
    )

    # Clear the input field
    st.session_state["input"] = ""

# Footer
st.markdown(
    """
    <hr>
    <div style="text-align: center; color: grey; font-size: small;">
        Powered by your custom LLM | © 2025
    </div>
    """,
    unsafe_allow_html=True
)
