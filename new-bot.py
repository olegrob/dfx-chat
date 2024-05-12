import streamlit as st
import taskingai
import logging
from taskingai.assistant.memory import AssistantNaiveMemory
import sys
st.write(sys.executable)

logging.basicConfig(level=logging.DEBUG)

# Initialize TaskingAI with API key
taskingai.init(api_key='taL9voVQCs4oaZKsZDFzo5nwuI2R2Q4E')
assistant_id = "X5lMrrRkWc3BPkp17yAoRFdF"

def start_chat():
    try:
        # Fetching recent chats
        chats = taskingai.assistant.list_chats(
            assistant_id=assistant_id,
            order="desc",
            limit=20
        )
        welcome_message = "Tere! Ma olen Datafoxi käsitsi tehtud ja treenitud robot!"
        chat_history = [{'message': chat.last_message.text, 'is_user': chat.last_message.role == 'user'} for chat in chats]
        return welcome_message, chat_history
    except Exception as e:
        logging.error("Error starting chat: %s", e)
        return "Error starting chat: {}".format(e), []

def send_message(user_input):
    if not user_input:
        return "No message provided"
    
    try:
        chat = taskingai.assistant.create_chat(assistant_id=assistant_id)
        taskingai.assistant.create_message(
            assistant_id=assistant_id,
            chat_id=chat.chat_id,
            text=user_input,
        )
        assistant_message = taskingai.assistant.generate_message(
            assistant_id=assistant_id,
            chat_id=chat.chat_id,
        )
        return assistant_message.content.text
    except Exception as e:
        return "Error sending message: {}".format(e)

# Streamlit UI
st.title('Chat with Assistant')
if 'history' not in st.session_state:
    st.session_state['history'] = []

if st.button('Start Chat'):
    welcome_message, history = start_chat()
    st.session_state['history'] = history
    st.write(welcome_message)

user_input = st.text_input('Your message:', '')
if st.button('Send'):
    if user_input:
        response = send_message(user_input)
        st.session_state['history'].append({'message': user_input, 'is_user': True})
        st.session_state['history'].append({'message': response, 'is_user': False})
        for chat in st.session_state['history']:
            if chat['is_user']:
                st.text_area('You:', chat['message'], height=70)
            else:
                st.text_area('Assistant:', chat['message'], height=70)
    else:
        st.error('Please enter a message.')

