import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq

# Streamlit Page Configuration
st.set_page_config(
    page_title="Conversational Q&A Chatbot",
    page_icon="💬",
    layout="centered"
)

# Chat Header
st.markdown(
    """
    <style>
        .chat-header {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
            color: #4CAF50;
        }
        .message-box {
            margin: 10px 0;
            padding: 10px;
            border-radius: 10px;
        }
        .user-message {
            background-color: #DCF8C6;
            text-align: right;
        }
        .ai-message {
            background-color: #F1F0F0;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="chat-header">💬 Conversational Q&A Chatbot</div>', unsafe_allow_html=True)

# Initialize LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key="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",  # Replace with your actual API key
    model_name="llama-3.1-70b-versatile"
)

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state["history"] = [SystemMessage(content="You are a helpful AI assistant.")]

# Function to get response from the chat model
def get_chatmodel_response(question):
    st.session_state["history"].append(HumanMessage(content=question))
    answer = llm.invoke(st.session_state["history"])
    st.session_state["history"].append(AIMessage(content=answer.content))
    return answer.content

# Chat interface
response_placeholder = st.empty()  # Placeholder for chat messages
user_input = st.text_input("Type your question here:", key="input", placeholder="Ask me anything...", on_change=lambda: None)
submit = st.button("Send")

if submit and user_input.strip():
    # Get the LLM response
    ai_response = get_chatmodel_response(user_input)

    # Display chat messages
    with response_placeholder.container():
        for msg in st.session_state["history"]:
            if isinstance(msg, HumanMessage):
                st.markdown(
                    f'<div class="message-box user-message">{msg.content}</div>',
                    unsafe_allow_html=True
                )
            elif isinstance(msg, AIMessage):
                st.markdown(
                    f'<div class="message-box ai-message">{msg.content}</div>',
                    unsafe_allow_html=True
                )

    # Clear the input field
    st.session_state["input"] = ""

# Footer
st.markdown(
    """
    <hr>
    <div style="text-align: center; color: grey; font-size: small;">
        Powered by your custom LLM
    </div>
    """,
    unsafe_allow_html=True
)
