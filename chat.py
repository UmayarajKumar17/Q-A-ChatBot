import streamlit as st
from dotenv import load_dotenv
from langchain.schema import HumanMessage,SystemMessage,AIMessage
from langchain_groq import ChatGroq
import os

st.set_page_config(page_title="💬Question & Answer Chatbot")
st.header("Ask the Question 🌙")
load_dotenv()

llm = ChatGroq (
    temperature=0,
    groq_api_key = os.getenv("api_key"), 
    model_name="llama-3.3-70b-versatile"
)

if 'history' not in st.session_state:
    st.session_state['history']=[
        SystemMessage(content="Yor are a friendly AI assitant")
    ]


def get_chatmodel_response(question):

    st.session_state['history'].append(HumanMessage(content=question))
    answer=llm.invoke(st.session_state['history'])
    st.session_state['history'].append(AIMessage(content=answer.content))
    return answer.content

input=st.text_input("Input: ",key="input")
response = get_chatmodel_response(input)

submit=st.button("Generate the Response")


if submit:
    st.subheader("The Generated Response is:")
    st.write(response)