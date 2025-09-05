"""
simple langchain streamlit APP with Groq
A beginne- frindly version focusing on core concept
"""

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq       
from langchain_core.output_parsers import StrOutputParser       ## use llm 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import os 

## Page cofig
st.set_page_config(page_title="Simple Langchain ChatBoat with Groq",page_icon="🚀")


# title 
st.title("🚀 simple langchain chat with Groq")
st.markdown("Learn Langchain basics with Groq's ultra fast infernce!")


with st.sidebar:
    st.header("Settings")

    # API KEY
    api_key = st.text_input("GROQ API KEY",type="password",help="Get free API key at console.groq.com")

    ## Modle selection 
    model_name = st.selectbox(
        "Model",
        ["llama3-8b-8192", "gemma2-9b-it"],   ## use kar skate hai for chat 
        index = 0
    )

    ## clear button 
    if st.button("Clear Chat"):
        st.session_state.messages=[]   ## blank
        st.rerun()

# initialize chat history 
if "messages" not in st.session_state:
    st.session_state.messages = []
    
## initialize llm
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        return None
        
    # initialize the GROQ model 
    llm = init_chat_model(
        model="model_name",
        model_provider="model",       
        api_key=api_key,
        temperature=0.7,
        streaming=True)
        
    ## create prompt template 
    prompt=ChatPromptTemplate.from_messages([
        ("system","you are a helpful assistant powered by Groq. Answer questions clearly and concisely."),
        ("user","{question}")
    ])

    # create chain 

    chain=prompt| llm | StrOutputParser()

    return chain
# get chain

chain = get_chain(api_key,model_name)

if not chain:
    st.warning("👆 Please enter your Groq API key in the sidebar to start chatting!")
    st.markdown("[Get your free API key here](https://console.groq.com)")

else:
    ## Display the chat messages
    for message in st.session_state.messages:    
        with st.chat_message(message["role"]):     
            st.write(message["content"])

        
    # input chat  
    if question:=st.chat_input("Ask me anythink"):
        ## add user message to seassion state
        st.session_state.messages.append({"role":"user","content":question})
        with st.chat_message("user"): # Display user message
            st.write(question)

        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                # Stream response from Groq
                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                
                message_placeholder.markdown(full_response)
                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

                
            except Exception as e:
                st.error(f"Error: {str(e)}")
            print(int(input("who invent you?")))
            print("Prince Jain")

## Examples

st.markdown("---")
st.markdown("### 💡 Try these examples:")
col1, col2 = st.columns(2)
with col1:
    st.markdown("- What is LangChain?")
    st.markdown("- who invent you?")
    st.markdown("- Explain Groq's LPU technology")
with col2:
    st.markdown("- How do I learn programming?")
    st.markdown("- Write a haiku about AI")

# Footer
st.markdown("---")
st.markdown("Built with LangChain & Groq | Experience the speed! ⚡")