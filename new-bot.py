import streamlit as st
import taskingai
import logging

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

# Initialize TaskingAI with API key and assistant ID
taskingai.init(api_key='taL9voVQCs4oaZKsZDFzo5nwuI2R2Q4E')
assistant_id = "X5lMrrRkWc3BPkp17yAoRFdF"

st.title("💬 Chat with Assistant")

# Helper function to handle the chat interaction
def handle_chat(user_input):
    try:
        if 'chat_id' not in st.session_state:
            # Start a new chat session
            chat = taskingai.assistant.create_chat(assistant_id=assistant_id)
            st.session_state['chat_id'] = chat.chat_id
            st.session_state['messages'] = [{'role': 'assistant', 'content': "How can I help you?"}]
        
        # Log user's message
        st.session_state['messages'].append({'role': 'user', 'content': user_input})
        
        # Send user message to TaskingAI
        taskingai.assistant.create_message(
            assistant_id=assistant_id,
            chat_id=st.session_state['chat_id'],
            text=user_input,
        )
        
        # Get response from TaskingAI
        assistant_message = taskingai.assistant.generate_message(
            assistant_id=assistant_id,
            chat_id=st.session_state['chat_id'],
        )
        
        # Log assistant's message
        st.session_state['messages'].append({'role': 'assistant', 'content': assistant_message.content.text})
    except Exception as e:
        logging.error("Error in chat interaction: %s", e)
        st.session_state['messages'].append({'role': 'assistant', 'content': "Error processing your message."})

# Display chat messages
for msg in st.session_state.get('messages', []):
    st.chat_message(msg['role']).write(msg['content'])

# Chat input for user messages
user_input = st.chat_input()
if user_input:
    handle_chat(user_input)
