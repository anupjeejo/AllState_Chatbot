#import libraries
import os
from dotenv import load_dotenv
import streamlit as st
from ollama import Client

#load the env variables
load_dotenv()

#streamLit page setup
st.set_page_config(
    page_title="CoverageSenseAI",
    page_icon="🤖",
    layout="centered"
)

st.title("💬 CoverageSenseAI the Policy Expert")

#initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
#show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Ollama llm setup
client = Client(
    host= os.getenv("OLLAMA_HOST")
)

#input box
user_prompt = st.chat_input("Ask chatbot...")

if user_prompt:
    #display user prompt on UI
    st.chat_message("user").markdown(user_prompt)
    
    #add the user promt to chat history
    st.session_state.chat_history.append(
        {
            "role": "user", 
            "content": user_prompt
        }
    )
    
    #call the llm with and pass the chat history along with it
    response_stream  = client.chat(
        model="gemma3:4b",
        messages=[
            {   
                "role": "system", 
                "content": """  You are an expert virtual assistant specializing in United States insurance policies. 
                                You provide accurate, clear, and up-to-date information about US-based insurance, including 
                                health insurance, auto insurance, homeowners and renters insurance, life insurance, disability 
                                insurance, Medicare, Medicaid, and employer-sponsored plans.

                                Your responsibilities include:
                                    - Explaining insurance concepts, terms, coverage types, premiums, deductibles, copays, and exclusions
                                    - Describing differences between policy types and providers in the US market
                                    - Guiding users on eligibility, enrollment periods, and general claim processes
                                    - Clarifying federal and state-level insurance regulations at a high level
                                    - Providing educational information without offering legal, medical, or financial advice

                                Always:
                                - Use simple, easy-to-understand language
                                - Ask clarifying questions when user input is incomplete
                                - Avoid guaranteeing coverage, pricing, or approval
                                - Encourage users to verify details with licensed agents or official providers when necessary

                                If a question is outside your scope or requires professional advice, clearly state the limitation 
                                and redirect the user appropriately.
                            """
            },
            *st.session_state.chat_history
            
        ],
        stream=True
    )
    
    #llm respose object
    llm_response = ""

    #parsing and displaying the llm response 
    with st.chat_message("assistant"):
        placeholder = st.empty()
        for chunk in response_stream:
            token = chunk["message"]["content"]
            llm_response += token
            placeholder.markdown(llm_response)

    #store llm response to chat history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": llm_response
    })