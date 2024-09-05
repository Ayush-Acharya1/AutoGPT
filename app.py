from langchain.chains import ConversationChain
import streamlit as st
import os
from langchain_groq import  ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.chains.conversation.memory import ConversationBufferMemory

#memory constructor

if 'generated' not in st.session_state:
    st.session_state['generated']=[]
if 'past' not in st.session_state:
    st.session_state['past']=[]
if 'input' not in st.session_state:
    st.session_state['input']=''




load_dotenv()
groq_api_key=os.getenv('apikey')
st.title('AutoGPT')

chat=ChatGroq(temperature=0.6,model_name='llama3-8b-8192',groq_api_key=groq_api_key)
#text=ChatPromptTemplate.from_template('You are a AI assistant and your tast is to create a story based on the question provided. Start the story directly without saying interesting. No need to give explanation. i want only the story. it can be based on fiction or based on true events. the question is here :Question:{input}')
text=ChatPromptTemplate.from_template('You are a AI assistant and you answer the question in details. answer based on the context: {context}. the question is here :Question:{input}')
if 'memory' not in st.session_state:
    st.session_state.memory=ConversationBufferMemory()
inputText=st.text_input('Enter the Prompt')

#print(st.session_state.memory)
print(*st.session_state.past)
print(*st.session_state.generated)
conversation=ConversationChain(llm=chat,memory=st.session_state.memory,input_key='input',output_key='response')
print(inputText)
if inputText:
    prompt=text.format(context=st.session_state.past,input=inputText)
    response=conversation({'input':inputText})
    st.session_state.past.append(prompt)
    st.session_state.generated.append(response['response'])
    st.write('Chatbot:',response['response'])
    #i want to add new chat button feature with session storage and also langchain for chatbot. when the person click button , it creates new chat