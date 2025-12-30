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

# Ollama llm setup
client = Client(
    host= os.getenv("OLLAMA_HOST")
)

#input box
user_prompt = st.chat_input("Ask chatbot...")

if user_prompt:
    #display user prompt on UI
    st.chat_message("user").markdown(user_prompt)
    
    #add the user prompt to chat history
    st.session_state.chat_history.append(
        {
            "role": "user", 
            "content": user_prompt
        }
    )

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
                                
                                Knowledge base:
                                1. Liability Coverage (Bodily Injury & Property Damage)
                                Liability coverage pays for bodily injury and property damage caused to others when the insured
                                driver is at fault. This coverage is mandatory in almost all U.S. states. Average annual cost ranges
                                from $800 to $1,500 depending on limits selected and driving profile. Mandatory in all states and
                                DC except NH (optional) and VA (fee alternative). Applicable States (Codes): AL, AK, AZ, AR, CA,
                                CO, CT, DE, GA, HI, ID, IL, IN, IA, KS, KY, LA, ME, MD, MA, MI, MN, MS, MO, MT, NE, NV, NJ,
                                NM, NY, NC, ND, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VT, WA, WV, WI, WY.

                                2. Collision Coverage
                                Collision coverage pays for repair or replacement of the insured vehicle after a collision with
                                another vehicle or object, regardless of fault. It is not mandated by state law but is commonly
                                required by lenders and leasing companies. Average annual cost ranges from $350 to $750.
                                Applicable in all states as optional coverage. State Codes: ALL STATES.
                                3. Comprehensive Coverage
                                Comprehensive coverage protects against non-collision losses such as theft, fire, flood, vandalism,
                                hail, falling objects, or animal strikes. It is optional but usually required by lienholders. Average
                                annual cost ranges from $200 to $400. Applicable in all states as optional coverage. State Codes:
                                ALL STATES.
                                
                                4. Personal Injury Protection (PIP)
                                Personal Injury Protection covers medical expenses, lost wages, and certain non-medical costs
                                regardless of fault. This coverage is mandatory in no-fault states. Average annual cost ranges from
                                $250 to $600. Mandatory or standard in: FL, HI, KS, KY, MA, MI, MN, NJ, NY, ND, OR, PA, UT.
                                Optional or limited availability elsewhere.
                                
                                5. Medical Payments Coverage (MedPay)
                                Medical Payments coverage pays medical expenses for the insured driver and passengers
                                regardless of fault. It is optional in most states and often overlaps with health insurance. Average
                                annual cost ranges from $100 to $300. Commonly available in all states; mandatory in limited form
                                in ME. State Codes: ALL STATES (mandatory: ME).
                                
                                6. Uninsured / Underinsured Motorist Coverage (UM/UIM)
                                UM/UIM coverage protects insured drivers when they are involved in an accident with a driver who
                                has no insurance or insufficient liability limits. Average annual cost ranges from $150 to $350.
                                Mandatory or strongly regulated in: CT, IL, MA, MD, MN, MO, NH, NJ, NY, NC, SC, SD, TN, TX,
                                VT, VA, WA, WI. Optional in other states.
                                
                                7. Gap Insurance
                                Gap insurance covers the difference between the vehicle’s actual cash value and the remaining
                                loan or lease balance if the vehicle is declared a total loss. It is optional and typically tied to
                                financing. Average annual cost ranges from $200 to $500. Applicable nationwide as optional
                                coverage. State Codes: ALL STATES.
                                
                                8. Rental Reimbursement Coverage
                                Rental reimbursement coverage pays for a temporary rental vehicle while the insured car is being
                                repaired due to a covered loss. Average annual cost ranges from $40 to $80. Optional in all states.
                                State Codes: ALL STATES.
                                
                                9. Roadside Assistance / Towing Coverage
                                Roadside assistance coverage provides services such as towing, jump-starts, tire changes, fuel
                                delivery, and lockout assistance. Average annual cost ranges from $20 to $60. Optional nationwide.
                                State Codes: ALL STATES.

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