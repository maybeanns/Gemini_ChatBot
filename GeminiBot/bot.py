from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
import base64
from streamlit_option_menu import option_menu
genai.configure(api_key=os.getenv("Google_API_key"))


## function to load Gemini Pro model and get repsonses


model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])
def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

##initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")


selected = option_menu(
    menu_title = None,
    options =["Chat Bot", "Projects", "Contacts"],
    icons= ["house", "book", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)
st.header("Gemini LLM ChatBot")    

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Input: ",key="input")
submit=st.button("Enter the question")


if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("Response:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("Chat History:")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
    

